#!/bin/bash

VENV=virtualenv

rm -rf $VENV 2> /dev/null
python3 -m venv $VENV
. $VENV/bin/activate
pip install -U pip
pip install .

python3 install/postinstall.py
cd src/fflp

python3 init.py
