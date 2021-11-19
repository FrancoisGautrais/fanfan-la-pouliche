from setuptools import setup

install_requires = (
    "django",
    "pillow"
)

tests_requires = (
    "pytest",
    "pytest-django",
    "pytest-django-models",
)

setup(
    name='fanfan-la-pouliche',
    version='0.1.0',
    packages=[''],
    url='',
    license='GPL v3',
    author='fanch',
    author_email='francois@gautrais.eu',
    description='A web site'
)
