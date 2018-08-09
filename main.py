#!/usr/bin/env python3
# -*- coding: Windows-1252 -*-
import os,sys
import numpy as np
import Adafruit_DHT
from MainDialog import *
from PyQt4.QtCore import QThread, Qt
import RPi.GPIO as GPIO
import time
import datetime
from urllib.request import urlopen
import tools
#RADIO communication
import piVirtualWire.piVirtualWire as piVirtualWire
import pigpio
from PyQt4.QtGui import (QColor, QPalette)
import pickle
#from apscheduler.schedulers.background import BackgroundScheduler
from PyQt4.QtGui import QApplication

#import logging

class DomoControlFrame(QtGui.QDialog):
    ''' .... '''
    def __init__(self,parent=None):
        ''' Constructor of DomoControlFrame '''
        QtGui.QWidget.__init__(self, parent)
        #Create the main dialog object
        self.ui = Ui_MainDialog()
        #Add controls
        self.ui.setupUi(self)
        self.ui.btn_alta.clicked.connect(self.modeAlta)
        self.ui.btn_baja.clicked.connect(self.modeBaja)
        self.ui.btn_auto.clicked.connect(self.modeAuto)
        self.ui.btn_apagado.clicked.connect(self.modeApagado)
        self.mode = "APAGADO"


    def show_temp_humi(self,humidity, temperature, temp_real):
        ''' Show the temperature and humidity in the LCD widgets '''
        self.ui.lcdTemp.display(temperature)
        self.ui.lcdTemp.update()
        self.ui.lcdHum.display(humidity)
        self.ui.lcdHum.update()
        self.ui.lcdTempReal.display(temp_real)
        self.ui.lcdTempReal.update()
 
    def setTempTarget(self,temperature):
        ''' Show the temperature target '''
        s = "T.Objetivo: "+str(temperature)+" ºC"
        #s = unicode(s, "utf-8")
        self.ui.label_temp_target.setText(s)

    def show_heater(self, control):
        ''' Show the icon of the heater '''
        if (control == True):
            self.ui.label_icon_casa.setPixmap(QtGui.QPixmap(os.getcwd() + "/res/heater_on.png"))
        else:
            self.ui.label_icon_casa.setPixmap(QtGui.QPixmap(os.getcwd() + "/res/heater_off.png"))
        self.ui.label_icon_casa.update()
    
    def showPirState(self,pir_state):
        ''' Show the PIR state '''
        if pir_state == True:
            self.ui.label_pir.setText("Presencia")
        else:
            self.ui.label_pir.setText("   -     ")

    def showLightValue(self,value):
        self.ui.label_light.setText("Iluminación: "+str(value)+"%")
    
    def setTime(self,ahora):
        ''' Show the hour '''
        self.ui.label_hora.setText(ahora)
    
    def setBarTimerMaximum(self,max):
        self.ui.barHeaterTimer.setMaximum(max)
        
    def setBarTimerValue(self,value):
        self.ui.barHeaterTimer.setValue(value)
        '''p = self.ui.barHeaterTimer.palette()
        p.setColor(QPalette.Highlight, QColor(Qt.red))
        self.ui.barHeaterTimer.setPalette(p)
        self.ui.barHeaterTimer.show()'''
        self.ui.barHeaterTimer.setStyleSheet("background:'red';")
        self.ui.barHeaterTimer.update()
        
    def modeAlta(self):
        self.mode = "T.ALTA"
            
    def modeBaja(self):
        self.mode = "T.BAJA"
    
    def modeAuto(self):
        self.mode = "AUTO"
        
    def modeApagado(self):
        self.mode = "APAGADO"

    def getMode(self):
        return self.mode


