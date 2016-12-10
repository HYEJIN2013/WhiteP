import sys
import glob
import re
import pandas as pd
import numpy as np
import datetime

STARTTIMEREGEX = re.compile(r'''^\#([0-9]{2}):([0-9]{2}):([0-9]{2})''')
COMMENTREGEX = re.compile(r'''^//''')
LINEREGEX = re.compile(r'''^\{([0-9]{2})\:([0-9]{2})\:([0-9]{2})\} (.+?@.+?):(.+?) \[([0-9\.]{6,15})\]$''')
BYTEREGEX = re.compile(r'''(append|retr)\((\d+)\)''')

def _convtodataframe(protodata):
  protoseriesdata = {}
  for cmd, l in protodata.items():
    protoseriesdata[cmd] = pd.Series(l)
  
  frame = pd.DataFrame(protoseriesdata)
  return frame

def _addtoprotodata(cmd, duration, protodata):
  match2 = BYTEREGEX.search(cmd)
  if match2:
    cmd = match2.group(1).lower()+"perbyte"
    bytes = int(match2.group(2))
    if cmd not in protodata:
      protodata[cmd] = []
    protodata[cmd].append(duration/bytes)
  else:
    if cmd not in protodata:
      protodata[cmd] = []
    protodata[cmd].append(duration)

def process(proto, rampup):
  allprotodata = {}
  
  if rampup:
    rampupdonetime = None
    postprotodata = {}
    preprotodata = {}
  
  protofiles = glob.glob("./" + proto + "*.stresslog")
  for protofile in protofiles:
    #print "Opening " + protofile
    with open(protofile) as f:
      startlogtime = None
      for line in f:
        #check for start time
        starttime = STARTTIMEREGEX.search(line)
        if starttime:
          if rampup and not startlogtime:
            hour = int(starttime.group(1))
            minute = int(starttime.group(2))
            second = int(starttime.group(3))
            startlogtime = datetime.time(hour, minute, second)
            if not rampupdonetime:
              logdatetime = datetime.datetime.combine(datetime.date.today(), startlogtime)
              rampupdonetime = (logdatetime + datetime.timedelta(seconds=rampup)).time()
          continue
        
        #check for comment
        comment = COMMENTREGEX.search(line)
        if comment:
          continue
        
        #move on to real processing
        match = LINEREGEX.search(line)
        if match:
          #extract data from regex
          hour = int(match.group(1))
          minute = int(match.group(2))
          second = int(match.group(3))
          logtime = datetime.time(hour, minute, second)
          user = match.group(4)
          cmd = match.group(5)
          duration = float(match.group(6))
          
          #add to allprotodata
          _addtoprotodata(cmd, duration, allprotodata)
          
          if rampup:
            if logtime <= rampupdonetime:
              _addtoprotodata(cmd, duration, preprotodata)
            else:
              _addtoprotodata(cmd, duration, postprotodata)
        else:
          sys.stderr.write("Line didn't match: %s" % line)
  
  alldataframe = _convtodataframe(allprotodata)
  
  if rampup:
    predataframe = _convtodataframe(preprotodata)
    postdataframe = _convtodataframe(postprotodata)
  
  with open(proto+"results.txt", "w") as f:
    f.write("ALL DATA\n")
    f.write(alldataframe.describe().to_string(justify="left"))
    f.write("\n-----\n")
    if rampup:
      f.write("PRE RAMP UP DATA\n")
      f.write(predataframe.describe().to_string(justify="left"))
      f.write("\n-----\n")
      f.write("POST RAMP UP DATA\n")
      f.write(postdataframe.describe().to_string(justify="left"))
      f.write("\n-----\n")

if __name__ == "__main__":
  try:
    rampup = int(sys.argv[-1])
  except ValueError:
    rampup = None
  process("imap", rampup)
  process("pop", rampup)
