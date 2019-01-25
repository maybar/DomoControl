"""This module contains several classes useful for domotic proyects."""

import Grid
import numpy as np
import datetime
import time
import smtplib
import json


#Tabla for Bochorno termico
humiNames = ['0','5','10','15','20','25','30','35','40','45','50','55','60','65','70','75','80','85','90','95','100']
tempNames = [20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
rawData = [ 16,16,17,17,17,18,18,19,19,19,19,19,20,20,20,21,21,21,21,21,21, \
            18,18,18,19,19,19,19,19,20,20,20,20,21,21,21,22,22,22,22,22,23, \
            19,19,19,20,20,20,20,20,21,21,21,21,22,22,22,22,23,23,23,23,24, \
            20,20,20,20,21,21,22,22,22,23,23,23,23,24,24,24,24,24,24,25,25, \
            21,21,22,22,22,22,23,23,23,24,24,24,24,25,25,25,25,26,26,26,26, \
            22,23,23,23,24,24,24,24,24,24,25,25,25,26,26,26,27,27,27,28,28, \
            24,24,24,24,25,25,25,26,26,26,26,27,27,27,27,28,28,29,29,29,30, \
            25,25,25,25,26,26,26,27,27,27,27,28,28,29,29,30,30,31,31,31,33, \
            26,26,26,26,27,27,27,28,28,28,29,29,29,30,31,32,32,33,34,34,36, \
            26,26,27,27,27,28,29,29,29,29,30,30,31,33,33,34,35,35,37,38,40, \
            27,27,28,28,28,28,29,29,30,30,31,32,33,34,35,36,37,39,40,41,45, \
            28,28,29,29,29,29,30,31,31,31,33,34,35,36,37,39,40,41,45,45,50, \
            29,29,29,29,30,31,33,33,34,34,35,35,37,39,40,42,44,45,51,51,55, \
            29,29,30,30,31,33,33,34,34,35,36,38,39,42,43,45,49,49,53,54,55, \
            30,30,31,31,32,34,34,35,36,37,38,41,42,44,47,48,50,52,55,99,99, \
            31,32,32,32,33,35,35,37,37,40,40,44,45,47,51,52,55,99,99,99,99, \
            32,33,33,34,35,36,37,39,39,42,43,46,49,50,54,55,99,99,99,99,99, \
            32,33,34,35,36,38,38,41,41,44,46,49,51,55,99,99,99,99,99,99,99, \
            33,34,35,36,37,39,40,43,44,47,49,51,55,99,99,99,99,99,99,99,99, \
            34,35,36,37,38,41,41,44,46,50,50,55,99,99,99,99,99,99,99,99,99, \
            35,36,37,39,40,43,43,47,49,53,55,99,99,99,99,99,99,99,99,99,99, \
            35,36,38,40,41,44,45,49,50,55,99,99,99,99,99,99,99,99,99,99,99, \
            36,37,39,41,42,45,47,50,52,55,99,99,99,99,99,99,99,99,99,99,99, \
            37,38,40,42,44,47,49,53,55,99,99,99,99,99,99,99,99,99,99,99,99, \
            38,39,41,44,45,49,52,55,99,99,99,99,99,99,99,99,99,99,99,99,99, \
            38,40,42,45,47,50,54,55,99,99,99,99,99,99,99,99,99,99,99,99,99 ]
indices = [ (row, col) for col in tempNames for row in humiNames ]
data = Grid.Grid(humiNames, tempNames, zip(indices, rawData))

def bochorno_get_temp(tempDeseada, s_humedad):
    for temp in tempNames:
        bocho = data[s_humedad,temp]
        if bocho == 99:
            return tempDeseada
        if data[s_humedad,temp] >= tempDeseada:
            return temp;

def get_real_temp(temp, humedad):
    temp_salida = temp
    temp = round(temp)
    decimal = temp_salida - temp
    humedad = round(humedad)
    if humedad > 100:
        return temp
    
    s_humedad = str(humedad)
    for humi_item in humiNames:
        if humedad <= int(humi_item):
            s_humedad = humi_item;
            break
    found=False
    # check if it's included in the list
    for temp_item in tempNames:
        if temp_item == temp:
            found = True
            break;
    if found == True:
        temp_salida = data[s_humedad,temp]
        temp_salida = temp_salida+decimal
        
    return temp_salida
    
def segToMin(inputSeg):
    local_minu=int(inputSeg/60)
    local_seg =int(inputSeg-(local_minu*60))
    return str(local_minu)+":"+str(local_seg)
        
def getMedia(lista,newValue):
    # Array processing to avoid resolution error
    #rotar valores
    lista[2] = lista[1]
    lista[1] = lista[0]
    lista[0] = newValue
    suma = (lista[0]+lista[1]+lista[2])
    cocie = suma / 3.0
    salida = round(cocie,1)
    return salida

def getRichTextWeather(observation, w3, wt):
    w = observation.get_weather()
    location = observation.get_location()
    t = w.get_temperature(unit='celsius')
    wind = w.get_wind(unit='meters_sec')
    rain = w.get_rain() 
    str_rain = "NA"
    if (len(rain) > 0):
        str_rain = str(rain['1h']) + " mm"
    snow = w.get_snow() 
    str_snow = "NA"
    if (len(snow) > 0):
        str_snow = str(snow['1h']) + " mm"
        
    sr = w.get_sunrise_time('iso')
    str_sr = sr[11:16]
    ss = w.get_sunset_time('iso')
    str_ss = ss[11:16]
    
    t3 = w3.get_temperature(unit='celsius')
    tt = wt.get_temperature(unit='celsius')
    
    h1 = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"> \
    <html><head><meta name="qrichtext" content="1" /><style type="text/css"> \
    p, li { white-space: pre-wrap; } \
    </style></head><body style=" font-family:''Ubuntu Condensed''; font-size:9pt; font-weight:400; font-style:normal;">'

    s1 = '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''Ubuntu'';">'
    s2 = '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:''Ubuntu'';"><br /></p>'
    s3 = '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''Ubuntu''; font-weight:600;">'
    s = h1 \
    +s1+location.get_name() +" - "+ "ES" + "</span></p>" \
    +s1+w.get_reference_time(timeformat='iso')  + "</span></p>" \
    +s2 \
    +s3+"Condiciones actuales:"+ "</span></p>" \
    +s1+w.get_detailed_status() + "</span></p>" \
    +s1+str(t['temp']) + " ºC  - " + str(w.get_humidity()) + " %</span></p>" \
    +s1+str(t['temp_max']) + "ºC / "+str(t['temp_min']) + "ºC"+"</span></p>" \
    +s1+str(wind['speed']) + " m/s  -  "+ str(wind['deg']) + " º"+"</span></p>" \
    +s1+"Lluvia: "+str_rain + " - "+"Nieve: "+str_snow + "</span></p>" \
    +s1+"Sol: "+str_sr  + " - "+str_ss + "</span></p>"\
    +s1+"------------------------------------"+ "</span></p>" \
    +s3+"Pronosticos:"+ "</span></p>" \
    +s1+(w3.get_reference_time(timeformat='iso'))[8:16]+","+w3.get_detailed_status() + ","+str(t3['temp_max']) + "ºC / "+str(t3['temp_min']) + "ºC"+"</span></p>"  \
    +s1+(wt.get_reference_time(timeformat='iso'))[8:16]+","+wt.get_status() + ","+str(tt['temp_max']) + "ºC / "+str(tt['temp_min']) + "ºC"+"</span></p>"  \
    +s2 \
    +s1+"------------------------------------"+ "</span></p>" 
    return s

from threading import Timer

class Watchdog:
    def __init__(self, timeout, userHandler=None):  # timeout in seconds
        self.timeout = timeout
        self.handler = userHandler if userHandler is not None else self.defaultHandler
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def defaultHandler(self):
        raise self
  
class DataLog:
    def __init__(self, header):  # name of the file
        self.file = open("log/DataLog-"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+".csv", "w")
        self.file.write(header+'\n')
        self.old_data = np.array([0,0,0,0,0])

    def write(self, data):
        if np.array_equal(self.old_data,data) == True:
            return 
        
        s = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ","+ str(data[0])+","+ str(data[1])+ ","+ str(data[2])+ ","+ str(data[3])+","+ str(data[4])+'\n'
        self.file.write(s)
        self.old_data = data
        
    def close(self):
        self.file.close()
        
class StatusLog:
    
    def __init__(self, **datos):  # name of the file
        self.old_data = datos

    def write(self, **data):
        ret = False
        if json.dumps(data) != json.dumps(self.old_data):
            with open('log/status.json', 'w') as file:
                json.dump(data, file)
            
            self.old_data = data
            ret = True
        return ret
        
        

class Timer:
    PERIODIC = 0
    ONE_SHOT = 1
    
    def __init__(self): 
        self.cycle = 0
        self.num_cycles = 0
        self.counter = long(0)
        
    def __init__(self, cycle, num_cycles = 0):  
        """ Constructor of the Timer class
        
        Arg:
            cycle: the period in seconds of the timer cycle
            num_cycles: the number of cycles on the timer (default 0: means run eternally)
        
        """
        self.cycle = cycle
        self.num_cycles = num_cycles
        self.counter = 0
        self.expired_now()

    def expired(self):
        result = False
        if (time.time()-self.start_time) > self.cycle:
            if (self.num_cycles == 0) or (self.counter <= self.num_cycles):
                self.start_time = time.time()
                self.counter = self.counter +1
            result = True
        if (self.num_cycles > 0) and (self.counter > self.num_cycles):
            result = False
        return result
    
    def expired_now(self):
        self.start_time = time.time()-self.cycle
        
    def restart(self):
        self.start_time = time.time()
        self.counter = 0
    
    def start(self, cycle, num_cycles = 0):
        self.cycle = cycle
        self.num_cycles = num_cycles
        self.counter = 0
        self.start_time = time.time()
    
        
    def elapsed(self):
        return time.time()-self.start_time
    
    def remainder(self):
        return self.start_time + self.cycle - time.time()
    
             
    
    
    
    