class main_thread(QThread):
    # Thread implementing the main loop 
    def __init__(self,myapp):
        # Constructor 
        #Important to avoid: QThread : Destroyed while thread is still running
        super(main_thread, self).__init__(myapp)
        
        # general Variables
        self.stopped = 0        
        self.myapp = myapp
        self.caldera = False #Indicates the caldera is switched off
        self.sensor_humidity = 50
        self.sensor_temp = 22;
        self.real_temp = 22
        self.num_read = 0
        self.num_failures = 0
        self.period_sensor = 60 #segundos
        self.period_ldr = 5 #segundos
        self.pir_state = False
        self.watchdog_counter = 0
        #------------------------------------------
        
        
        #CONFIG
        self.HIGH_TEMP = 21
        self.LOW_TEMP = 18
        self.OFF_TEMP = 10
        self.temp_target = self.OFF_TEMP
        self.mode = "APAGADO"   #  AUTO,T.ALTA,T.BAJA,APAGADO
        self.myapp.setTempTarget(self.temp_target)
        self.hora_start_high = datetime.time(7,0,0)
        self.hora_start_low = datetime.time(0,0,0)
        self.cycle_caldera = 15*60     #15 o 20 minutos
        self.max_time_caldera = 10*60     #10 min max time the caldera can be active
        self.tx_resend = 60 #Resend
        #-------------------------------------------
        try:
            f = open ('config.pickle','rb')
            config_list = pickle.load(f)
            f.close()
            self.mode = config_list[0]
            if config_list[0] == "AUTO":
                self.myapp.modeAuto()
            elif config_list[0] == "T.ALTA":
                self.myapp.modeAlta()
            elif config_list[0] == "T.BAJA":
                self.myapp.modeBaja()
            else:
                self.myapp.modeApagado()
                
            self.watchdog_counter = config_list[1]
        except:
            print ('Error opening config file')
        
        #-------------------------------------------
        #PINES
        self.pin_sensor_temp = 12
        self.pin_pir = 20
        self.pin_led_a = 6
        self.pin_led_b = 5
        self.pin_ldr_charge = 19
        self.pin_ldr_discharge = 13
        self.pin_tx = 14
        #self.pin_rx = 
        #-------------------------------------------

        
        #Config GPIO
        GPIO.setmode(GPIO.BCM)
        #configure the pin of PIR
        GPIO.setup(self.pin_pir,GPIO.IN)
        #configure the pines to control the bicolor led
        GPIO.setup(self.pin_led_a,GPIO.OUT)
        GPIO.setup(self.pin_led_b,GPIO.OUT)
        #configure the pines for light sensor
        GPIO.setup(self.pin_ldr_charge,GPIO.IN)
        GPIO.setup(self.pin_ldr_discharge,GPIO.IN) 
        GPIO.setup(self.pin_sensor_temp, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        #-------------------------------------------
        
        self.data = tools.DataLog("Tiempo,T.Real,T.Sensor,T.Humedad,Caldera")
        #self.data = open("data.csv", "w")
        self.temp_list = np.array([22.0,22.0,22.0])
        self.humi_list = np.array([50.0,50.0,50.0])
        
        #Timers
        self.timer_sensor = tools.Timer(self.period_sensor)
        #self.start_sensor_time=time.time()-self.period_sensor
        self.start_cycle_caldera = time.time()-self.cycle_caldera
        self.start_heater_on = time.time()-self.max_time_caldera
        self.start_ldr_time = time.time()-self.period_ldr
        self.timer_tx = tools.Timer(self.tx_resend)
        self.timer_config = tools.Timer(5)     #timer to write de config data
        #-----------------------------------------------
        
        self.myapp.show_temp_humi(self.sensor_humidity, self.sensor_temp, self.real_temp)
        self.myapp.setTempTarget(self.temp_target)
        self.myapp.setBarTimerMaximum(self.cycle_caldera)
        self.myapp.setBarTimerValue(self.cycle_caldera)
        self.myapp.show_heater(False)
        
        #Init RADIO Com
        self.pi = pigpio.pi()
        self.radio_tx = piVirtualWire.tx(self.pi, self.pin_tx, 2000) 
        
        
    def __del__(self):
        self.stop()
        if not self.finished():
            self.wait()
    
    def _get_temp(self):

        #humidity, temperature = Adafruit_DHT.read_retry(11, self.pin_sensor_temp)
        humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.AM2302, self.pin_sensor_temp)
        self.num_read+=1
        if humidity is not None and temperature is not None and humidity <= 100.0 and humidity >= 0.0:
            self.sensor_temp = round(temperature,1) #1 decimal
            self.sensor_humidity = round(humidity,1)
            self.sensor_temp =tools.getMedia(self.temp_list, temperature)
            #print self.temp_list[0],self.temp_list[1],self.temp_list[2],self.sensor_temp
            #self.sensor_humidity =tools.getMedia(self.humi_list, humidity)
            print (self.sensor_temp,self.sensor_humidity)
            self.real_temp = tools.get_real_temp(self.sensor_temp,self.sensor_humidity)
            #
            self.myapp.show_temp_humi(self.sensor_humidity, self.sensor_temp, self.real_temp)
        else:
            print ('Error lectura sensor DHT22')
