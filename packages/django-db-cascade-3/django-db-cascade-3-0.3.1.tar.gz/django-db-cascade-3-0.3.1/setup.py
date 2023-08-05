from setuptools import setup, find_packages

setup(
    name='django-db-cascade-3',
    version='0.3.1',
    description='Fork of https://github.com/jkapelner/django-db-cascade-2.  Optionally use postgres db ON CASCADE DELETE/SET NULL on django foreign keys',
    url='http://github.com/fingul/django-db-cascade-3',
    author='Fingul',
    author_email='fingul@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'Django >= 3.0',
        'psycopg2 >= 2.5'
    ],
    classifiers=[
        'Framework :: Django',
        'Topic :: Database',
    ],
    zip_safe=False
)
