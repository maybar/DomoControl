import psutil
import time
import tools
import private_data as private
import datetime

print("******** SUPERVISOR.PY ************")
state = "IDLE"
print ("Supervisor>> IDLE")
pid = 0
process = psutil.Process()
watchdog_counter = 0
error_counter = 0
correo = tools.Email(private)
str_detail=""
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
        time.sleep(1)
        #check if the application is running
        try:
            ST = process.status()
            if (not psutil.pid_exists(pid)) or (ST == psutil.STATUS_STOPPED) or (ST == psutil.STATUS_ZOMBIE):
                str_detail = "Status: "+ ST +"\n"
                str_detail += "PID does not exist\n"
                state = "STOPPED"
                    
        except (psutil.ZombieProcess):
            str_detail += "Process Zombie\n"
            state = "STOPPED"
        except (psutil.NoSuchProcess):
            str_detail += "No process\n"
            state = "STOPPED"
        # Check watchdog couter
        try:
            with open ('config.pickle','rb') as f:
                config_list = pickle.load(f)
                f.close()
                if (watchdog_counter == config_list[1]):
                    error_counter +=1
                else:
                    error_counter = 0
                if error_counter == 5:
                    state = "STOPPED"
                    str_detail = "Status: "+ ST +"\n"
                    str_detail +='watchdog is blocked\n'
                watchdog_counter = config_list[1]
        except Exception as e:
            pass
        
    elif state == "STOPPED":
        
        print(str_detail)
        try:
            process.terminate()
            time.sleep(3)
            process.kill()
        except:
            print ("except terminating process")
            str_detail += "Error stoping process\n"
            
        #try to start again
        process = psutil.Popen("/home/pi/Documents/PhytonFiles/DomoControl/main.sh")
        if process is not None:
            print("main.sh restarted ! pid={}".format(process.pid))
            str_detail += "main.sh restarted ! pid={}\n".format(process.pid)
            time.sleep(5)
            pid = process.pid
            state = "IDLE"
            print ("Supervisor>>RUNNING")
            correo.send_email("Supervisor report","Application restarted \n Time: "+str(datetime.datetime.now())+"\nDetail: \n"+str_detail)
            str_detail = ""
        else:
            print("main.sh process open fail ! ")

    time.sleep(1)

                
                
        
            


