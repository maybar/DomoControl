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
from urllib.request import urlopen, urlretrieve
import tools
#RADIO communication
import piVirtualWire.piVirtualWire as piVirtualWire
import pigpio
from PyQt4.QtGui import (QColor, QPalette)
import pickle
from PyQt4.QtGui import QApplication, QMessageBox

import logging
from weather import Weather, Unit
import constants as const
import psutil

class DomoControlFrame(QtGui.QDialog):
    ''' .... '''
    def __init__(self,parent=None):
        ''' Constructor of DomoControlFrame '''
        QtGui.QWidget.__init__(self, parent)
        #Create the main dialog object
        self.ui = Ui_MainDialog()
        #Add controls
        self.ui.setupUi(self)
        self.ui.btn_alta.setEnabled(True)
        self.ui.btn_baja.setEnabled(True)
        self.ui.btn_auto.setEnabled(True)
        self.ui.btn_apagado.setEnabled(True)
        self.ui.btn_alta.clicked.connect(self.modeAlta)
        self.ui.btn_baja.clicked.connect(self.modeBaja)
        self.ui.btn_auto.clicked.connect(self.modeAuto)
        self.ui.btn_apagado.clicked.connect(self.modeApagado)
        self.ui.btn_test.clicked.connect(self.test)
        self.mode = "APAGADO"
        self.old_bar_timer_value = 99


    def show_temp_humi(self,humidity, temperature):
        ''' Show the temperature and humidity in the LCD widgets '''
        self.ui.lcdTemp.display(temperature)
        self.ui.lcdTemp.update()
        self.ui.lcdHum.display(humidity)
        self.ui.lcdHum.update()
        #self.ui.lcdTempReal.display(temp_real)
        #self.ui.lcdTempReal.update()
 
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
            #print ("Presencia")
        else:
            self.ui.label_pir.setText("   -     ")
            #print ("No Presencia")

    def showLightValue(self,value):
        self.ui.label_light.setText("Iluminación: "+str(value)+"%")
        
    def showWeather(self, rich_text):
        self.ui.text_weather.setHtml(rich_text)
        self.ui.text_weather.update()
        self.ui.icon_condition.setPixmap(QtGui.QPixmap(os.getcwd() + "/res/icon_weather.gif"))
        self.ui.icon_condition.update()
        self.ui.icon_condition_2.setPixmap(QtGui.QPixmap(os.getcwd() + "/res/icon_weather2.gif"))
        self.ui.icon_condition_2.update()
    
    def setTime(self,ahora):
        ''' Show the hour '''
        self.ui.label_hora.setText(ahora)
    
    def setBarTimerMaximum(self,max):
        self.ui.barHeaterTimer.setMaximum(max)
        
    def setBarTimerValue(self,value):
        if self.old_bar_timer_value != value:
            self.ui.barHeaterTimer.setValue(value)
