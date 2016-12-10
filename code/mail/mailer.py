#!/usr/bin/python
# Relayd eMail AP Test

import re
import os
import glob
import urllib
import smtplib

from email.mime.text import MIMEText
from datetime import datetime
from subprocess import call

pathrelayd = "/tmp/error2"
KEYWORD = "stack"

senders, receivers = None, None

sender_mail = ['noreply@netcetera.ch']
receivers_mail = ['aleksandar.petreski@netcetera.com']
subject_mail = ['Switched']

sender_ecall = ['ap@netcetera.ch']
receivers_ecall = ['+38975279297@msg.ecall.ch']
subject_ecall = ['FWBLUE_RELAYD is in invalid state']

def compose(line):
  g = re.match("C\ (.+)\ (\d{2}):(\d{2}):(\d{2})\ (.+)\ applog:(.+)", line)

  if g:
    date, hour, minute, second, hostname, msg = g.groups()
    date = datetime.strptime("%d %s" % (datetime.now().year, date), "%Y %b %d")
    date = date.replace(hour=int(hour), minute=int(minute), second=int(second))
    mail_text = str.replace(str.replace(msg, ';', '\r\n'), '#011', '  ')
    mail_msg = MIMEText(mail_text)

    if KEYWORD in mail_text:
        receivers = receivers_ecall
        senders = sender_ecall
        subject = subject_ecall
    else:
        receivers = receivers_mail
        senders = sender_mail
        subject = subject_mail

    mail_msg['To'] = ",".join(receivers)
    mail_msg['From'] = ",".join(senders)
    mail_msg['Subject'] = ",".join(subject)

    return mail_msg

for file in glob.glob(pathrelayd):
 with open(file) as f:
  for line in f.readlines():
    out = compose(line)
    if out:
        print out
        print senders
        print receivers
        s = smtplib.SMTP('localhost')
        s.sendmail(senders, receivers, out.as_string())
        s.quit()

        #os.remove(file)
