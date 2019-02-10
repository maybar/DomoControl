import psutil
import time
import tools
import private_data as private
import datetime
import pickle
import fcntl
import os, sys


def lockFile(fp):
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        return False

    return True

def unlockFile(x):
    try:
        fcntl.flock(x, fcntl.LOCK_UN)
    except IOError:
        pass

try:
    fp = open("/var/lock/supervisor.lock", 'w')
except:
    print ("Supervisor.py is already running. Exit now!")
    sys.exit(0)
    
if not lockFile(fp):
    print ("Supervisor.py is already running. Exit now!")
    sys.exit(0)
        
        
print("******** SUPERVISOR.PY ************")
state = "IDLE"
print ("Supervisor>> IDLE")
pid = 0
process = psutil.Process()
watchdog_counter = 0
error_counter = 0
correo = tools.Email(private)
restart_counter = 0
current_pid = psutil.Process().pid
header = "***Supervisor. PID: "+ str(current_pid) +"\nStart time: "+str(datetime.datetime.now()) + "\n"
str_detail=header
while(1):
    if state == "IDLE":
        #check if the app is running the first time
        list_pid = psutil.pids()
        found = False
        for pid in list_pid:
            try:
                process = psutil.Process(pid)
                #print ("Nombre:",p.name(),"EXE:",p.exe(),"CWD:",p.cwd(),"CL:",p.cmdline(   ),"ST:",p.status())
                CL = process.cmdline()
                ST = process.status()
                for word in CL:
                    if '/DomoControl/main.py' in word:
                        if 'sleeping' in ST:
                            print ("IDLE>>RUNNING")
                            state = "RUNNING"
                            found = True
                            str_detail += "Time: "+str(datetime.datetime.now()) +" IDLE>>RUNNING "+ " Status: "+ ST+ " PID: "+ str(pid)+"\n"
                            break
                    
            except (psutil.ZombieProcess, psutil.AccessDenied, psutil.NoSuchProcess):
                print ("IDLE except checking main process")
            if found == True:
                break
        
    elif state == "RUNNING":
        time.sleep(1)
        #check if the application is running
        try:
            ST = process.status()
            if (not psutil.pid_exists(pid)) or (ST == psutil.STATUS_STOPPED) or (ST == psutil.STATUS_ZOMBIE):
                str_detail += "Time: "+str(datetime.datetime.now()) +" RUNNING>>STOPPED "+ "Status: "+ ST+ " PID: "+ str(pid)+ " Reason: (PID does not exist)\n"
                state = "STOPPED"
                print ("RUNNING>>STOPPED: Reason: (PID does not exist)")
            
        except (psutil.ZombieProcess):
            str_detail += "Time: "+str(datetime.datetime.now()) +" RUNNING>>STOPPED "+ "Status: "+ ST+ " PID: "+ str(pid)+ " Reason: (Process Zombie)\n"
            state = "STOPPED"
            print ("RUNNING>>STOPPED: Reason: (Process Zombie)")
        except (psutil.NoSuchProcess):
            str_detail += "Time: "+str(datetime.datetime.now()) +" RUNNING>>STOPPED "+ "Status: "+ ST+ " PID: "+ str(pid)+ " Reason:(No process)\n"
            state = "STOPPED"
            print ("RUNNING>>STOPPED: Reason:(No process)")
        # Check watchdog couter
        try:
            f = os.open("/var/tmp/debug.txt", os.O_RDONLY | os.O_NONBLOCK)
            ret = os.read(f,50)
            os.close(f)
            if watchdog_counter == ret:
                error_counter +=1
            else:
                error_counter = 0
            if error_counter == 10:
                state = "STOPPED"
                str_detail += "Time: "+str(datetime.datetime.now()) +" RUNNING>>STOPPED "+ "Status: "+ ST+ " PID: "+ str(pid)+ " Reason:(watchdog is blocked)\n"
                str_detail += "Debug file: "+ret.decode()+"\n"
                print ("RUNNING>>STOPPED: Reason:(watchdog is blocked)")
            watchdog_counter = ret
        except Exception as e:
            error_counter +=1
            print ("Supervisor: Error Opening debug.txt. Error: "+str(e))
        
    elif state == "STOPPED":
        if error_counter == 10:
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
            correo.send_email("Supervisor report","Detail: \n"+str_detail)
            time.sleep(5)
            pid = process.pid
            state = "IDLE"
            error_counter = 0
            print ("STOPPED>>IDLE")            
            str_detail=header
            str_detail += "Time: "+str(datetime.datetime.now()) +" STOPPED>>IDLE "+ " restart_counter: "+ str(restart_counter)+ "\n"
        else:
            print("main.sh process open fail ! ")
            str_detail += "Time: "+str(datetime.datetime.now()) +" STOPPED "+ " Reason:(main.sh process open fail)\n"

    time.sleep(1)

unlockFile(fp)

        
            


