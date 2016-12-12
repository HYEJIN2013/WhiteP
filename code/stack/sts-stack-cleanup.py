#!/usr/bin/env python

__author__ = "Jorge Niedbalski <niedbalski@ubuntu.com>"

import os
import re
import operator
import smtplib

from keystoneclient.v2_0 import client 
from ceilometerclient.client import get_client
from ceilometerclient.v2.options import cli_to_array

from keystoneclient.auth.identity import v2
from keystoneclient import session

from novaclient.v1_1 import client as novaclient

from datetime import date, datetime, timedelta 
from optparse import OptionParser

_HERE = os.path.dirname(os.path.basename(__file__))
TEMPLATES_PATH = os.path.join(_HERE, "templates")


from jinja2 import Environment, FileSystemLoader

def send_email(sender, receveirs, message):
   try:
       smtp = smtplib.SMTP('localhost')
       smtp.sendmail(sender, receivers, message)      
   except:
     pass


def dispatch_report(tenants):
    for email, instances in tenants.items():
	instances = [i.to_dict() for i in instances]
	send_email('sts-stack-noreply@canonical.com',
		[email],
		load_template("stop_instance", {'email': email,
					        'instances': instances,
	}))

def load_template(name, params):
    env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
    return env.get_template(name + ".tpl").render(**params)

def filter_instances(delta, excluded_tenants):

    def is_old_enough(created, delta):
        return datetime.strptime(created, '%Y-%m-%dT%H:%M:%SZ') <= delta

    keystone = client.Client(username=os.environ.get('OS_USERNAME'), 
	password=os.environ.get('OS_PASSWORD'), 
	tenant_name=os.environ.get('OS_TENANT_NAME'),
        auth_url=os.environ.get('OS_AUTH_URL'))

    nova = novaclient.Client(None, None, None, auth_url=keystone.auth_url,
		       tenant_id=keystone.tenant_id,
		       auth_token=keystone.auth_token)

    for server in nova.servers.list(search_opts={'all_tenants': True}):
        if not server.human_id.endswith('bastion') and server.status in ('ACTIVE', ) and is_old_enough(server.updated, delta):
	    tenant = keystone.tenants.get(server.tenant_id)
	    setattr(tenant, 'email', keystone.users.get(server.user_id).email)

	    if tenant.name not in excluded_tenants:
   	        yield tenant, server


def filter_ceilometer_stats(instance_id, meters):
    ceilometer = get_client(api_version=2, **{
	'os_username': os.environ.get("OS_USERNAME"),
	'os_password': os.environ.get("OS_PASSWORD"),
	'os_tenant_name': os.environ.get("OS_TENANT_NAME"),
	'os_auth_url': os.environ.get("OS_AUTH_URL"),
    })

    for meter in meters:
        for stat in ceilometer.statistics.list(meter_name=meter.get('field'),
		q=cli_to_array("resource_id={0}".format(instance_id))):
	    yield getattr(operator, meter.get('op'))(float(stat.avg), float(meter.get('value')))


def parse_options():
    parser = OptionParser()
    parser.add_option("-d", "--days", dest="days", default=3,
                      help="Days delta for instances", metavar="days")

    parser.add_option("-m", "--meters", default="cpu_util<=0.9",
                      dest="meters",
                      help="Meters to check, i.e: 'cpu_util<=0.9'")

    parser.add_option("-e", "--exclude-tenants", default="",
                      dest="exclude_tenants")

    parser.add_option("-s", "--send-report", default=False,
                      dest="dispatch_report")

    (options, args) = parser.parse_args()
    return options 


def main():
    options = parse_options()
    meters = cli_to_array(options.meters)
    delta = datetime.now() - timedelta(days=int(options.days))
    exclude_tenants = options.exclude_tenants.split(",")

    print "Looking for instances matching: {0} usage criteria , ignoring the ones creted over the last {1} days\n".format(optio
ns.meters, options.days)
    
    to_report = {}
    for tenant, instance in filter_instances(delta, exclude_tenants):
        if all(f for f in filter_ceilometer_stats(instance.id, meters)):
	    if tenant.email not in to_report:
                to_report[tenant.email] = []
            to_report[tenant.email].append(instance)	    

	    # Stop the instance, until new activity
            instance.stop()

    if options.dispatch_report:
        dispatch_report(to_report)


if __name__ == "__main__":
    main()
