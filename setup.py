import os

from setuptools import setup, find_packages
from install.utils import package_data
import sys

install_requires = (
    "django",
    "pillow",
    "unidecode",
    "django-cors-headers"
)

tests_requires = (
    "pytest",
    "pytest-django",
    "pytest-django-models",
)

setup(
    name='fanfan-la-pouliche',
    version='0.1.0',
    install_requires =install_requires,
    url='',
    packages=find_packages('src/fflp'),
    tests_require= tests_requires,
    package_dir={'': 'src/fflp'},
    license='GPL v3',
    author='fanch',
    author_email='francois@gautrais.eu',
    description='A web site',
    package_data={
         '': package_data("src/www"),
    }
)