#!/usr/local/bin/python3.4

import string
import os
import re
import sys
import atexit
import base64
if os.name=='nt':
   from ctypes import windll


import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


hits = 0
smtp_passwd = 'password'
email_from = 'dummy@email.com'
email_to = ['dummy@email.com']
scan_done = False

def write_log(log_file,string):
    with open(log_file, "a") as myfile:
        myfile.write(string + "\n")

def delete_log(log_file):
    if os.path.isfile(log_file):
        os.remove(log_file)

def find_file(root_folder, rex,name,log_file):
    global hits
    print( "{0} hit(s)\r".format(hits),end="" )

    for root,dirs,files in os.walk(root_folder):
        for f in files:
            result = rex.search(f)
            if result:
                hit = os.path.join(root,f)

                if(not re.compile("^(\/Applications|.?:(\\|\/)Windows).*").match(hit)):
                    hits+=1
                    write_log(log_file,hit)
                    print( "{0} hit(s)\r".format(hits),end="" )


def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives

def find_file_in_all_drives(pattern):
    global hits,scan_done
    hits = 0
    rex = re.compile(pattern)
    name = input("Who are you?: ")

    

    log_file = name.replace (" ", "_").lower()+'_media_log.txt'
    write_log(log_file,"Scanning for "+name)

    atexit.register(send_log,log_file=log_file)

    delete_log(log_file)

    if os.name=='nt':
        print("Windows System Detected")
        drives = get_drives();
        write_log(log_file,"Scanning Drives: "+str(drives)[1:-1])
        print ("Scanning Drives: "+str(drives)[1:-1])
        for drive in drives:
            find_file( drive+":\\", rex,name ,log_file )
    elif os.name=='posix':
        print("POSIX System Detected")
        write_log(log_file,"Scanning root (/)")
        print("Scanning root (/)")

        find_file( '/', rex,name , log_file)

    scan_done = True
    write_log(log_file,"Done Scanning")

def send_log(log_file):
    global email_to,email_from,scan_done

    if(not scan_done):
        write_log(log_file,"Scan Cancelled")

    print('sending log: '+log_file)

    with open (log_file, "r") as myfile:
        data=myfile.read()
        send_mail(email_from,email_to,'Media Scan Log',data)


def send_mail(send_from, send_to, subject, text, server="smtp.gmail.com", port=587):
    global smtp_passwd
    assert isinstance(send_to, list)





    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
           % (send_from, COMMASPACE.join(send_to), subject))
    msg+=text

    passwd = base64.b64decode(smtp_passwd).decode('ascii')
    smtp = smtplib.SMTP(server,port)
    smtp.ehlo()
    smtp.starttls()
    #smtp.set_debuglevel(True)
    smtp.login(send_from,passwd)
    try:
        smtp.sendmail(send_from, send_to, msg)
        print("Email report sent")
    finally:
        smtp.close()

if __name__ == '__main__':
    find_file_in_all_drives( '(mp3|mp4|wma|wmv|mkv|avi|mpg|mpeg)$' )
    print("Done")
