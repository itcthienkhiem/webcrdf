#!/bin/bash

##source ~/dev/bin/set-ocv-cuda-jdk-qt4.sh
source ~/dev/bin/set-ocv-qt4.sh

##source ./venv/bin/activate

cd webcrdf

python manage.py runserver 192.168.0.10:8001