import os

from setuptools import setup, find_packages
from install import do_preinstall, do_postinstall
from install.utils import package_data
import sys

if len(sys.argv)>=2 and sys.argv[1]=="migrate":
    do_postinstall()
    exit(0)

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

do_preinstall()

setup(
    name='fanfan-la-pouliche',
    version='0.1.0',
    install_requires =install_requires,
    url='',
    packages=find_packages('src'),
    tests_require= tests_requires,
    package_dir={'': 'src'},
    license='GPL v3',
    author='fanch',
    author_email='francois@gautrais.eu',
    description='A web site',
    package_data={
         '': package_data("src/www"),
    }
)

os.system(f"{sys.executable} {__file__} migrate")