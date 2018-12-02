import psutil
import time

print("******** SUPERVISOR.PY ************")
state = "IDLE"
print ("Supervisor>> IDLE")
pid = 0
process = psutil.Process()
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
                            print ("Supervisor>>RUNNING")
                            state = "RUNNING"
                            found = True
                            break
                    
            except (psutil.ZombieProcess, psutil.AccessDenied, psutil.NoSuchProcess):
                print ("except")
            if found == True:
                break
        
    elif state == "RUNNING":
        #check if the application is running
        try:
            ST = process.status()
            if (not psutil.pid_exists(pid)) or (ST == psutil.STATUS_STOPPED) or (ST == psutil.STATUS_ZOMBIE):
                print (ST)
                print ("pid does not exist")
                state = "STOPPED"
                    
        except (psutil.ZombieProcess, psutil.NoSuchProcess):
            print ("Supervisor>>STOPPED")
            state = "STOPPED"
        
    elif state == "STOPPED":
        try:
            process.terminate()
            time.sleep(3)
            process.kill()
        except:
            print ("except terminating process")
            
        #try to start again
        process = psutil.Popen("/home/pi/Documents/PhytonFiles/DomoControl/main.sh")
        if process is not None:
            print("domo_control.sh restarted ! pid={}".format(process.pid))
            time.sleep(5)
            pid = process.pid
            state = "IDLE"
            print ("Supervisor>>RUNNING")
        else:
            print("domo_control.sh process open fail ! ")
        

    time.sleep(1)

                
                
        
            


