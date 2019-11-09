#!/bin/sh

echo " ***** MAIN.SH ******* "
sleep 1

cd /home/pi/Scripts/DomoControl/
/usr/bin/python3 /home/pi/Scripts/DomoControl/main.py &

