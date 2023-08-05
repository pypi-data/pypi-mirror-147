from typing import Dict

from flask_sqlalchemy import Pagination


def pagination(page: Pagination, max_pages=10) -> Dict:
    return dict(
        has_next=page.has_next,
        next_num=page.next_num,
        has_prev=page.has_prev,
        prev_num=page.prev_num,
        page=page.page,
        page_range=[p for p in range(1, page.pages + 1) if page.page - max_pages//2 <= p <= page.page + max_pages//2]
    )


def serialize(page: Pagination, only=None, include=None, exclude=None, max_pages=10) -> Dict:
    return dict(
        pagination=pagination(page, max_pages=max_pages),
        items=[item.serialize(only=only, include=include, exclude=exclude) for item in page.items]
    )
