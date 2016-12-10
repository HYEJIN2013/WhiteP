# coding: utf-8
#Print your mail

import imaplib, tempfile, os, subprocess, time
import email, email.header

def checkUnreadAndPrint():
    mail = imaplib.IMAP4_SSL("IMAP.HOST.COM")
    mail.login("USER", "PASSWORD")
    mail.select("INBOX")
    result, data = mail.search(None, '(UNSEEN)')
    if data != [""]:
        ids = data[0]
        id_list = ids.split()
        latest_email_id = id_list[-1]
        result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        
        for part in email_message.walk():
        
            if part.get_content_type() == "text/plain":
                temp = tempfile.NamedTemporaryFile(delete=False)
                temp.write(part.get_payload(decode=True).decode("utf-8"))
                temp.close()
                subprocess.call(["lpr", "-P", "PRINTERNAME", "-l", temp.name])

            if part.get_content_maintype()  != "multipart" and part.get("Content-Disposition") is not None:
                temp = os.path.join("/tmp", part.get_filename().decode("utf-8"))
                f = open(temp, "wb")
                f.write(part.get_payload(decode=True))
                f.close()
                #Pdf ??
                if "application/pdf" in part.get("Content-Type").split(";")[0]:
                    subprocess.call(["lpr", "-P", "PRINTERNAME", "-l", temp])
                #Convert with unoconv if not
                else:
                    subprocess.call(["unoconv", "-f", "pdf", temp])
                    subprocess.call(["lpr", "-P", "PRINTERNAME", "-l", temp.split(".")[0] + ".pdf"])
    mail.close()

while True:
    checkUnreadAndPrint()
    time.sleep(60)
