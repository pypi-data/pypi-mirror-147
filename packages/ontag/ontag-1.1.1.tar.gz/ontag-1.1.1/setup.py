from setuptools import find_packages, setup

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ontag",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    version = '1.1.1',
    description = "Olimpic Number Theory and Algebra question Generator",
    author = "Wojtek M",
    license = 'MIT',
    classifiers = 
    [
        "Programming Language :: Python :: 3.9"
    ],
    packages = ["ontag"],
    include_package_data = True,
    install_requires = [],

)


