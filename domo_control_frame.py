# -*- coding: utf-8 -*-

import os,sys
from MainDialog import *
from PyQt4.QtGui import QMessageBox
import psutil

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
        #debug
        self.id_function = 0
        self.watchdog_counter = 0

    def set_debug_data(self, _id, counter):
        self.id_function = _id
        self.watchdog_counter = counter

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
    
    def setBarTimerMaximum(self,_max):
        self.ui.barHeaterTimer.setMaximum(_max)
        
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
        s = "ID Function: " +str(self.id_function)+"\n"
        s += "Watchdog counter: "+ str(self.watchdog_counter) +"\n"
        msg.setDetailedText(s)
 
        #msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        #msg.buttonClicked.connect(msgbtn)
        
        #retval = msg.exec_()

