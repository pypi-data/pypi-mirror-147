from datetime import datetime
from typing import Dict

from sqlalchemy import func
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.sql.elements import BinaryExpression, and_, or_


class SqlalchemyExtensionError(Exception):
    pass


class SerializeMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_serialized_attribute(self, name: str, include=None):
        if not hasattr(self, name):
            return None
        param = self.__getattribute__(name)
        if isinstance(param, SerializeMixin):
            return param.serialize(include=include)
        elif isinstance(param, InstrumentedList):
            return [el.serialize(include=include) for el in param]
        elif isinstance(param, datetime):
            return param.timestamp()
        elif isinstance(param, memoryview):
            return param.tobytes().decode('utf-8')
        return param

    def serialize(self, only=None, include=None, exclude=None) -> Dict:
        if include is None:
            include = []
        if exclude is None:
            exclude = []

        _include_set = []
        _subincludes = []
        for key in [key.split('.') for key in include]:
            if (subincl := '.'.join(key[1:])) == '':
                subincl = []
            else:
                subincl = [subincl]

            if key[0] in _include_set:
                _subincludes[_include_set.index(key[0])].extend(subincl)
            else:
                _include_set.append(key[0])
                _subincludes.append(subincl)

        if hasattr(self, '__table__') and hasattr(self.__table__, 'columns'):
            return dict(
                [(c.key, self.get_serialized_attribute(c.key)) for c in self.__table__.columns
                 if c.key not in exclude and (only is None or c.key in only)]
                + [(key, self.get_serialized_attribute(key, include)) for key, include in zip(_include_set, _subincludes)]
            )
        return dict()


class DeserializeMixin:
    def check_constrains(self):
        if hasattr(self, '__table__') and hasattr(self.__table__, 'columns'):
            for c in self.__table__.columns:
                if not c.nullable and not c.primary_key and \
                        self.__getattribute__(c.key) is None and c.default is None:
                    raise SqlalchemyExtensionError(f'Column `{c.key}` must have not null value')
        return self

    def deserialize(self, data: Dict, only=None, exclude=None, exclude_id=True):
        if exclude is None:
            exclude = []
        if exclude_id:
            exclude.append('id')

        if hasattr(self, '__table__') and hasattr(self.__table__, 'columns'):
            columns = [c.key for c in self.__table__.columns
                       if c.key not in exclude and (only is None or c.key in only)]
            for k, v in data.items():
                if k in columns:
                    self.__setattr__(k, v)
                elif f'{k}_id' in columns and 'id' in v:
                    self.__setattr__(f'{k}_id', v['id'])

        return self


class QueryMixin:
    @classmethod
    def _filter(cls, filters: Dict, filter_type='and') -> BinaryExpression:
        def __k_v_filter(cls_, k, v, operator_='eq'):
            split_k = [k]
            if '__' in k:
                split_k = k.split('__')
                if split_k[-1] in ['gte', 'gt', 'lt', 'lte', 'neq', 'ne', 'eq', 'like', 'ieq', 'ilike']:
                    operator_ = split_k.pop()

            instrumented_attribute = cls_.__dict__[split_k[0]]
            if len(split_k) == 1:
                if operator_ == 'gte':
                    return instrumented_attribute >= v
                elif operator_ == 'gt':
                    return instrumented_attribute > v
                elif operator_ == 'lt':
                    return instrumented_attribute < v
                elif operator_ == 'lte':
                    return instrumented_attribute <= v
                elif operator_ == 'neq' or operator_ == 'ne':
                    return instrumented_attribute != v
                elif operator_ == 'like':
                    return instrumented_attribute.like(v)
                elif operator_ == 'ilike':
                    return instrumented_attribute.ilike(v)
                elif operator_ == 'ieq':
                    return func.lower(instrumented_attribute) == func.lower(v)
                else:
                    return instrumented_attribute == v
            else:
                cls2_ = instrumented_attribute.property.mapper.class_
                if instrumented_attribute.property.uselist:
                    return instrumented_attribute.any(__k_v_filter(cls2_, '__'.join(split_k[1:]), v, operator_))
                else:
                    return instrumented_attribute.has(__k_v_filter(cls2_, '__'.join(split_k[1:]), v, operator_))

        if filter_type == 'or':
            return or_(*[__k_v_filter(cls, *f) for f in filters.items()])
        else:
            return and_(*[__k_v_filter(cls, *f) for f in filters.items()])

    @classmethod
    def _order(cls, order_by=None):
        def __order_by(cls_, k, order='asc'):
            split_k = [k]
            if '__' in k:
                split_k = k.split('__')

            instrumented_attribute = cls_.__dict__[split_k[0]]
            if len(split_k) == 1:
                if order.lower() == 'desc':
                    return instrumented_attribute.desc(), []
                else:
                    return instrumented_attribute.asc(), []
            else:
                cls_ = instrumented_attribute.property.mapper.class_
                clause, joins = __order_by(cls_, '__'.join(split_k[1:]), order)
                return clause, [cls_] + joins

        return [__order_by(cls, k, order) for k, order in order_by.items()]

    @classmethod
    def complex_query(cls, filter_by=None, filter_type='and', order_by=None):
        if hasattr(cls, 'query'):
            query = cls.query
            if filter_by is not None:
                query = query.filter(cls._filter(filter_by, filter_type=filter_type))
            if order_by is not None:
                _order = cls._order(order_by)
                query = query.order_by(*[clause for clause, _ in _order])
                for _, joins in _order:
                    for join in joins:
                        query = query.join(join)
            return query
        raise SqlalchemyExtensionError(f'Class {cls} does not have query attribute')
