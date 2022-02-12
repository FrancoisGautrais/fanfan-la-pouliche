#!/bin/bash

VENV=virtualenv

rm -rf $VENV 2> /dev/null
python -m venv $VENV
. $VENV/bin/activate
pip install -U pip
pip install .

python install/postinstall.py
cd src/fflp

python init.py
