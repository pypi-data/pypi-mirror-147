from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='flask-sqlalchemy-extension',
    version='0.0.3',
    author='Dmitry Kotlyar',
    author_email='dm.kotlyar@yandex.ru',
    description='Package provided mixins and extension for sqlalchemy and flask-sqlalchemy packages.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dkotlyar/flask-sqlalchemy-extension',
    packages=find_packages(),
    install_requires=[
        'Flask-SQLAlchemy >= 2.5.1',
        'SQLAlchemy >= 1.4.35'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
