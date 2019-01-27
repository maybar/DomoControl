#!/usr/bin/env python3


"""This module is the main module for Domo control project.
It contains two classes: DomoControlFrame and main_thread"""

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
import pyowm    #Open weather
from pyowm import timeutils
import constants as const
import psutil
import pytz

class DomoControlFrame(QtGui.QDialog):
    """This class docstring shows how to use sphinx and rst syntax

    The first line is brief explanation, which may be completed with 
    a longer one. For instance to discuss about its methods. The only
    method here is :func:`function1`'s. The main idea is to document
    the class and methods's arguments with 

    - **parameters**, **types**, **return** and **return types**::

          :param arg1: description
          :param arg2: description
          :type arg1: type description
          :type arg1: type description
          :return: return description
          :rtype: the return type description

    - and to provide sections such as **Example** using the double commas syntax::

          :Example:

          followed by a blank line !

      which appears as follow:

      :Example:

      followed by a blank line

    - Finally special sections such as **See Also**, **Warnings**, **Notes**
      use the sphinx syntax (*paragraph directives*)::

          .. seealso:: blabla
          .. warnings also:: blabla
          .. note:: blabla
          .. todo:: blabla

    .. note::
        There are many other Info fields but they may be redundant:
            * param, parameter, arg, argument, key, keyword: Description of a
              parameter.
            * type: Type of a parameter.
            * raises, raise, except, exception: That (and when) a specific
              exception is raised.
            * var, ivar, cvar: Description of a variable.
            * returns, return: Description of the return value.
            * rtype: Return type.

    .. note::
        There are many other directives such as versionadded, versionchanged,
        rubric, centered, ... See the sphinx documentation for more details.

    Here below is the results of the :func:`function1` docstring.

    """
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
        self.ui.icon_condition.setPixmap(QtGui.QPixmap(os.getcwd() + "/res/icon_weather.png"))
        self.ui.icon_condition.update()
        
        
    def showStatus(self, status):
        self.ui.label_weather_status.setText(status)
        self.ui.label_weather_status.update()
        
    
    def setTime(self,ahora):
        ''' Show the hour '''
        old_text=self.ui.label_hora.text()
        if old_text != ahora:
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
    """This class main_thread implements the main loop of the project

    This class is executed from a Thread

    :param QThread: Clase QThread

    """

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
        self.toggle = False
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
        self.location = "Usurbil,ES"
        self.cond_protection = True
        self.save_history = False
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
        except Exception as e:
            logging.critical('Error opening config file \n'+str(e))

        
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
        self.status_datos = {
            'temp1' : 25.0,
            'hum'   : 50.0,
            'mode'   : 'dia',
            'temp2'   : 21.0,
            'state'   : False,
            'time'  :   "00:00",
            'pir'   : False,
            'alarma'   : 1
        }
        self.status_log = tools.StatusLog(**self.status_datos)
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
        """ It stops the thread """
        self.stop()
        if not self.finished():
            self.wait()
    
    def _get_temp(self):
        """ 
        It reads the temperature 
        
        """
        #humidity, temperature = Adafruit_DHT.read_retry(11, const.PIN_SENSOR_TEMP)
        try:
            humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.DHT22, const.PIN_SENSOR_TEMP)
        except Exception as e:
            logging.critical("Error en librería de lectura de sensor \n"+str(e))
            
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
        """ Update the bar timer in the dialog GUI 
        
        Args:
            value: Number between 0 and self.max_time_caldera
        """
        self.myapp.setBarTimerValue(value)
    
    def _updateHeatterWidget(self,value):
        """ Update the Dialog GUI heatter widget """
        self.myapp.show_heater(value)
        
    def _updateWeatherText(self,value):
        """ Update the dialog GUI for the Weather panel"""
        self.myapp.showWeather(value)
        
    '''def _updateWeatherStatusText(self,value):
        """ Update the dialog GUI for the current Weather status"""
        self.myapp.showStatus(value)'''
        
    #   
    def _temperatureControl(self):
        ''' Implements the control function of temperature '''
        send_emomcms_data = False
        
        
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
        
        #anti condensation protection
        if self.cond_protection == True:
            if self.temp_external < 0 and self.temp_target > const.TEMP_TARGET_0:
                self.temp_target = const.TEMP_TARGET_0
            elif self.temp_external < 5 and self.temp_target > const.TEMP_TARGET_5:
                self.temp_target = const.TEMP_TARGET_5
            elif self.temp_external < 10 and self.temp_target > const.TEMP_TARGET_10:
                self.temp_target = const.TEMP_TARGET_10
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
                self._setLed('OFF')
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
            if self.toggle == True:
                self._setLed('GREEN')
                self.toggle = False
            else:
                self._setLed('OFF')
                self.toggle = True
        elif self.sm_caldera == "WAITING": 
            self._setLed('GREEN')
            caldera_enable = False
            self.myapp.ui.label_arm.setText("Desarmada. Espera: "+ tools.segToMin(int(self.timer_cycle_caldera.remainder()))) 
            if self.timer_cycle_caldera.expired() == True:
                self.myapp.ui.label_arm.setText("Sistema preparado")
                self.emit(QtCore.SIGNAL("_updateBarTimer(int)"),int(0)) 
                self.sm_caldera = "IDLE"
        else:
            pass
        
        #print (self.sm_caldera)
                 
          
        # -----------------------------------------------------
        
        # Cycle to read sensor --------------------------------------
        if self.timer_sensor.expired():
            #current_led_state = self._getLed()
            self._setLed('GREEN')
            old_temp=self.sensor_temp
            old_hum=self.sensor_humidity
            self._get_temp()
            # Write log on internet
            send_emomcms_data = True
            self._setLed('OFF')
                
                
            
         
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
            except Exception as e:
                logging.critical("EXCEPTION: self.radio_tx.put\n"+ str(e))
            if result == True:
                s="Tx radio: "+msg
                logging.info(s)
            else: 
                logging.error("Tx Error sending")
                
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
        """ Implements the movement detection function """
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
        ''' Send the data to Emoncms web server '''
        s = 'https://emoncms.org/input/post?node='+str(id)+'&fulljson={'+var_data+'}&apikey=9771b32a0de292aabb7f01cfdcad146b'
        #print("EmoncmsData: "+s)
        try:
            contents = urlopen(s).read()
        except Exception as e:
            logging.critical ("Error sending data to Emoncms\n"+str(e))
        #print("EmoncmsData "+contents)

    def _lightProcess(self):
        """ Read the LDR sensor """
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
        """ Show the external weather information """
        owm = pyowm.OWM('9aee4fb7c7506e85af9550c30c4ce886', language="es") 
        if ((self.timer_weather.expired() == True) and (owm.is_API_online())):
            # Search for current weather in City (country)
            observation = owm.weather_at_place(self.location)
            weather = observation.get_weather()
            location = observation.get_location()
            
            nombre_local_imagen_1 = os.getcwd() + "/res/icon_weather.png" # El nombre con el que queremos guardarla
            
            try:
                rich_text_weather = tools.HtmlText(10)
                rich_text_weather.add_text(location.get_name() +" - "+ "ES")
                local_reference_time = tools.utc_to_local(weather.get_reference_time(timeformat='date')).strftime('%d-%m-%Y %H:%M')
                rich_text_weather.add_text(local_reference_time)
                rich_text_weather.add_empty_line()
                rich_text_weather.add_title("Condiciones actuales:")
                rich_text_weather.add_text(weather.get_detailed_status())
                temp = weather.get_temperature(unit='celsius')
                self.temp_external = int(temp['temp'])
                rich_text_weather.add_text(str(temp['temp']) + " ºC  - " + str(weather.get_humidity()) + " %")
                rich_text_weather.add_text(str(temp['temp_max']) + "ºC / "+str(temp['temp_min']) + "ºC")
                wind = weather.get_wind(unit='meters_sec')
                wind_speed = ""
                wind_deg = ""
                if (len(wind) > 0):
                    wind_speed = str(wind['speed']) + " m/s"
                elif (len(wind) > 1):
                    wind_deg = " - "+str(wind['deg']) + " º"
                rich_text_weather.add_text(wind_speed + wind_deg)
                rain = weather.get_rain() 
                str_rain = "NA"
                if (len(rain) > 0):
                    str_rain = str(rain['1h']) + " mm"
                snow = weather.get_snow() 
                str_snow = "NA"
                if (len(snow) > 0):
                    str_snow = str(snow['1h']) + " mm"
                rich_text_weather.add_text("Lluvia: "+str_rain + " - "+"Nieve: "+str_snow)
                sr = weather.get_sunrise_time('date')
                str_sr = tools.utc_to_local(sr).strftime('%H:%M')

                ss = weather.get_sunset_time('date')
                str_ss = tools.utc_to_local(ss).strftime('%H:%M')
                rich_text_weather.add_text("Sol: "+str_sr  + " - "+str_ss)
                rich_text_weather.add_text("------------------------------------")
                rich_text_weather.add_title("Pronósticos:")
                
                # Forecasts
                forecaster = owm.three_hours_forecast(self.location)
                #
                
                # Tomorrow
                f = forecaster.get_forecast()
                date_tomorrow = timeutils.tomorrow() 
                cont = 0
                for weather_tomorrow in f:
                    reference_time = weather_tomorrow.get_reference_time('date')
                    if reference_time.day <= date_tomorrow.day and (cont < 8):
                        tt = weather_tomorrow.get_temperature(unit='celsius')
                        str_local_time_wt = tools.utc_to_local(weather_tomorrow.get_reference_time(timeformat='date')).strftime('%d %H:%M')
                        rich_text_weather.add_text(str_local_time_wt+" "+weather_tomorrow.get_status() + " "+str(tt['temp']) + "ºC")
                        cont = cont+1
                
                s = rich_text_weather.get_text()
                
                #Descargar imagen
                url_imagen = weather.get_weather_icon_url()  # El link de la imagen
                self.myapp.showStatus(weather.get_status())
                
                try:
                    urlretrieve(url_imagen, nombre_local_imagen_1)
                except Exception as e:
                    logging.error ("Error trying to retrieve the icon weather\n"+str(e))
                    
                    
            except Exception as e:
                logging.error ("Error trying to get Open weather data. \nERROR: " + str(e))
                print(str(e))
                s = "Sin datos meteorológicos OpenWeather!"
                if os.path.exists(nombre_local_imagen_1):
                    os.remove(nombre_local_imagen_1)
            
            self.emit(QtCore.SIGNAL("_updateWeatherText(PyQt_PyObject)"),s)
            

        
    def _setLed(self, state):
        ''' Method to control the led 
        \param state State the led (RED, GREEN, OFF)'''
        
        if state == "RED":
            GPIO.output(const.PIN_LED_A,True)
            GPIO.output(const.PIN_LED_B,False)
        elif state == "GREEN":
            GPIO.output(const.PIN_LED_A,False)
            GPIO.output(const.PIN_LED_B,True)
        else:
            GPIO.output(const.PIN_LED_A,False)
            GPIO.output(const.PIN_LED_B,False)
    
    def _getLed(self):
        A = GPIO.input(const.PIN_LED_A)
        B = GPIO.input(const.PIN_LED_B)
        if A == 1 and B == 0:
            return "RED"
        elif A == 0 and B == 1:
            return "GREEN"
        else:
            return "OFF"
            
    #   
    def _alarm_control(self):
        # Implements the alarm function
        return
    
    def _watchdogHandler(self):
        logging.critical ("Whoa! Watchdog expired. Holy heavens!")
        sys.exit()
        
    def _writeData(self):
        if self.save_history == False:
            return
        ''' Write data '''
        dataList = np.array([self.real_temp, self.sensor_temp,self.sensor_humidity, self.caldera, self.presence])
        self.data.write(dataList)
    
    def _writeStatusData(self):
        ''' Write status data '''
        if self.sm_caldera != "IDLE":
            self.status_datos['time']  = tools.segToMin(self.timer_heater_on.elapsed()) + " [m:s] ("+self.sm_caldera+")"
        else:
            self.status_datos['time']  = "00:00 [m:s] (IDLE)"

        self.status_datos['temp1'] = self.sensor_temp
        self.status_datos['hum']   = self.sensor_humidity
        self.status_datos['mode']   = self.mode
        self.status_datos['temp2']   = self.temp_target
        self.status_datos['state']   = self.caldera
        self.status_datos['pir']   = self.presence
        self.status_datos['alarma']   = 1
        
        ret = self.status_log.write(**self.status_datos)
        '''if ret == True:
            logging.info("Status data written in json file")'''
        
    def _writeConfig(self):
        if (self.timer_config.expired() == True):
            # Write configuration
            self.watchdog_counter += 1
            config_list = [self.mode,self.watchdog_counter]
            f = open ('config.pickle','wb')
            pickle.dump(config_list,f)
            f.close()
        

    def run(self):
        """ Run de main loop. 
        
            This is the endless method.
            * Read 3 times the temperature sensor
            * Create the signals to mannage the widgets:
                - _updateBarTimer
                - _updateHeatterWidget
                - _updateWeatherText
            * Endless loop:
                - self._temperatureControl
                - self._pirProcess
                - self._weather_process
                - self._writeData
                - self._writeStatusData
                - self._writeConfig
                
        """
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
            self._writeStatusData()
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
        """ Command the stop of the thread.
        
        self.stopped is set.
        """
        self.stopped = 1

def main():
    """ Main  function
    
    Raises:
        KeyboardInterrupt
    """
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
    except Exception as e:
        logging.info("except app.exec\n"+str(e))
        GPIO.cleanup() # this ensures a clean exit 
    finally:  
        #GPIO.cleanup() # this ensures a clean exit  
        mainThread.stop()
        logging.info("finally app.exec")


if __name__ == "__main__":
    """ Enter point """
    logging.basicConfig(filename=os.getcwd() +'/log/main.log',format='%(levelname)s:%(asctime)s %(message)s', datefmt='%d/%m %H:%M:%S', level=logging.WARNING)
    #logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s', datefmt='%d/%m %H:%M:%S', level=logging.DEBUG)
    
    
    main()
 


