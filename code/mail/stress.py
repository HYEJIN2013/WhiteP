import traceback
import imaplib
import poplib
import random
import string
import socket
import signal
import sys
import datetime

from timer import Timer

DONE = False

def write_comment(s):
  sys.stderr.write("//" + str(s) + "\n")

def write_comment_exception():
  excstr = traceback.format_exc()
  excstr = "\n".join(["//" + line for line in excstr.split("\n")][:-1])
  sys.stderr.write(excstr+"\n")

def setup(n, proto, user, sleeptime, debug):
  sys.stdout = open("%s%s.stresslog" % (proto, n), "w")
  if debug == 0:
    sys.stderr = open("/dev/null", "w")
  elif debug == 1:
    sys.stderr = sys.stdout
  
  print "#" + datetime.datetime.now().strftime("%H:%M:%S")
  
  signal.signal(signal.SIGTERM, _signalhandler)
  signal.signal(signal.SIGCHLD, _signalhandler)
  
  return maketimermaker(user, sleeptime)

def _signalhandler(signum, frame):
  sys.stdout.flush()
  global DONE
  DONE = True

class BindingPOP(poplib.POP3, object):
  def __init__(self, source, host, port=110):
    self.source = source
    self.host = host
    self.port = port
    #self.sock = socket.create_connection((host, port), timeout)
    self.sock = socket.socket()
    self.sock.bind((self.source, 0))
    self.sock.connect((host, port))
    self.file = self.sock.makefile('rb')
    self._debugging = 0
    self.welcome = self._getresp()

class BindingIMAP(imaplib.IMAP4, object):
  def __init__(self, source, host = '', port = 143):
    self.source = source
    super(BindingIMAP, self).__init__(host, port)
  
  def open(self, host = '', port = 143):
    self.host = host
    self.port = port
    #print "Opening socket"
    self.sock = socket.socket()
    #print "Binding socket to %s" % self.source
    self.sock.bind((self.source, 0))
    #print "Connecting"
    self.sock.connect((host, port))
    self.file = self.sock.makefile('rb')

def maketimermaker(user, sleep=None):
  def timermaker(cmd):
    return Timer("%s:%s" % (user, cmd), sleep)
  return timermaker

def pop(n, source, host, user, passwd, sleeptime, debug):
  maketimer = setup(n, "pop", user, sleeptime, debug)
  
  while not DONE:
    deleted = 0
    try:
      with maketimer("socket"):
        pop = BindingPOP(source, host)
    except:
      write_comment_exception()
      sys.stdout.flush()
      sys.exit(1)
    try:
      with maketimer("login"):
        pop.user(user)
        pop.pass_(passwd)
      with maketimer("stat"):
        count, size = pop.stat()
      if count > 0:
        roll = random.randint(1, 3)
        if roll == 1:
          msgnum = random.randint(1, count)
          with maketimer("list"):
            response = pop.list(msgnum)
          size = response.split(" ")[-1]
          with maketimer("retr(%s)" % size):
            pop.retr(msgnum)
        elif roll == 2:
          msgnum = random.randint(1, count)
          with maketimer("dele"):
            pop.dele(msgnum)
          if random.randint(1, 20) <= 5:
            with maketimer("rset"):
              pop.rset()
              deleted = 0
          else:
            deleted += 1
        elif roll == 3:
          msgnum = random.randint(1, count)
          with maketimer("top"):
            pop.top(msgnum, 0)
      else:
        with maketimer("noop"):
          pop.noop()
    except poplib.error_proto:
      write_comment_exception()
    except:
      write_comment_exception()
      sys.stdout.flush()
      sys.exit(1)
    finally:
      with maketimer("logout(%s)" % deleted):
        pop.quit()
  
  write_comment("POP fork for user %s exiting at %s due to lack of messages" % (user, datetime.datetime.now()))
  sys.stdout.flush()

