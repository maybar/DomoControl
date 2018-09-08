# DomoControl
Centralita de control de temperatura

# Descripción
Esta aplicación corre sobre el hardware RaspberryPi3.
- Presenta la pantalla de control sobre un display de 5".
- Envía la señal de control usando una radio en 855MHz ASK. Ver proyecto CalderaCtrl para el proyecto del control de caldera.
- Arranque automatico ciando el RaspberryPi3 se enciende (util para cuando hay corestes de energía).
- Mantiene la temperatura del hogar a la tempertura establecida.
- Se puede configurar para que automaticamente cambia en 2 modos de funcionamiento: dia/noche.
- Modo desactivado para cuando la casa se deja varios dias.


# Usa Python3
Todas las herramientas han sido compiladas para python3
Adafruit_DHAT:
python3 setup.py install

PyQT4
sudo apt-get install python3-pyqt4


pip3 install apscheduler


# Ventana
Creada con QTDesigner

Usar el siguiente comando para compilar el archivo MainDialog.ui.
pyuic4 MainDialog.ui -o MainDialog.py
Despues de la compilación, se generará el archivo MainDialogg.py

