from setuptools import setup, find_packages

setup(
    name="Simple SQL",
    version='1.0',
    packages= [
        'simple_sqlite'
    ],
    description="This is a library to simplify the use of a SQLite3 database, easy to use, easy to understand.",
    long_description=open('README.md', encoding='utf-8').read(),
    author="Greem3",
    url="https://github.com/Greem3",
    install_requires=[
        'sqlite3'
    ],
)