def imap(n, source, host, user, passwd, mailfiles, sleeptime, debug):
  maketimer = setup(n, "imap", user, sleeptime, debug)
  
  def parsemailboxes(mailboxesraw):
    return [entry.split(" ")[-1] for entry in mailboxesraw[1]]  

  while not DONE:
    selected = False
    try:
      with maketimer("socket"):
        imap = BindingIMAP(source, host)
    except:
      write_comment_exception()
      sys.stdout.flush()
      sys.exit(1)
    try:
      with maketimer("login"):
        imap.login(user, passwd)
      with maketimer("list"):
        mailboxesraw = imap.list()
      mailboxes = parsemailboxes(mailboxesraw)
      write_comment(str(mailboxes))
      madefolders = []
      pushedmsgs = []
      for _ in range(1,random.randint(15,25)):
        roll = random.randint(1,8)
        if roll == 1:
          #upload a message to a random folder
          mailbox = random.choice(mailboxes)
          with maketimer("select"):
            count = int(imap.select(mailbox)[1][0])
          selected = True
          if len(pushedmsgs) >= len(mailfiles):
            #just no-op instead
            with maketimer("noop"):
              imap.noop()
          else:
            #continue uploading file
            #make sure we haven't pushed that file yet
            mailfile = random.choice([mf for mf in mailfiles if mf not in [msg[0] for msg in pushedmsgs]])
            with open(mailfile, "r") as f:
              strng = f.read()
            with maketimer("append(%s)" % len(strng)):
              imap.append(mailbox, None, None, strng)
            response = imap.response("EXISTS")
            write_comment(response)
            newid = response[1][1]
            pushedmsgs.append((mailfile, mailbox, newid))
        elif roll == 2:
          #just no-op
          with maketimer("noop"):
            imap.noop()
        elif roll == 3:
          #read a random message from a random folder
          mailbox = random.choice(mailboxes)
          with maketimer("select"):
            count = int(imap.select(mailbox)[1][0])
          selected = True
          response = imap.response("EXISTS")
          write_comment(response)
          if count > 1:
            msgnum = random.choice(range(1,count))
            with maketimer("fetch"):
              imap.fetch("%s:%s" % (msgnum, msgnum), "(UID BODY[TEXT])")
          else:
            #just no-op
            with maketimer("noop"):
              imap.noop()
        elif roll == 4:
          #make a random folder
          foldername = "_" + "".join(random.sample(string.hexdigits, random.randint(5,8)))
          #check for the folder on the server
          with maketimer("list"):
            mailboxesraw = imap.list("", foldername)
          if mailboxesraw[0] == None:
            #just no-op instead
            with maketimer("noop"):
              imap.noop()
          else:
            with maketimer("create"):
              imap.create(foldername)
            madefolders.append(foldername)
        elif roll == 5:
          #delete a folder we made
          if len(madefolders) == 0:
            #just no-op instead
            with maketimer("noop"):
              imap.noop()
          else:
            #delete a folder
            foldername = random.choice(madefolders)
            madefolders.remove(foldername)
            with maketimer("delete"):
              imap.delete(foldername)
        elif roll == 6:
          #delete a message we pushed
          if len(pushedmsgs) == 0:
            #just no-op instead
            with maketimer("noop"):
              imap.noop()
          else:
            write_comment(str(pushedmsgs))
            msg = random.choice(pushedmsgs)
            mailbox = msg[1]
            id = msg[2]
            sys.stderr.write(str(msg))
            with maketimer("select"):
              imap.select(mailbox)
            selected = True
            with maketimer("store"):
              imap.store(id, "+FLAGS", r"\Deleted")
            with maketimer("expunge"):
              imap.expunge()
            pushedmsgs.remove(msg)
        elif roll == 7:
          #move a message to a random folder
          srcmailbox = random.choice(mailboxes)
          destmailbox = random.choice(mailboxes)
          with maketimer("select"):
            count = int(imap.select(srcmailbox)[1][0])
          selected = True
          if count > 1:
            msgnum = random.choice(range(1,count))
            with maketimer("copy"):
              imap.copy(msgnum, destmailbox)
            with maketimer("store"):
              imap.store(msgnum, "+FLAGS", r"\Deleted")
            with maketimer("expunge"):
              imap.expunge()
            pushedmsgs = [msg for msg in pushedmsgs if msg[2] != msgnum] #remove from pushed messages if we move it
          else:
            #just no-op instead
            with maketimer("noop"):
              imap.noop()
        elif roll == 8:
          with maketimer("recent"):
            imap.recent()
    except imaplib.IMAP4.error:
      write_comment_exception()
    except:
      write_comment_exception()
      sys.stdout.flush()
      sys.exit(1)
    finally:
      if selected:
        with maketimer("close"):
          imap.close()
      with maketimer("logout"):
        imap.logout()
  
  sys.stdout.flush()