##            logging.warning('Error lectura sensor DHT11')
            self.num_failures+=1
            
    def _updateBarTimer(self,value):
        self.myapp.setBarTimerValue(value)
    
    def _updateHeatterWidget(self,value):
        self.myapp.show_heater(value)
        
    #   
    def _temperatureControl(self):
        send_emomcms_data = False
        
        ''' Implements the control function of temperature '''
        ahora_tmp = datetime.datetime.now()
        ahora = datetime.time(ahora_tmp.hour,ahora_tmp.minute,ahora_tmp.second)
        self.myapp.setTime(str(ahora))
        
        # Calculate the target temperature -------------
        self.mode = self.myapp.getMode()
        temp_target = self.temp_target 
        if self.mode == "AUTO":
            if ahora >= self.hora_start_low and ahora < self.hora_start_high :
                self.temp_target = self.LOW_TEMP
            else:
                self.temp_target = self.HIGH_TEMP
        elif self.mode == "T.ALTA":
            self.temp_target = self.HIGH_TEMP
        elif self.mode == "T.BAJA":
            self.temp_target = self.LOW_TEMP
        else:
            self.temp_target = self.OFF_TEMP
            
        if self.temp_target != temp_target:
            self.myapp.setTempTarget(self.temp_target)
        # ------------------------------------------------
        
          
        #Cycle protection of heater -----------------------
        caldera_enable = True
        time_heater_on = time.time()-self.start_heater_on
        timer_protection = time.time()-self.start_cycle_caldera
        if self.caldera == True:
            if time_heater_on > self.max_time_caldera: 
                caldera_enable = False  # the heater was along time on
                self.myapp.ui.label_arm.setText("Desarmada!. Espera: "+ tools.segToMin(int(self.cycle_caldera-timer_protection)))
            else:
                caldera_enable = True   # heater keep enabled
                self.myapp.ui.label_arm.setText("Activada. Tiempo: "+ tools.segToMin(time_heater_on))
                #self.emit(QtCore.SIGNAL("_updateBarTimer(int)"),int(time_heater_on))
        else:
            if timer_protection > self.cycle_caldera:
                caldera_enable = True   # heater is enabled to be activated
                self.myapp.ui.label_arm.setText("Armada")
            else:
                caldera_enable = False   # heater have to wait to activa again
                self.myapp.ui.label_arm.setText("Desarmada. Espera: "+ tools.segToMin(int(self.cycle_caldera-timer_protection)))
                #self.emit(QtCore.SIGNAL("_updateBarTimer(int)"),int(timer_protection)+1)
         
          
        # -----------------------------------------------------
        
        # Cycle to read sensor --------------------------------------
        if self.timer_sensor.expired():
            old_temp=self.sensor_temp
            old_hum=self.sensor_humidity
            self._get_temp()
            # Write log on internet
            send_emomcms_data = True
         
        # Take decition to start the heater ------------------------------------------------------
        old_caldera = self.caldera
        if self.real_temp < self.temp_target and self.caldera == False and caldera_enable == True:
            #active caldera
            self.caldera = True
            self.start_heater_on = time.time()
            self.start_cycle_caldera = time.time()
            print ("Heater ON")
##            logging.info('Heater ON')
        if (self.real_temp >= self.temp_target or caldera_enable == False) and self.caldera == True:
            #disable caldera
            self.caldera = False
            print ("Heater OFF")
