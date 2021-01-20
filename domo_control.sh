#!/bin/sh

sleep 1
echo " ***** DOMO_CONTROL:SH ******"
echo cd /home/pi/Documents/DomoControl/domocontrol_web
echo python3 -m http.server --cgi &

sleep 1
sudo pigpiod
pigs m 5 w
pigs m 6 w
pigs w 6 1
pigs w 5 0

cd /home/pi/Scripts/DomoControl
/usr/bin/python3 /home/pi/Scripts/DomoControl/supervisor.py &



