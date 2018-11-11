import psutil
import time

state = "IDLE"
print ("Supervisor>> IDLE")
pid = 0
while(1):
    if state == "IDLE":
        #check if the app is running the first time
        list_pid = psutil.pids()
        found = False
        for pid in list_pid:
            try:
                p = psutil.Process(pid)
                #print ("Nombre:",p.name(),"EXE:",p.exe(),"CWD:",p.cwd(),"CL:",p.cmdline(   ),"ST:",p.status())
                CL = p.cmdline()
                ST = p.status()
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
            ST = p.status()
            if (not psutil.pid_exists(pid)) or (ST == psutil.STATUS_STOPPED) or (ST == psutil.STATUS_ZOMBIE):
                print (ST)
                print ("pid does not exist")
                state = "STOPPED"
                    
        except (psutil.ZombieProcess, psutil.NoSuchProcess):
            print ("Supervisor>>STOPPED")
            state = "STOPPED"
        
    elif state == "STOPPED":
        try:
            p.terminate()
            time.sleep(3)
            p.kill()
        except:
            print ("except terminating process")
            
        #try to start again
        process_new = psutil.Popen("/home/pi/Documents/PhytonFiles/DomoControl/main.sh")
        if process_new is not None:
            print("domo_control.sh restarted ! pid={}".format(process_new.pid))
            time.sleep(5)
            pid = process_new.pid
            state = "IDLE"
            print ("Supervisor>>RUNNING")
        else:
            print("domo_control.sh process open fail ! ")
        

    time.sleep(1)

                
                
        
            