##            logging.info('Heater ON')
            
        # Command the heatter
        if old_caldera != self.caldera:
            self.timer_tx.expired_now()
            self.emit(QtCore.SIGNAL("_updateHeatterWidget(int)"),self.caldera)
            send_emomcms_data = True
        #-----------------------------------------------------
        
        # The command is periodically transmitted by the Radio
        if self.timer_tx.expired() == True:
            msg = "0001-OFF"
            if self.caldera == True:
                msg = "0001-ON_"
            result = self.radio_tx.put(msg)
            if result == True: 
                print ("Tx radio: "+msg)
            else: 
                print ("Tx Error sending")
        #-----------------------------------------------------
        
        ''' control the led '''
        if self.caldera == True:
            self._setLed('RED')
        else:
            self._setLed('GREEN')
        #---------------------------------------------------
        if send_emomcms_data == True:
            var_data = '"temp":'+str(self.sensor_temp) + "," + '"hum":'+str(self.sensor_humidity) + ","
            if self.caldera == True:
                var_data += '"heat":10'
            else:
                var_data += '"heat":0'
            self._putEmoncmsData(0,var_data)
            
    #   
    def _pirProcess(self):
        # Implements the movement detection function 
        old_pir_state = self.pir_state
        self.pir_state = GPIO.input(self.pin_pir)
        if old_pir_state != self.pir_state:
            self.myapp.showPirState(self.pir_state)
        return
    
    def _putEmoncmsData(self, id, var_data):
        s = 'https://emoncms.org/input/post?node='+str(id)+'&fulljson={'+var_data+'}&apikey=9771b32a0de292aabb7f01cfdcad146b'
        #print("EmoncmsData: "+s)
        try:
            contents = urlopen(s).read()
        except:
            print ("Error sending data to Emoncms")
        #print("EmoncmsData "+contents)

    def _lightProcess(self):
        ''' Read the LDR sensor '''
        if (time.time() - self.start_ldr_time) > self.period_ldr:
            #charge
            GPIO.setup(self.pin_ldr_discharge,GPIO.IN)
            GPIO.setup(self.pin_ldr_charge,GPIO.OUT)
            GPIO.output(self.pin_ldr_charge, True)
            t1=time.time()
            while not GPIO.input(self.pin_ldr_discharge):
                pass
            t2 = time.time()
            delta_us = (t2 -t1) * 1000000   #us
            #print delta_us 
            value = int(100.0 - (0.001 * int(delta_us)))
            self.myapp.showLightValue(value)
            self.start_ldr_time = time.time()
            
            #discharge
            GPIO.setup(self.pin_ldr_charge,GPIO.IN)
            GPIO.setup(self.pin_ldr_discharge,GPIO.OUT)
            GPIO.output(self.pin_ldr_discharge, False)
            
    
    def _setLed(self, state):
        if state == "RED":
            GPIO.output(self.pin_led_a,True)
            GPIO.output(self.pin_led_b,False)
        elif state == "GREEN":
            GPIO.output(self.pin_led_a,False)
            GPIO.output(self.pin_led_b,True)
        else:
            GPIO.output(self.pin_led_a,False)
            GPIO.output(self.pin_led_b,False)
            
    #   
    def _alarm_control(self):
        # Implements the alarm function
        return
    
    def _watchdogHandler(self):
        #print "Whoa! Watchdog expired. Holy heavens!"
        GPIO.output(self.pin_caldera,False) #stop caldera
        sys.exit()
        
    def _writeData(self):
        ''' Write data '''
        dataList = np.array([self.real_temp, self.sensor_temp,self.sensor_humidity, self.caldera])
        self.data.write(dataList)
        
    def _writeConfig(self):
        if (self.timer_config.expired() == True):
            # Write configuration
            self.watchdog_counter += 1
            config_list = [self.mode,self.watchdog_counter]
            f = open ('config.pickle','wb')
            pickle.dump(config_list,f)
            f.close()
        

    def run(self):
        print('Thread is started' )
##        watchdog = tools.Watchdog(60, self._watchdogHandler)
        #Start CONFIC scheduler --------------
        #scheduler = BackgroundScheduler()
        #scheduler.add_job(self._write_config, 'interval', seconds=5)
        #scheduler.start()
        #-------------------------------------------------------

        self._get_temp()
        time.sleep(2)
        self._get_temp()
        time.sleep(2)
        self._get_temp()
        time.sleep(2)
        #self.connect(self, QtCore.SIGNAL("_updateBarTimer(int)"),self._updateBarTimer)
        self.connect(self, QtCore.SIGNAL("_updateHeatterWidget(int)"),self._updateHeatterWidget)
        while not self.stopped:
            #self._rx_radio_process()
            self._temperatureControl()
            self._pirProcess()
            #self._lightProcess()
            #self._alarm_control()
##            watchdog.reset()
            self._writeData()
            self._writeConfig()
            time.sleep(0.5)
            QApplication.processEvents()    #to avoid freze the screen
            
            
        # ... Clean shutdown code here ...
        print('Thread is stopped' )
        GPIO.output(self.pin_caldera,False)
        self.data.close()
        GPIO.cleanup() # this ensures a clean exit 
        self.radio_tx.cancel()
        self.pi.stop()
            
    def stop(self):
        self.stopped = 1

def main():
        app = QtGui.QApplication(sys.argv)
        myapp = DomoControlFrame()
        myapp.showFullScreen()
        #myapp.show()
        
##        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
##        logging.basicConfig(filename='main.log',level=logging.DEBUG)
        
        ''' Main Loop '''
        try:    
            mainThread = main_thread(myapp)
            mainThread.start()
        except KeyboardInterrupt:
              print ("KeyboardInterrupt")  
##        except:
##            print ("Error starting the Main thread")

        
        try:
            sys.exit(app.exec_())
        except:
            print ("except app.exec")
            GPIO.cleanup() # this ensures a clean exit 
        finally:  
            #GPIO.cleanup() # this ensures a clean exit  
            mainThread.stop()
            print ("finally app.exec")




if __name__ == "__main__":
    main()
 


