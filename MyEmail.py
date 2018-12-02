import smtplib
# Import the email modules we'll need
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback
import imaplib
import email



ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "casa.aybar" + ORG_EMAIL
FROM_PWD    = "miki7070"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 587
TO_EMAIL    = "ma.aybar@hotmail.com"

def read_email_from_gmail():
##        try:
                mail = imaplib.IMAP4_SSL(SMTP_SERVER)
                mail.login(FROM_EMAIL,FROM_PWD)
                mail.select('inbox')

                type, data = mail.search(None, 'ALL')
                mail_ids = data[0]

                id_list = mail_ids.split()   
                first_email_id = int(id_list[0])
                latest_email_id = int(id_list[-1])

                typ, data = mail.fetch(str(latest_email_id), '(RFC822)' )

                for response_part in data:
                        if isinstance(response_part, tuple):
                                msg = email.message_from_string(response_part[1].decode())
                                email_subject = msg['subject']
                                email_from = msg['from']
                                print ('From : ' + email_from + '\n')
                                print ('Subject : ' + email_subject + '\n')

##        except Exception as err:
##                traceback.print_tb(err.__traceback__)


def send_email():
        msg = MIMEMultipart()
        msg['Subject'] = 'test email'
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        body = "Python test mail"
        msg.attach(MIMEText(body, 'plain'))

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        smtpserver = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(FROM_EMAIL, FROM_PWD) 
        smtpserver.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        smtpserver.close()


read_email_from_gmail()
