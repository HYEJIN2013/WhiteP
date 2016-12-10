#!/usr/bin/env python

import getopt
import json
import smtplib
import sys
import time
import email.utils
import random
import string
from email.mime.text import MIMEText

ARGS = ""
LONG_ARGS = []

QUIET = False
VERBOSITY = 1

def debugwrite(s, l):
  if VERBOSITY >= l and not QUIET:
    sys.stderr.write(s)

def dumpRecipientsRefused(e):
  '''Takes in an SMTPRecipientsRefused exception and
pretty prints it if verbosity is set.'''
  if VERBOSITY >= 1 and not QUIET:
    sys.stderr.write("Recipient Address Refused.\n")
    for k, v in e.recipients.items():
      sys.stderr.write("%s: %s (%s)\n" % (k, v[0], v[1]))

def sendMessage(smtp, messagestr, env_from_address, sendingtoaddress):
  '''Sends the given message to the given address,
using the given SMTP instance.'''
  debugwrite("Sending a message.\n", 2)
  try:
    smtp.sendmail(env_from_address,
                  sendingtoaddress,
                  messagestr)
  except smtplib.SMTPRecipientsRefused, e:
    dumpRecipientsRefused(e)
  except smtplib.SMTPHeloError, e:
    debugwrite("SMTP server failed to respond correctly to HELO command.\n", 1)
  except smtplib.SMTPSenderRefused, e:
    debugwrite(
        "SMTP server rejected env-from address of %s.\n"
        % env_from_address, 1)
  except smtplib.SMTPDataError, e:
    debugwrite("Unknown STMP error.\n", 1)
  time.sleep(.05)

      
if __name__=="__main__":
  try:
    opts, args = getopt.getopt(sys.argv[1:],
                               ARGS,
                               LONG_ARGS)
  except getopt.GetoptError, err:
    #print help information and exit:
    #will print something like "option -a not recognized"
    print str(err) 
    usage()
    sys.exit(2)
    
  smtp = smtplib.SMTP(args[0])
  #smtp.login(SMTP_USER, SMTP_PASS)
  
  count = int(args[1])
  for n in range(count):
    messagedatafilename = "messagefiller.json"
    
    size = 0
    for nn in range(20):
      size += random.randint(1,6) + 4
    messageraw = ""
    for nn in range(size):
      messageraw = messageraw + random.choice(string.printable)

    dataf = open(messagedatafilename)
    data = json.load(dataf)
    dataf.close()
    
    message = MIMEText(messageraw)
    
    for header, value in data.items():
      message[header] = value

    if "Date" in message:
      del message["Date"]
    message["Date"] = email.utils.formatdate()

    if "From" not in message:
      message["From"] = "bob@fpcomm.net"
    if "Reply-To" not in message:
      message["Reply-To"] = "do-not-reply@fpcomm.net"

    #message["Subject"] = "Reply from FRII regarding your recent support request"
    #message["From"] = "support@frii.com"
    #message["Reply-To"] = "do-not-reply@frii.com"
    
    with open("logins.json") as listingf:
      listing = json.load(listingf)
    
      for emailaddr in [login[0] for login in listing["logins"]]:
        del message["To"]
        if data["To"] == "__RCPTTO__":
          message["To"] = emailaddr
        else:
          message["To"] = data["To"]
        sendMessage(smtp, message.as_string(), "bob@fpcomm.net", emailaddr.lower())
  
  smtp.close()
