
#!/usr/bin/env python
# encoding: utf-8

import sys, os, getopt
from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.db.models import Q
from YOUR_SITE.models import QueuedEmail

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "hv", ["help", "verbose"])
		except getopt.error, msg:
			raise Usage(msg)
		for option, value in opts:
			if option in ("-v", "--verbose"):
				verbose = True
			if option in ("-h", "--help"):
				raise Usage("QueuedEmail queue flush tool. Use -v for verbose.")
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2
	
	mailqueue = FSQueuedEmail.objects.filter(
		Q(status=0) & (Q(to__isnull=False) | Q(toaddress__isnull=False) & Q(subject__isnull=False))
	)
	
	if verbose:
		print "###\t Mail queue contains %s items to be sent.\n" % len(mailqueue)
	
	for qm in mailqueue:
		if verbose:
			print "###\t Sending message..."
			print "---\t TO:\t\t\t %s" % qm.to
			print "---\t TOADDRESS:\t\t %s" % qm.toaddress
			print "---\t SUBJECT:\t\t %s" % qm.subject
		
		# output will be 1 if sending was successful
		# messages will be saved to the DB with the
		# same number for their status.
		if qm.sendit() == 1:
			if verbose:
				print "---\t Mail sent OK\n"
			else:
				print "###\t MAIL FAIL\n"

if __name__ == "__main__":
	sys.exit(main())
