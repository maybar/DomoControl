"""This module contains several classes useful for domotic proyects."""

import Grid
import numpy as np
import datetime
import time
import smtplib
import json
import pytz
import RPi.GPIO as GPIO
import email

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

def utc_to_local(utc_dt):
    local_tz = pytz.timezone('Europe/Madrid')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_dt

def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')

class HtmlText:
    def __init__(self, font_size):
        h1 = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"> \
        <html><head><meta name="qrichtext" content="1" /><style type="text/css"> \
        p, li { white-space: pre-wrap; } \
        </style></head><body style=" font-family:''Ubuntu Condensed''; font-size:'+str(font_size)+'pt; font-weight:400; font-style:normal;">'
        self.s1 = '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''Ubuntu'';">'
        self.s2 = '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:''Ubuntu'';"><br /></p>'
        self.s3 = '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''Ubuntu''; font-weight:600;">'
        self.s = h1 

    def add_text(self, text):
        self.s = self.s + self.s1 + text + "</span></p>" 
        
    def add_empty_line(self):
        self.s = self.s + self.s2 
        
    def add_title(self, text):
        self.s = self.s + self.s3 + text + "</span></p>" 
        
    def get_text(self):
        return self.s
    

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
        self.file = open("/var/tmp/DataLog-"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+".csv", "w")
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
            with open('/var/tmp/status.json', 'w') as file:
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
    
             
    
class LedDualColor:
    
    def __init__(self, PinA, PinB): 
        self.pin_a = PinA
        self.pin_b = PinB
        GPIO.setup(PinA,GPIO.OUT)
        GPIO.setup(PinB,GPIO.OUT)
        
    def setState(self, state):
        ''' Method to control the led 
        \param state State the led (RED, GREEN, OFF)'''
        
        if state == "RED":
            GPIO.output(self.pin_a,True)
            GPIO.output(self.pin_b,False)
        elif state == "GREEN":
            GPIO.output(self.pin_a,False)
            GPIO.output(self.pin_b,True)
        else:
            GPIO.output(self.pin_a,False)
            GPIO.output(self.pin_b,False)
    
    def getState(self):
        A = GPIO.input(self.pin_a)
        B = GPIO.input(self.pin_b)
        if A == 1 and B == 0:
            return "RED"
        elif A == 0 and B == 1:
            return "GREEN"
        else:
            return "OFF"
        
    def toggle(self, color):
        if (self.getState() == color) :
            self.setState("OFF")
        else:
            self.setState(color)
            
 
import smtplib
# Import the email modules we'll need
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback
import imaplib
import email  

class Email:
    def __init__(self, private):
        self.private = private
        self.mail = imaplib.IMAP4_SSL(self.private.SMTP_SERVER)
        self.mail.login(self.private.FROM_EMAIL,self.private.FROM_PWD)
        self.mail.select('inbox')
        
    def send_email(self, subject, body):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.private.FROM_EMAIL
        msg['To'] = self.private.TO_EMAIL
        msg.attach(MIMEText(body, 'plain'))

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        smtpserver = smtplib.SMTP(self.private.SMTP_SERVER, self.private.SMTP_PORT)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(self.private.FROM_EMAIL, self.private.FROM_PWD) 
        smtpserver.sendmail(self.private.FROM_EMAIL, self.private.TO_EMAIL, msg.as_string())
        smtpserver.close()

    def get_decoded_email_body(self, message_body):
        """ Decode email body.
        Detect character set if the header is not set.
        We try to get text/plain, but if there is not one then fallback to text/html.
        :param message_body: Raw 7-bit message body input e.g. from imaplib. Double encoded in quoted-printable and latin-1
        :return: Message body as unicode string
        """

        msg = email.message_from_string(message_body)

        text = ""
        if msg.is_multipart():
            html = None
            for part in msg.get_payload():

                #print "%s, %s" % (part.get_content_type(), part.get_content_charset())

                if part.get_content_charset() is None:
                    # We cannot know the character set, so return decoded "something"
                    text = part.get_payload(decode=True)
                    continue

                charset = part.get_content_charset()

                if part.get_content_type() == 'text/plain':
                    text = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')

                if part.get_content_type() == 'text/html':
                    html = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')

            if text is not None:
                return text.strip()
            else:
                return html.strip()
        else:
            text = str(msg.get_payload(decode=True), msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
        
        return text.strip()
    
    def receive_email(self):
        self.mail.select('inbox')
        status, response = self.mail.uid('search', None, 'UNSEEN SUBJECT "DOMO-CMD"')
        if status == 'OK':
            unread_msg_nums = response[0].split()
        else:
            unread_msg_nums = []
        data_list = []
        for e_id in unread_msg_nums:
            data_dict = {}
            e_id = e_id.decode('utf-8')
            _, response = self.mail.uid('fetch', e_id, '(RFC822)')
            html = response[0][1].decode('utf-8')
            email_message = email.message_from_string(html)
            data_dict['mail_to'] = email_message['To']
            data_dict['mail_subject'] = email_message['Subject']
            data_dict['mail_from'] = email.utils.parseaddr(email_message['From'])
            data_dict['body'] = get_decoded_email_body(html)
            data_list.append(data_dict)
        print(data_list)
        
    def receive_domo_cmd(self):
        self.mail.select('inbox')
        status, response = self.mail.uid('search', None, 'UNSEEN SUBJECT "DOMO-CMD"')
        if status == 'OK':
            unread_msg_nums = response[0].split()
        else:
            unread_msg_nums = []
        
        result = False
        data_dict = {}
        if (len(unread_msg_nums) > 0):
            e_id = unread_msg_nums[0]
            e_id = e_id.decode('utf-8')
            _, response = self.mail.uid('fetch', e_id, '(RFC822)')
            html = response[0][1].decode('utf-8')
            email_message = email.message_from_string(html)
            data_dict['mail_to'] = email_message['To']
            data_dict['mail_subject'] = email_message['Subject']
            data_dict['mail_from'] = email.utils.parseaddr(email_message['From'])
            data_dict['body'] = self.get_decoded_email_body(html).decode('utf-8')
            #self.mail.store(unread_msg_nums[0].replace(' ',','),'+FLAGS','\Deleted')
            result = True
        return result, data_dict
            

        
        
        
        
        
        
        