#!/bin/bash
python3 setup.py sdist
pip3 install virtualenv
virtualenv venv --system-site-packages
source venv/bin/activate
pip3 install -r requirements.txt
pip3 install .
