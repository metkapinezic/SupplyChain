#!/bin/bash

python 01-mainpage.py
python 02-subpage.py
python 03-transformation.py
python 04-esconnect.py
python 05-sentiment.py

# Wait for 2 minutes (120 seconds)
sleep 120

python 06-dashboard.py