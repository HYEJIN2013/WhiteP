#coding=utf-8
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart 
from email.MIMEBase import MIMEBase 
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import smtplib
class gmail (object):
    def __init__ (self,account,password):
        self.account="%s@gmail.com"%account
        self.password=password
    
    def send (self,to,title,content):
        server = smtplib.SMTP('smtp.gmail.com' )
        server.docmd("EHLO server" )
        server.starttls()
        server.login(self.account,self.password)

        msg = MIMEText(content,'html','GBK')
        msg['Content-Type']='text/html; charset="GBK"' 
        msg['Subject'] = title
        msg['From'] = self.account
        for tomail in to.replace(',',' ').split():
            msg['To'] = tomail
            server.sendmail(self.account, tomail,msg.as_string())
        server.close()

    def sendAttach(self, to, title, content, files=[]):
        server = smtplib.SMTP('smtp.gmail.com')
        server.docmd("EHLO server" )
        server.starttls()
        server.login(self.account,self.password)
        
        msg = MIMEMultipart()
        msg.attach(MIMEText(content))
        #msg = MIMEText(content,'html','GBK')
        msg['Content-Type']='text/html; charset="GBK"' 
        msg['Subject'] = title
        msg['From'] = self.account

        for file in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(file, "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
            msg.attach(part)

        for tomail in to.replace(',',' ').split():
            msg['To'] = tomail
            server.sendmail(self.account, tomail,msg.as_string())
        server.close()
