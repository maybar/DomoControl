# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainDialog.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainDialog(object):
    def setupUi(self, MainDialog):
        MainDialog.setObjectName(_fromUtf8("MainDialog"))
        MainDialog.resize(800, 480)
        MainDialog.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.lcdTemp = QtGui.QLCDNumber(MainDialog)
        self.lcdTemp.setGeometry(QtCore.QRect(250, 50, 121, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lcdTemp.setFont(font)
        self.lcdTemp.setFrameShape(QtGui.QFrame.Panel)
        self.lcdTemp.setFrameShadow(QtGui.QFrame.Sunken)
        self.lcdTemp.setLineWidth(4)
        self.lcdTemp.setSmallDecimalPoint(True)
        self.lcdTemp.setNumDigits(4)
        self.lcdTemp.setObjectName(_fromUtf8("lcdTemp"))
        self.label_temp = QtGui.QLabel(MainDialog)
        self.label_temp.setGeometry(QtCore.QRect(380, 60, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_temp.setFont(font)
        self.label_temp.setObjectName(_fromUtf8("label_temp"))
        self.lcdHum = QtGui.QLCDNumber(MainDialog)
        self.lcdHum.setGeometry(QtCore.QRect(250, 130, 71, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lcdHum.setFont(font)
        self.lcdHum.setFrameShape(QtGui.QFrame.Panel)
        self.lcdHum.setFrameShadow(QtGui.QFrame.Sunken)
        self.lcdHum.setLineWidth(4)
        self.lcdHum.setSmallDecimalPoint(True)
        self.lcdHum.setNumDigits(4)
        self.lcdHum.setObjectName(_fromUtf8("lcdHum"))
        self.label_hum = QtGui.QLabel(MainDialog)
        self.label_hum.setGeometry(QtCore.QRect(330, 130, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_hum.setFont(font)
        self.label_hum.setObjectName(_fromUtf8("label_hum"))
        self.label_icon_casa = QtGui.QLabel(MainDialog)
        self.label_icon_casa.setGeometry(QtCore.QRect(320, 160, 141, 131))
        self.label_icon_casa.setText(_fromUtf8(""))
        self.label_icon_casa.setPixmap(QtGui.QPixmap(_fromUtf8("res/heater_off.png")))
        self.label_icon_casa.setAlignment(QtCore.Qt.AlignCenter)
        self.label_icon_casa.setObjectName(_fromUtf8("label_icon_casa"))
        self.frame = QtGui.QFrame(MainDialog)
        self.frame.setGeometry(QtCore.QRect(10, 60, 121, 181))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.btn_config = QtGui.QPushButton(self.frame)
        self.btn_config.setEnabled(False)
        self.btn_config.setGeometry(QtCore.QRect(10, 100, 99, 61))
        self.btn_config.setObjectName(_fromUtf8("btn_config"))
        self.btn_alarm = QtGui.QPushButton(self.frame)
        self.btn_alarm.setEnabled(False)
        self.btn_alarm.setGeometry(QtCore.QRect(10, 20, 99, 61))
        self.btn_alarm.setObjectName(_fromUtf8("btn_alarm"))
        self.label_temp_target = QtGui.QLabel(MainDialog)
        self.label_temp_target.setGeometry(QtCore.QRect(10, 10, 131, 31))
        self.label_temp_target.setFrameShape(QtGui.QFrame.Panel)
        self.label_temp_target.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_temp_target.setObjectName(_fromUtf8("label_temp_target"))
        self.label_pir = QtGui.QLabel(MainDialog)
        self.label_pir.setGeometry(QtCore.QRect(150, 10, 101, 31))
        self.label_pir.setFrameShape(QtGui.QFrame.Panel)
        self.label_pir.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_pir.setObjectName(_fromUtf8("label_pir"))
        self.label_alarm = QtGui.QLabel(MainDialog)
        self.label_alarm.setGeometry(QtCore.QRect(400, 10, 151, 31))
        self.label_alarm.setFrameShape(QtGui.QFrame.Panel)
        self.label_alarm.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_alarm.setObjectName(_fromUtf8("label_alarm"))
        self.label_light = QtGui.QLabel(MainDialog)
        self.label_light.setGeometry(QtCore.QRect(260, 10, 131, 31))
        self.label_light.setFrameShape(QtGui.QFrame.Panel)
        self.label_light.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_light.setObjectName(_fromUtf8("label_light"))
        self.label_mensaje = QtGui.QLabel(MainDialog)
        self.label_mensaje.setEnabled(False)
        self.label_mensaje.setGeometry(QtCore.QRect(20, 290, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_mensaje.setFont(font)
        self.label_mensaje.setAlignment(QtCore.Qt.AlignCenter)
        self.label_mensaje.setObjectName(_fromUtf8("label_mensaje"))
        self.label_hora = QtGui.QLabel(MainDialog)
        self.label_hora.setGeometry(QtCore.QRect(720, 10, 71, 31))
        self.label_hora.setFrameShape(QtGui.QFrame.Panel)
        self.label_hora.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_hora.setObjectName(_fromUtf8("label_hora"))
        self.frame_2 = QtGui.QFrame(MainDialog)
        self.frame_2.setEnabled(True)
        self.frame_2.setGeometry(QtCore.QRect(170, 370, 461, 111))
        self.frame_2.setFrameShape(QtGui.QFrame.Panel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setLineWidth(5)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.btn_auto = QtGui.QPushButton(self.frame_2)
        self.btn_auto.setEnabled(True)
        self.btn_auto.setGeometry(QtCore.QRect(10, 10, 99, 91))
        self.btn_auto.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("res/btn_auto.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("res/btn_auto_g.png")), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.btn_auto.setIcon(icon)
        self.btn_auto.setIconSize(QtCore.QSize(64, 64))
        self.btn_auto.setCheckable(True)
        self.btn_auto.setAutoExclusive(True)
        self.btn_auto.setObjectName(_fromUtf8("btn_auto"))
        self.btn_alta = QtGui.QPushButton(self.frame_2)
        self.btn_alta.setEnabled(True)
        self.btn_alta.setGeometry(QtCore.QRect(120, 10, 99, 91))
        self.btn_alta.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("res/btn_sol.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("res/btn_sol_g.png")), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.btn_alta.setIcon(icon1)
        self.btn_alta.setIconSize(QtCore.QSize(64, 64))
        self.btn_alta.setCheckable(True)
        self.btn_alta.setAutoExclusive(True)
        self.btn_alta.setObjectName(_fromUtf8("btn_alta"))
        self.btn_baja = QtGui.QPushButton(self.frame_2)
        self.btn_baja.setEnabled(True)
        self.btn_baja.setGeometry(QtCore.QRect(230, 10, 99, 91))
        self.btn_baja.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("res/btn_luna.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("res/btn_luna_g.png")), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.btn_baja.setIcon(icon2)
        self.btn_baja.setIconSize(QtCore.QSize(64, 64))
        self.btn_baja.setCheckable(True)
        self.btn_baja.setAutoExclusive(True)
        self.btn_baja.setObjectName(_fromUtf8("btn_baja"))
        self.btn_apagado = QtGui.QPushButton(self.frame_2)
        self.btn_apagado.setEnabled(True)
        self.btn_apagado.setGeometry(QtCore.QRect(340, 10, 99, 91))
        self.btn_apagado.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("res/btn_off.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("res/btn_off_g.png")), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.btn_apagado.setIcon(icon3)
        self.btn_apagado.setIconSize(QtCore.QSize(64, 64))
        self.btn_apagado.setCheckable(True)
        self.btn_apagado.setAutoExclusive(True)
        self.btn_apagado.setObjectName(_fromUtf8("btn_apagado"))
        self.label_arm = QtGui.QLabel(MainDialog)
        self.label_arm.setGeometry(QtCore.QRect(290, 310, 211, 20))
        self.label_arm.setObjectName(_fromUtf8("label_arm"))
        self.text_weather = QtGui.QTextEdit(MainDialog)
        self.text_weather.setEnabled(True)
        self.text_weather.setGeometry(QtCore.QRect(540, 40, 261, 321))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(242, 241, 241))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 241, 241))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.text_weather.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Condensed"))
        font.setPointSize(11)
        font.setItalic(False)
        self.text_weather.setFont(font)
        self.text_weather.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.text_weather.setFrameShape(QtGui.QFrame.Box)
        self.text_weather.setFrameShadow(QtGui.QFrame.Raised)
        self.text_weather.setLineWidth(4)
        self.text_weather.setMidLineWidth(0)
        self.text_weather.setDocumentTitle(_fromUtf8(""))
        self.text_weather.setReadOnly(True)
        self.text_weather.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.text_weather.setObjectName(_fromUtf8("text_weather"))
        self.icon_condition = QtGui.QLabel(MainDialog)
        self.icon_condition.setGeometry(QtCore.QRect(430, 50, 80, 80))
        self.icon_condition.setText(_fromUtf8(""))
        self.icon_condition.setPixmap(QtGui.QPixmap(_fromUtf8("res/icon_weather.png")))
        self.icon_condition.setScaledContents(True)
        self.icon_condition.setObjectName(_fromUtf8("icon_condition"))
        self.label_alarm_2 = QtGui.QLabel(MainDialog)
        self.label_alarm_2.setGeometry(QtCore.QRect(560, 10, 151, 31))
        self.label_alarm_2.setFrameShape(QtGui.QFrame.Panel)
        self.label_alarm_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_alarm_2.setText(_fromUtf8(""))
        self.label_alarm_2.setObjectName(_fromUtf8("label_alarm_2"))
        self.btn_test = QtGui.QPushButton(MainDialog)
        self.btn_test.setGeometry(QtCore.QRect(700, 390, 97, 81))
        self.btn_test.setObjectName(_fromUtf8("btn_test"))
        self.label_weather_status = QtGui.QLabel(MainDialog)
        self.label_weather_status.setGeometry(QtCore.QRect(400, 120, 131, 41))
        self.label_weather_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_weather_status.setObjectName(_fromUtf8("label_weather_status"))
        self.frame_2.raise_()
        self.lcdTemp.raise_()
        self.label_temp.raise_()
        self.lcdHum.raise_()
        self.label_hum.raise_()
        self.label_icon_casa.raise_()
        self.frame.raise_()
        self.label_temp_target.raise_()
        self.label_pir.raise_()
        self.label_alarm.raise_()
        self.label_light.raise_()
        self.label_mensaje.raise_()
        self.label_hora.raise_()
        self.label_arm.raise_()
        self.text_weather.raise_()
        self.icon_condition.raise_()
        self.label_alarm_2.raise_()
        self.btn_test.raise_()
        self.label_weather_status.raise_()

        self.retranslateUi(MainDialog)
        QtCore.QMetaObject.connectSlotsByName(MainDialog)

    def retranslateUi(self, MainDialog):
        MainDialog.setWindowTitle(_translate("MainDialog", "Dialog", None))
        self.label_temp.setText(_translate("MainDialog", "ºC", None))
        self.label_hum.setText(_translate("MainDialog", "%", None))
        self.btn_config.setText(_translate("MainDialog", "Config", None))
        self.btn_alarm.setText(_translate("MainDialog", "Alarma", None))
        self.label_temp_target.setText(_translate("MainDialog", "T.Objetivo: 10ºC", None))
        self.label_pir.setText(_translate("MainDialog", "-", None))
        self.label_alarm.setText(_translate("MainDialog", "Alarma: Desactivada", None))
        self.label_light.setText(_translate("MainDialog", "Iluminación: 70%", None))
        self.label_mensaje.setText(_translate("MainDialog", "OK", None))
        self.label_hora.setText(_translate("MainDialog", "00:00:00", None))
        self.label_arm.setText(_translate("MainDialog", "Caldera disarm", None))
        self.text_weather.setHtml(_translate("MainDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu Condensed\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-weight:600;\">Usurbil-Spain</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">Fecha</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-weight:600;\">Condición actual:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">Nublado</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">Temperatura: 25ºC</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">10º / 20º</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">Vel. viento: </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">Humedad:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">Sol: </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">--------------------------------------------------------</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New,courier\';\">Fri 62º / 49º</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Courier New,courier\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">--------------------------------------------------------</p></body></html>", None))
        self.btn_test.setText(_translate("MainDialog", "Test", None))
        self.label_weather_status.setText(_translate("MainDialog", "Weather", None))

