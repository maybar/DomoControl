#!/bin/sh

sleep 1
cd /home/pi/Documents/PhytonFiles/DomoControl/domocontrol_web
python3 -m http.server --cgi &

sleep 1
sudo pigpiod
cd /home/pi/Documents/PhytonFiles/DomoControl/
/usr/bin/python3 /home/pi/Documents/PhytonFiles/DomoControl/supervisor.py &


./main.sh &

