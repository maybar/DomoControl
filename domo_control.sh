#!/bin/sh

sleep 5
sudo pigpiod
cd /home/pi/Documents/PhytonFiles/DomoControl/
/usr/bin/python3 /home/pi/Documents/PhytonFiles/DomoControl/main.py &

