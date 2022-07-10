#!/bin/bash
WORK_DIR=$(dirname "${BASH_SOURCE[0]}")
cd $WORK_DIR

VENV=$WORK_DIR/virtualenv

. $VENV/bin/activate

python3.7 flp-server $*


