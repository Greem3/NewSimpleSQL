from setuptools import setup, find_packages

setup(
    name="NewSimpleSQL",
    version='0.5.0',
    packages= [
        'NewSimpleSQL'
    ],
    description="This is a library to simplify the use of a SQLite3 database, easy to use, easy to understand.",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author="Greem3",
    author_email="ianpichardo575@gmail.com",
    url="https://github.com/Greem3/NewSimpleSQL",
)