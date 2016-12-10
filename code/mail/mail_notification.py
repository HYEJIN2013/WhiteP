#!/usr/bin/python
import smtplib
from email.mime.text import MIMEText
import netrc
from docopt import docopt

DEFAULTFROM = "admin@minsky.unist.ac.kr"
DEFAULTTO = "carpedm20@gmail.com"
SMSADDRESS = "carpedm20@messaging.sprintpcs.com"
DEFAULTSUBJECT = "Job finished from PAIL Minsky"

def send_email(message="Job finished",subject=DEFAULTSUBJECT,
    me=DEFAULTFROM,recipients=[DEFAULTTO],
    smtpserver="localhost",login=None,password=None):

    msg = MIMEText(message)

    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ", ".join(recipients)

    s = smtplib.SMTP(smtpserver)
    s.sendmail(me,recipients, msg.as_string())
    s.quit()
    
if __name__=="__main__":
    toaddr = DEFAULTTO
    fromaddr = DEFAULTFROM
    subject = DEFAULTSUBJECT

    send_email(recipients=[toaddr], me=fromaddr, subject=subject)
