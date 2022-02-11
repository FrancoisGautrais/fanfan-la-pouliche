from setuptools import setup, find_packages
from pathlib import Path
from install import do_preinstall, do_postinstall

def package_data(dir, relative_to=None):
    array =  []
    relative_to=Path(relative_to or Path(__file__).parent)
    stack = [Path(dir)]
    while stack:
        for path in stack.pop(0).iterdir():
            if path.is_file():
                array.append(str(path.resolve().relative_to(relative_to)))
            else:
                stack.append(path)
    return array

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

do_postinstall()