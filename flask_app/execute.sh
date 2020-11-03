#!/bin/bash

if [ -z $VIRTUAL_ENV ]
then
    echo "Activating Python Virtual Environment"
    source myenv/bin/activate
fi
export FLASK_APP=run.py
export FLASK_ENV=development
export PYTHONPATH=/home/ubuntu/workspace/raelvaes/flask_app

flask run -h 0.0.0.0