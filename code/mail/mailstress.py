#!/usr/bin/env python

import sys
import json
import subprocess
import shlex
import socket
import time
import json
import netifaces
import glob
import os
import os.path
import errno
import signal
from optparse import OptionParser

import stress

ISPARENT = True

if __name__ == "__main__":  
  parser = OptionParser("Usage: %prog [options]")
  parser.add_option("--host", dest="host", help="Target hostname to benchmark")
  parser.add_option("--rampup", dest="rampup", default=None, type="float", help="Time in seconds to ramp up (0 for full power instantly)")
  parser.add_option("--duration", dest="duration", type="float", help="Time in seconds to benchmark over (total)")
  parser.add_option("--imap", dest="imap", default=None, type="int", help="Number of IMAP connections")
  parser.add_option("--pop", dest="pop", default=None, type="int", help="Number of POP connections")
  parser.add_option("--iface-pattern", dest="ifacepattern", default="eth0", type="string", help="Pattern of interfaces to use")
  parser.add_option("--loginfile", dest="loginpath", default="logins.json", type="string", help="Filename of login information")
  parser.add_option("--sleep", dest="sleep", default=None, type="float", help="Amount to sleep after each operation on children connections")
  parser.add_option("--debug", dest="debug", action="count", default=0)
  #parser.add_option("--smtp", dest="smtp", default=0, type="int", help="Number of SMTP connections")
  
  (options, args) = parser.parse_args()
  
  if options.rampup and options.rampup < 0:
    parser.error("--rampup must be >=0, or not specified")
    sys.exit(2)
  
  if options.duration <= 0:
    parser.error("--duration must be >0")
    sys.exit(2)
  
  if options.sleep and options.sleep <= 0:
    parser.error("--sleep must be >0, or not specified")
    sys.exit(2)
  
  if options.pop and options.pop <= 0:
    parser.error("--pop must be >0, or not specified")
    sys.exit(2)
    
  if options.imap and options.imap <= 0:
    parser.error("--imap must be >0, or not specified")
    sys.exit(2)
  
  if not os.path.isfile(options.loginpath):
    parser.error("--loginfile must exist")
    sys.exit(2)
 
  try:
    with open(options.loginpath) as loginfile:
      logins = json.load(loginfile)["logins"]
  except IOError as e:
    if e.errno == errno.EACCES:
      parser.error("Insufficient permissions to read specified --loginfile %s" % options.loginpath)
    else:
      parser.error("Cannot open specified --loginfile %s" % options.loginpath)
    sys.exit(2)
  
  null = open("/dev/null", "w")
  imaptime = time.time()
  imapbabies = []
  imappids = []
  #imapfiles = []
  poptime = time.time()
  popbabies = []
  poppids = []
  #popfiles = []
  
  interfaces = [interface for interface in netifaces.interfaces() if options.ifacepattern in interface]
  
  def forkimap(n):
    interface = interfaces[n%len(interfaces)]
    ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]["addr"]
    login = logins[n%len(logins)]
    
    pid = os.fork()
    if pid == 0:
      global ISPARENT
      ISPARENT = False
      stress.imap(n, ip, options.host, login[0], login[1], glob.glob("./*.msg"), options.sleep, options.debug)
      sys.exit(0)
    else:
      print "Forked IMAP process"
      imappids.append(pid)
  
  def forkpop(n):
    interface = interfaces[n%len(interfaces)]
    ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]["addr"]
    login = logins[n%len(logins)]
    
    pid = os.fork()
    if pid == 0:
      global ISPARENT
      ISPARENT = False
      stress.pop(n, ip, options.host, login[0], login[1], options.sleep, options.debug)
      sys.exit(0)
    else:
      print "Forked POP process"
      poppids.append(pid)
  
  def killforks():
    for imappid in imappids:
      print "Terminating IMAP fork"
      os.kill(imappid, signal.SIGTERM)
    for poppid in poppids:
      print "Terminating POP fork"
      os.kill(poppid, signal.SIGTERM)
  
  try:
    starttime = time.time()
    #print starttime
    if options.rampup == None:
      if options.imap:
        for n in range(options.imap):
          forkimap(len(imappids))
      if options.pop:
        for n in range(options.pop):
          forkpop(len(poppids))
    
    while time.time() - starttime < options.duration:
      #print time.time() - starttime
      if options.rampup > 0:
        if len(imappids) < options.imap:
          imappersec = options.rampup/options.imap
          while time.time() - imaptime > imappersec:
            imaptime += imappersec
            forkimap(len(imappids))
        if len(poppids) < options.pop:
          poppersec = options.rampup/options.pop
          while time.time() - poptime > poppersec:
            poptime += poppersec
            forkpop(len(poppids))
      
      time.sleep(0.05)
  finally:
    if ISPARENT:
      killforks()
      print "Done."
