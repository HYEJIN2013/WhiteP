import os, sys
import smtplib
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
 
mailInfo = {
"from":"user@domain.com",
"to":"someone@anotherdomain.com",
"hostname":"smtp.exmail.qq.com",
"username":"USERNAME",
"password":"PASSWORD",
"mailsubject":"Title",
"mailtext":"Hello World!",
"mailencoding":"utf-8"
}
         
if __name__ == '__main__':
    smtp = SMTP_SSL(mailInfo["hostname"])
    smtp.set_debuglevel(1)
    smtp.ehlo(mailInfo["hostname"])
    smtp.login(mailInfo["username"],mailInfo["password"])
     
    msg = MIMEText(mailInfo["mailtext"],"text",mailInfo["mailencoding"])
    msg["Subject"] = Header(mailInfo["mailsubject"],mailInfo["mailencoding"])
    msg["from"] = mailInfo["from"]
    msg["to"] = mailInfo["to"]
    smtp.sendmail(mailInfo["from"], mailInfo["to"], msg.as_string())
     
    smtp.quit()
