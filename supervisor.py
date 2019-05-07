import psutil
import time
import tools
import datetime
import sys
import os
import RPi.GPIO as GPIO
import logging
        
        
def start_app():
    process = psutil.Popen("/home/pi/Documents/PhytonFiles/DomoControl/main.sh")
    if process is not None:
        # print("main.sh Start by supervisor ! pid={}".format(process.pid))
        logging.debug("main.sh Start by supervisor ! pid=" + str(process.pid))
        time.sleep(5)
        return True
    else:
        print("main.sh Start fail ! ")
        logging.debug("main.sh Start fail !")
        return False
    
    

def check_if_process_name_exist(name_process, num):
    list_pid = psutil.pids()
    found = False
    count = 0
    last_pid = 0
    for pid in list_pid:
        try:
            process = psutil.Process(pid)
            #print ("Nombre:",p.name(),"EXE:",p.exe(),"CWD:",p.cwd(),"CL:",p.cmdline(   ),"ST:",p.status())
            #print ("CL:",process.cmdline(   ))
            CL = process.cmdline()
            for word in CL:
                if name_process in word:
                    count+=1
                    if count == num:
                        print ("SUP> " + name_process+ " is running! Status: PID: "+ str(last_pid))
                        logging.debug (name_process+ "is running! Status: PID: "+ str(last_pid))
                        found = True
                        break
                    last_pid = pid
        except (psutil.ZombieProcess, psutil.AccessDenied, psutil.NoSuchProcess):
            print ("except checking process "+ name_process)
            logging.debug("except checking process "+ name_process)
        if found == True:
            break
    return found, pid, process  

    
print("******** SUPERVISOR.PY ************")
if check_if_process_name_exist('supervisor.py', 2)[0] == True:
    print ("Supervisor.py is already running. Exit now!")
    sys.exit(0)
        
state = "IDLE"
print ("Supervisor>> IDLE")
pid = 0
watchdog_pin = False
error_counter = 0
timeout = 30        # sec
'''email_enabled = False
try:
    correo = tools.Email(private)
    email_enabled = True
except Exception as e:
    print ("Supervisor. Error openning email"+str(e))'''
    
LedCtrl = tools.LedDualColor(6, 5)
restart_counter = 0
current_pid = psutil.Process().pid
header = "***Supervisor. PID: "+ str(current_pid) +"\nStart time: "+str(datetime.datetime.now()) + "\n"
str_detail=header
count_no_app =0
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
logging.basicConfig(filename='/var/tmp/supervisor.log',format='%(levelname)s:%(asctime)s %(message)s', datefmt='%d/%m %H:%M:%S', level=logging.DEBUG)
cont_try = 0

# try to start the main application
while start_app() == False:
    pass
    
while(1):
    if state == "IDLE":
        #check if the app is running the first time
        LedCtrl.toggle('RED')
        found, pid, process = check_if_process_name_exist('main.py', 1)
        if found == True:
            print ("IDLE>>RUNNING")
            str_detail += "Time: "+str(datetime.datetime.now()) +" IDLE>>RUNNING "+ " PID: "+ str(pid)+"\n"
            state = "RUNNING"
            LedCtrl.setState('OFF')
            logging.debug("IDLE>>RUNNING")
            error_counter = 0
            count_no_app = 0
            cont_try = 0
        else:
            count_no_app+=1
            if count_no_app >= timeout:
                # start_app()
                os.system('/home/pi/Documents/PhytonFiles/DomoControl/main.sh')
                time.sleep(10)
                count_no_app = 0
                cont_try += 1
                # if cont_try == 5:
                #     os.system('reboot')
                               
        
    elif state == "RUNNING":
        #check if the application is running
        # Check watchdog couter
        error_counter +=1
        try:
            ret = GPIO.input(17)    # watchdog pin
            if watchdog_pin != ret:
                error_counter = 0
            if error_counter == timeout:
                state = "STOPPED"
                str_detail += "Time: "+str(datetime.datetime.now()) +" RUNNING>>STOPPED  PID: "+ str(pid)+ " Reason:(watchdog is blocked)\n"
                print ("RUNNING>>STOPPED: Reason:(watchdog is blocked)")
                logging.debug("RUNNING>>STOPPED: Reason:(watchdog is blocked)")
                LedCtrl.setState('RED')
            watchdog_pin = ret
        except Exception as e:
            print ("Supervisor: Error checking hw watchdog. Error: "+str(e))
        
    elif state == "STOPPED":
        if error_counter == timeout:
            try:
                process.terminate()
                time.sleep(3)
                process.kill()
            except:
                print ("except terminating process")
                str_detail += "Time: "+str(datetime.datetime.now()) +" STOPPED PID: "+ str(pid)+ " Reason:(Error stopping process)\n"
                
            
        #try to start again
        process = psutil.Popen("/home/pi/Documents/PhytonFiles/DomoControl/main.sh")
        restart_counter +=1
        if process is not None:
            print("main.sh restarted ! pid={}".format(process.pid))
            str_detail += "Time: "+str(datetime.datetime.now()) +" STOPPED "+ "main.sh restarted ! pid={}\n".format(process.pid)
            '''if email_enabled:
                correo.send_email("Supervisor report","Detail: \n"+str_detail)'''
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


        
            


