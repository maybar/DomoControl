#!/bin/sh

sleep 1
echo " ***** DOMO_CONTROL:SH ******"
cd /home/pi/Documents/PhytonFiles/DomoControl/domocontrol_web
python3 -m http.server --cgi &

sleep 1
sudo pigpiod
pigs m 5 w
pigs m 6 w
pigs w 6 1
pigs w 5 0

cd /home/pi/Documents/PhytonFiles/DomoControl
/usr/bin/python3 /home/pi/Documents/PhytonFiles/DomoControl/supervisor.py &


./main.sh &

