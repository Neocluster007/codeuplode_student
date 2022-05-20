#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

sudo /usr/bin/python3 /home/pi/MAASProject/projectPrinterNew.py & sudo /usr/bin/python3 /home/pi/MAASProject/BackendDownloadAuto.py