##            p = self.ui.barHeaterTimer.palette()
##            p.setColor(QPalette.Highlight, QColor(Qt.red))
##            self.ui.barHeaterTimer.setPalette(p)
            self.ui.barHeaterTimer.show()
            #self.ui.barHeaterTimer.setStyleSheet("background:'red';")
            self.ui.barHeaterTimer.update()
            self.old_bar_timer_value = value
            
            
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
    
    def test(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        p = psutil.Process()
        pid = os.getpid()
        ST = p.status()
        msg.setWindowTitle("Test MessageBox")
        msg.setText("Process status: "+ST+"\n"+"PID: "+str(pid))
        #msg.setInformativeText("This is additional information")
        
        #msg.setDetailedText(s)
 
        #msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        #msg.buttonClicked.connect(msgbtn)
        
        retval = msg.exec_()


class main_thread(QThread):
    ''' Thread implementing the main loop '''

    def __init__(self,myapp):
        ''' Constructor '''
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
        self.presence = False
        self.watchdog_counter = 0
        self.temp_external = 22
        self.sm_caldera = "IDLE"  #state machine for heater protection
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
        self.location = "Usurbil"
        self.cond_protection = True
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
            logging.error('Error opening config file')

        
        #Config GPIO
        GPIO.setmode(GPIO.BCM)
        #configure the pin of PIR
        GPIO.setup(const.PIN_PIR, GPIO.IN)
        #configure the pines to control the bicolor led
        GPIO.setup(const.PIN_LED_A,GPIO.OUT)
        GPIO.setup(const.PIN_LED_B,GPIO.OUT)
        #configure the pines for light sensor
        GPIO.setup(const.PIN_LDR_CHARGE,GPIO.IN)
        GPIO.setup(const.PIN_LDR_DISCHARGE, GPIO.IN) 
        GPIO.setup(const.PIN_SENSOR_TEMP, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        #-------------------------------------------
        
        self.data = tools.DataLog("Tiempo,T.Real,T.Sensor,T.Humedad,Caldera, Presence")
        self.temp_list = np.array([22.0,22.0,22.0])
        self.humi_list = np.array([50.0,50.0,50.0])
        
        #Timers
        self.timer_sensor = tools.Timer(self.period_sensor)
        self.timer_cycle_caldera = tools.Timer(self.cycle_caldera, tools.Timer.ONE_SHOT)
        self.timer_heater_on = tools.Timer(self.max_time_caldera, tools.Timer.ONE_SHOT)
        self.start_ldr_time = time.time()-self.period_ldr
        self.timer_tx = tools.Timer(const.TX_RESEND, 3) #3 times
        self.timer_config = tools.Timer(5)     #timer to write de config data
        self.timer_pir = tools.Timer(50)
        self.timer_weather = tools.Timer(900) #update each 15 min
        #self.timer_one_sec = tools.Timer(1)
        #-----------------------------------------------
        
        self.myapp.show_temp_humi(self.sensor_humidity, self.sensor_temp)
        self.myapp.setTempTarget(self.temp_target)
        self.myapp.setBarTimerMaximum(self.max_time_caldera)
        self.myapp.setBarTimerValue(0)
        self.myapp.show_heater(False)
        self.myapp.ui.label_arm.setText("Sistema preparado")
        
        #Init RADIO Com
        self.pi = pigpio.pi()
        self.radio_tx = piVirtualWire.tx(self.pi, const.PIN_TX, 2000) 

        
    def __del__(self):
        self.stop()
        if not self.finished():
            self.wait()
    
    def _get_temp(self):
        #humidity, temperature = Adafruit_DHT.read_retry(11, const.PIN_SENSOR_TEMP)
        humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.DHT22, const.PIN_SENSOR_TEMP)
        self.num_read+=1
        if humidity is not None and temperature is not None and humidity <= 100.0 and humidity >= 0.0:
            #redondear
            self.sensor_temp = round(temperature,1) #1 decimal
            self.sensor_humidity = round(humidity,1)
            
            #Compensate the error in temperature
            self.sensor_temp = self.sensor_temp - 2.2
            
            #media
            self.sensor_temp =tools.getMedia(self.temp_list, self.sensor_temp)
            #print self.temp_list[0],self.temp_list[1],self.temp_list[2],self.sensor_temp
            #print (self.sensor_temp,self.sensor_humidity)
            #self.real_temp = tools.get_real_temp(self.sensor_temp,self.sensor_humidity)
            self.real_temp = self.sensor_temp;
            #
            self.myapp.show_temp_humi(self.sensor_humidity, self.sensor_temp)
        else:
            logging.warning('Error lectura sensor DHT11')
            self.num_failures+=1
            
    def _updateBarTimer(self,value):
        self.myapp.setBarTimerValue(value)
    
    def _updateHeatterWidget(self,value):
        self.myapp.show_heater(value)
        
    def _updateWeatherText(self,value):
        self.myapp.showWeather(value)
        
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
        
        #protection
        if self.cond_protection == True:
            if self.temp_external < 0 and self.temp_target > 18:
                self.temp_target = 18
            elif self.temp_external < 5 and self.temp_target > 19:
                self.temp_target = 19
            elif self.temp_external < 10 and self.temp_target > 20:
                self.temp_target = 20
            else:
                pass
        # --------------------------------------------------------
        
        #
        if self.temp_target != temp_target:
            self.myapp.setTempTarget(self.temp_target)
        # ------------------------------------------------
        
          
        # State machine protection of heater -----------------------
        caldera_enable = True
        if self.sm_caldera == "IDLE":
            if self.caldera == True:
                self.timer_heater_on.restart()
                self.timer_cycle_caldera.restart()
                self.sm_caldera = "WORKING"
                #print ("Caldera se activó -> WORKING")
        elif self.sm_caldera == "WORKING":
            time_heater_on = self.timer_heater_on.elapsed()
            self.myapp.ui.label_arm.setText("Activada. Tiempo: "+ tools.segToMin(time_heater_on))
            self.emit(QtCore.SIGNAL("_updateBarTimer(int)"),int(time_heater_on))
            if self.timer_heater_on.expired() == True: 
                self.emit(QtCore.SIGNAL("_updateBarTimer(int)"),int(self.max_time_caldera))
                self.sm_caldera = "WAITING"
                #print ("Temporizador1 expiró. Espera")
            if self.caldera == False:
                self.sm_caldera = "WAITING"
                #print ("Caldera se apagó. Espera")
        elif self.sm_caldera == "WAITING": 
            caldera_enable = False
            self.myapp.ui.label_arm.setText("Desarmada. Espera: "+ tools.segToMin(int(self.timer_cycle_caldera.remainder()))) 
            if self.timer_cycle_caldera.expired() == True:
                self.myapp.ui.label_arm.setText("Sistema preparado")
                self.emit(QtCore.SIGNAL("_updateBarTimer(int)"),int(0)) 
                self.sm_caldera = "IDLE"
                #print ("Temporizador2 expiró. pasa a Idle")
        else:
            pass
        
        #print (self.sm_caldera)
                 
          
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
            logging.info('Heater ON')
        if (self.real_temp >= self.temp_target or caldera_enable == False) and self.caldera == True:
            #disable caldera
            self.caldera = False
            logging.info('Heater OFF')
            
        # Command the heatter
        if old_caldera != self.caldera:
            self.timer_tx.restart()
            self.emit(QtCore.SIGNAL("_updateHeatterWidget(int)"),self.caldera)
            send_emomcms_data = True
        #-----------------------------------------------------
        
        # The command is periodically transmitted by the Radio
        if self.timer_tx.expired() == True:
            msg = "0001-OFF"
            if self.caldera == True:
                msg = "0001-ON_"
            result = False
            try:
                result = self.radio_tx.put(msg)
            except:
                logging.error("EXCEPTION: self.radio_tx.put")
            if result == True:
                s="Tx radio: "+msg
                logging.info(s)
            else: 
                logging.error("Tx Error sending")
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
        old_presence = self.presence
        old_pir_state = self.pir_state
        new_pir_state = GPIO.input(const.PIN_PIR)
        #print(old_pir_state, new_pir_state)
        if (old_pir_state == False) and (new_pir_state == 1):
            #print ("restart up")
            self.timer_pir.start(40)
        if (new_pir_state == True) and (self.timer_pir.expired()):
            self.presence = True
        if (old_pir_state == True) and (new_pir_state == 0):
            #print ("restart down")
            self.timer_pir.start(20)
        if (new_pir_state == False) and (self.timer_pir.expired()):
            self.presence = False
            
        if old_presence != self.presence:
            self.myapp.showPirState(self.presence)
          
        self.pir_state =  new_pir_state; 
        return
    
    def _putEmoncmsData(self, id, var_data):
        s = 'https://emoncms.org/input/post?node='+str(id)+'&fulljson={'+var_data+'}&apikey=9771b32a0de292aabb7f01cfdcad146b'
        #print("EmoncmsData: "+s)
        try:
            contents = urlopen(s).read()
        except:
            logging.error ("Error sending data to Emoncms")
        #print("EmoncmsData "+contents)

    def _lightProcess(self):
        ''' Read the LDR sensor '''
        if (time.time() - self.start_ldr_time) > self.period_ldr:
            #charge
            GPIO.setup(const.PIN_LDR_DISCHARGE, GPIO.IN)
            GPIO.setup(const.PIN_LDR_CHARGE,GPIO.OUT)
            GPIO.output(const.PIN_LDR_CHARGE, True)
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
            GPIO.setup(const.PIN_LDR_CHARGE,GPIO.IN)
            GPIO.setup(const.PIN_LDR_DISCHARGE, GPIO.OUT)
            GPIO.output(const.PIN_LDR_DISCHARGE, False)
            
    def _weather_process(self):
        '''Show the external weather information''' 
        if (self.timer_weather.expired() == True):
            weather = Weather(unit=Unit.CELSIUS)
            location = weather.lookup_by_location(self.location)
            condition = location.condition
            forecasts = location.forecast
            s = tools.getRichTextWeather(location, condition, forecasts)
            self.temp_external = int(condition.temp)
            #Descargar imagen
            url_imagen = "http://l.yimg.com/a/i/us/we/52/"+condition.code+".gif" # El link de la imagen
            nombre_local_imagen = os.getcwd() + "/res/icon_weather.gif" # El nombre con el que queremos guardarla
            try:
                urlretrieve(url_imagen, nombre_local_imagen)
            except:
                logging.error ("Error trying to retrieve the icon weather")
            self.emit(QtCore.SIGNAL("_updateWeatherText(PyQt_PyObject)"),s)
            
            #Descargar imagen pronostico para mañana
            url_imagen2 = "http://l.yimg.com/a/i/us/we/52/"+forecasts[1].code+".gif" # El link de la imagen
            #print(url_imagen2)
            nombre_local_imagen = os.getcwd() + "/res/icon_weather2.gif" # El nombre con el que queremos guardarla
            try:
                urlretrieve(url_imagen2, nombre_local_imagen)
            except:
                logging.error ("Error trying to retrieve the icon weather2")

        
    def _setLed(self, state):
        if state == "RED":
            GPIO.output(const.PIN_LED_A,True)
            GPIO.output(const.PIN_LED_B,False)
        elif state == "GREEN":
            GPIO.output(const.PIN_LED_A,False)
            GPIO.output(const.PIN_LED_B,True)
        else:
            GPIO.output(const.PIN_LED_A,False)
            GPIO.output(const.PIN_LED_B,False)
            
    #   
    def _alarm_control(self):
        # Implements the alarm function
        return
    
    def _watchdogHandler(self):
        logging.critical ("Whoa! Watchdog expired. Holy heavens!")
        GPIO.output(self.pin_caldera,False) #stop caldera
        sys.exit()
        
    def _writeData(self):
        ''' Write data '''
        dataList = np.array([self.real_temp, self.sensor_temp,self.sensor_humidity, self.caldera, self.presence])
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
        logging.info('Thread is started' )
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
        self.connect(self, QtCore.SIGNAL("_updateBarTimer(int)"),self._updateBarTimer)
        self.connect(self, QtCore.SIGNAL("_updateHeatterWidget(int)"),self._updateHeatterWidget)
        self.connect(self, QtCore.SIGNAL("_updateWeatherText(PyQt_PyObject)"),self._updateWeatherText)
        while not self.stopped:
            '''try:'''
            #self._rx_radio_process()
            self._temperatureControl()
            self._pirProcess()
            self._weather_process()
            #self._lightProcess()
            #self._alarm_control()
##              watchdog.reset()
            self._writeData()
            self._writeConfig()
            time.sleep(0.5)
            QApplication.sendPostedEvents()    #to avoid freze the screen
            '''except:
                logging.critical('Error loop run')'''
            
            
        # ... Clean shutdown code here ...
        logging.info('Thread is stopped' )
        self.data.close()
        GPIO.cleanup() # this ensures a clean exit 
        self.radio_tx.cancel()
        self.pi.stop()
            
    def stop(self):
        self.stopped = 1

def main():
        logging.info("MAIN Function")
        app = QtGui.QApplication(sys.argv)
        myapp = DomoControlFrame()
        myapp.showFullScreen()
        #myapp.show()
        
        ''' Main Loop '''
        try:    
            mainThread = main_thread(myapp)
            mainThread.start()
        except KeyboardInterrupt:
              logging.info("KeyboardInterrupt")  
##        except:
##            print ("Error starting the Main thread")

        
        try:
            sys.exit(app.exec_())
        except:
            logging.info("except app.exec")
            GPIO.cleanup() # this ensures a clean exit 
        finally:  
            #GPIO.cleanup() # this ensures a clean exit  
            mainThread.stop()
            logging.info("finally app.exec")


if __name__ == "__main__":
    #logging.basicConfig(filename='log/main.log',format='%(levelname)s:%(asctime)s %(message)s', datefmt='%d/%m %H:%M:%S', level=logging.DEBUG)
    logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s', datefmt='%d/%m %H:%M:%S', level=logging.DEBUG)
    
    
    main()
 


