#!/usr/bin/env python
import smtplib
import argparse

parser = argparse.ArgumentParser(description='Send massive emails')
parser.add_argument('to_addr_list', metavar='TO', type=str, nargs='+',
                    help='List of addresses to send the emails')
parser.add_argument('--number', '-n', type=int, default=100,
                    help='Number of emails to send)')
parser.add_argument('--username', '-u', help='SMTP login')
parser.add_argument('--password', '-p', help='SMTP password')
parser.add_argument('--host', default="localhost", help='SMTP host')
parser.add_argument('--subject', default="Mail subject", help='Subject of the mail to send')
parser.add_argument('--message', default="Mail body", help='Body of the mail to send')


def connect_smtp(host, username, password):
    server = smtplib.SMTP(host)
    server.login(username, password)
    return server

def send_email(server, from_addr, to_addr_list, subject, message):
    header = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    return server.sendmail(from_addr, to_addr_list, message)


args = parser.parse_args()
server = connect_smtp(args.host, args.username, args.password)

if args.number > 1:
    for i in xrange(args.number):
        subject = "%s %d" % (args.subject, i + 1)
        message = "%s %d" % (args.message, i + 1)
        send_email(server, args.username, args.to_addr_list, subject, message)
elif args.number == 1:
    send_email(server, args.username, args.to_addr_list, args.subject, args.message)
else:
    print "Ok, 0 emails sent"
