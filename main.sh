#!/bin/sh

echo " ***** MAIN.SH ******* "
sleep 1
sudo pigpiod
cd /home/pi/Documents/PhytonFiles/DomoControl/
/usr/bin/python3 /home/pi/Documents/PhytonFiles/DomoControl/main.py &

