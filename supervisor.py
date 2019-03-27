import psutil
import time
import tools
import private_data as private
import datetime
import pickle
import fcntl
import os, sys
import RPi.GPIO as GPIO
import logging
        
        
def start_app():
    process = psutil.Popen("/home/pi/Documents/PhytonFiles/DomoControl/main.sh")
    if process is not None:
        print("main.sh First start by supervisor ! pid={}".format(process.pid))
        logging.debug("main.sh First start by supervisor")
        time.sleep(5)
        return True
    else:
        print("main.sh First start fail ! ")
        logging.debug("main.sh First start fail !")
        return False
    
try:
    fp = open("/var/lock/supervisor.lock", 'w')
except:
    print ("Supervisor.py is already running. Exit now!")
    sys.exit(0)
        
        
print("******** SUPERVISOR.PY ************")
state = "IDLE"
print ("Supervisor>> IDLE")
pid = 0
process = psutil.Process()
watchdog_pin = False
error_counter = 0
email_enabled = False
try:
    correo = tools.Email(private)
    email_enabled = True
except Exception as e:
    print ("Supervisor. Error openning email"+str(e))
    
LedCtrl = tools.LedDualColor(6, 5)
restart_counter = 0
current_pid = psutil.Process().pid
header = "***Supervisor. PID: "+ str(current_pid) +"\nStart time: "+str(datetime.datetime.now()) + "\n"
str_detail=header
count_no_app =0
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
logging.basicConfig(filename='/var/tmp/supervisor.log',format='%(levelname)s:%(asctime)s %(message)s', datefmt='%d/%m %H:%M:%S', level=logging.DEBUG)


# try to start the main application
while start_app() == False:
    pass
    
while(1):
    if state == "IDLE":
        #check if the app is running the first time
        list_pid = psutil.pids()
        found = False
        LedCtrl.toggle('RED')
        for pid in list_pid:
            try:
                process = psutil.Process(pid)
                #print ("Nombre:",p.name(),"EXE:",p.exe(),"CWD:",p.cwd(),"CL:",p.cmdline(   ),"ST:",p.status())
                CL = process.cmdline()
                ST = process.status()
                for word in CL:
                    if 'main.py' in word:
                        print ("IDLE>>RUNNING")
                        state = "RUNNING"
                        found = True
                        str_detail += "Time: "+str(datetime.datetime.now()) +" IDLE>>RUNNING "+ " Status: "+ ST+ " PID: "+ str(pid)+"\n"
                        LedCtrl.setState('OFF')
                        logging.debug("IDLE>>RUNNING")
                        error_counter = 0
                        break
                    
            except (psutil.ZombieProcess, psutil.AccessDenied, psutil.NoSuchProcess):
                print ("IDLE except checking main process")
            if found == True:
                count_no_app = 0
                break
        if found == False:
            count_no_app+=1
            if count_no_app >= 20:
                start_app()
                count_no_app = 0
            
                    
        
    elif state == "RUNNING":
        #check if the application is running
        # Check watchdog couter
        error_counter +=1
        try:
            ret = GPIO.input(17)    #watchdog pin
            if watchdog_pin != ret:
                error_counter = 0
            if error_counter == 15:
                state = "STOPPED"
                str_detail += "Time: "+str(datetime.datetime.now()) +" RUNNING>>STOPPED "+ "Status: "+ ST+ " PID: "+ str(pid)+ " Reason:(watchdog is blocked)\n"
                print ("RUNNING>>STOPPED: Reason:(watchdog is blocked)")
                logging.debug("RUNNING>>STOPPED: Reason:(watchdog is blocked)")
                LedCtrl.setState('RED')
            watchdog_pin = ret
        except Exception as e:
            print ("Supervisor: Error checking hw watchdog. Error: "+str(e))
        
    elif state == "STOPPED":
        if error_counter == 15:
            try:
                process.terminate()
                time.sleep(3)
                process.kill()
            except:
                print ("except terminating process")
                str_detail += "Time: "+str(datetime.datetime.now()) +" STOPPED "+ "Status: "+ ST+ " PID: "+ str(pid)+ " Reason:(Error stoping process)\n"
                
            
        #try to start again
        process = psutil.Popen("/home/pi/Documents/PhytonFiles/DomoControl/main.sh")
        restart_counter +=1
        if process is not None:
            print("main.sh restarted ! pid={}".format(process.pid))
            str_detail += "Time: "+str(datetime.datetime.now()) +" STOPPED "+ "main.sh restarted ! pid={}\n".format(process.pid)
            if email_enabled:
                correo.send_email("Supervisor report","Detail: \n"+str_detail)
            time.sleep(5)
            pid = process.pid
            state = "IDLE"
            error_counter = 0
            count_no_app =0
            print ("STOPPED>>IDLE")            
            str_detail=header
            str_detail += "Time: "+str(datetime.datetime.now()) +" STOPPED>>IDLE "+ " restart_counter: "+ str(restart_counter)+ "\n"
        else:
            print("main.sh process open fail ! ")
            str_detail += "Time: "+str(datetime.datetime.now()) +" STOPPED "+ " Reason:(main.sh process open fail)\n"

    time.sleep(1)


        
            


