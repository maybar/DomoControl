#!/usr/bin/python

# Constants definition
TX_RESEND = 60 #Time in seconds to resend the radio command to 'Caldera'

PIN_SENSOR_TEMP = 12    # INPUT Pin to read the temperature
PIN_PIR = 20            # INPUT Pin for movement detection (PIR)
PIN_LED_A = 6
PIN_LED_B = 5
PIN_LDR_CHARGE = 19
PIN_LDR_DISCHARGE = 13
PIN_TX = 14             # OUTPUT Pin to radio communication

PIN_WATCHDOG = 17
TEMP_TARGET_0 = 19
TEMP_TARGET_5 = 20
TEMP_TARGET_10 = 21

# MiHome App -> Gateway -> Settings -> About -> [Second last menu item]
MIHOME_GATEWAY_PASSWORD = 'z0fm3179i6yjb0go'
GATEWAY_IP = '192.168.1.100'
GATEWAY_PORT = 9898

# Sensors - SID : {device: Device type, name: Human-readable name}
SENSORS = {
    '158d0002c8d953': {'device': 'sensor_ht', 'id': 0, 'name': 'TempSensor1', 'nightmode': False},
    '158d0002bf8b7e': {'device': 'sensor_ht', 'id': 1, 'name': 'TempSensor2', 'nightmode': False},
    '158d0002c99ba6': {'device': 'sensor_ht.v1', 'id': 2, 'name': 'TempSensor3', 'nightmode': False}
 #    '158d0002c99ba6': {'device': 'sensor_ht', 'name': 'Outside'},
 #   '158d00010850da': {'device': 'magnet', 'name': 'Balcony door'}
}