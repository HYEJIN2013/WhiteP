#!/usr/bin/env python
#coding=utf8

##########################################################################################
import sys
import traceback
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

g__logger = None

##########################################################################################
def get_exception_logger(logfile='./log_exception.log', maxBytes=1024, backupCount=5):
	if g__logger is not None:
		return g__logger
	logger = logging.getLogger("Rotating Log")
	logger.setLevel(logging.INFO)

	# add a rotating handler
	handler = RotatingFileHandler(logfile, maxBytes=maxBytes, backupCount=backupCount)
	logger.addHandler(handler)
	global g__logger
	g__logger = logger
	return g__logger

##########################################################################################
def log_exception():
	exc_info = sys.exc_info()
	out = traceback.format_exception(*exc_info)
	del exc_info
	logger = get_exception_logger()
	logger.info("[%s]%s\n%s" % (datetime.now(), '='*50, ''.join(out)))
