#!/usr/bin/env python

import subprocess
import sys
import time
from boto.ec2.connection import EC2Connection

from chef import ChefAPI, Node

SSH_CONFIG_BLOCK = """
host %(host)s
User ubuntu
hostname %(hostname)s
IdentityFile ~/.ssh/id_rsa
"""

VPC_SSH_CONFIG_BLOCK = """
host %(host)s
User ubuntu
hostname %(hostname)s
ProxyCommand ssh -q -o StrictHostKeyChecking=no vpc_%(environment)s_nat1 nc %%h 22
IdentityFile ~/.ssh/id_rsa
"""

SERVER_OPTS = {

    "dev" :
            {
             "machine_size": 'm1.large',
             "security_groups": ['default', 'linux', 'web'],
             "subnet": "subnet-1234abcd",
            },

       "staging_web" :
            {
            "machine_size": "m1.large",
            "security_groups": ['default', 'linux', 'web'],
            "subnet": "subnet-1234abcd",
            },

      "prod_web" :
            {
            "machine_size": "c1.xlarge",
            "security_groups": ['default', 'linux', 'web']
            },

}

SUBNETS = {

    'public': ['subnet-1234abcd'],
    'private': ['subnet-abcd1234']

}

class Machine(object):
    """
    Class to contain all the information about a new AWS machine configuration
    in an easy to use format.  Additional information about the machine stored
    by AWS can be retrieved via class methods.
    """
    def get_machine_name(self):
        """
        Get the human readable machine name using the machine type and
        searching Knife for similar servers
        """
        # This must be called to get the correct Knife Setup for Node()
        # Even if we don't use the resulting API object directly
        api = ChefAPI.from_config_file(self.KNIFE_CONFIG)
        if self.VPC:
            base_name = "yip_%s%%s" % self.machine_type
        else:
            base_name = "yipit_%s%%s" % self.machine_type

        index = 1
        while True:
            name = base_name % index
            node = Node(name)
            if node.exists:
                index += 1
            else:
                break

        return name


    def __init__(self, machine_type, machine_size, security_groups, role=None, subnet=None, mongo_shard=None):
        super(Machine, self).__init__()
        self.machine_type = machine_type
        self.machine_size = machine_size
        self.security_groups = security_groups

        # So Knife Doesn't complain when launching into EC2
        # We want to keep the original list so we can update groups in VPC
        if len(self.security_groups) > 1:
            self.security_groups_as_string = ','.join(self.security_groups).replace("'", "")
        else:
            self.security_groups_as_string = str(self.security_groups).strip('[').strip(']')

        self.role = role
        self.subnet = subnet


        # Figure out what environment we will be launching into
        if self.subnet is not None:
            self.VPC = True
        else:
            self.VPC = False

        if 'prod' in self.machine_type:
            self.ENV = 'prod'
            if self.VPC:
                self.KNIFE_CONFIG = 'prod/vpc-knife.rb'
            else:
                self.KNIFE_CONFIG = 'prod/knife.rb'
            self.CHEF_ENV = 'production'
        elif 'staging' in self.machine_type:
            self.ENV = 'staging'
            if self.VPC:
                self.KNIFE_CONFIG = 'staging/vpc-knife.rb'
            else:
                self.KNIFE_CONFIG = 'staging/knife.rb'
            self.CHEF_ENV = 'staging'

        # Build out our default options
        self.ami = 'ami-a29943cb'
        self.ssh_key = "%s_1" % (ENV)
        self.ssh_key_path = "~/.ssh/%s.pem" % (self.ssh_key)
        self.user = 'ubuntu'
        self.ebs_size = 20
        self.bootstrap_script = 'ubuntu12.04'

        self.name = self.get_machine_name()

        # Default to the machine type as the role
        if self.role is None:
            self.role = self.machine_type

        self.options = {
                        'ami': ('-I', self.ami),
                        'ssh_key': ('-S', self.ssh_key),
                        'ssh_key_path': ('-i', self.ssh_key_path),
                        'user': ('-x', self.user),
                        'ebs_size': ('--ebs-size', self.ebs_size),
                        'bootstrap_script': ('-d', self.bootstrap_script),
                        'name': ('-N', self.name),
                        'knife_key': ('-c', self.KNIFE_CONFIG),
                        'chef_environment': ('-E', self.CHEF_ENV),
                        'machine_size': ('-f', self.machine_size),
                        'security_groups': ('-G', self.security_groups_as_string),
                        'role': ('-r', "role[{}]".format(self.role)),
                        }

        if self.subnet is not None:
            self.options.update({'subnet': ('-s', self.subnet)})



    def get_knife_command(self):
        """
        Returns the knife command necessary to launch the instance from
        a subprocess.
        """

        base_command = "knife ec2 server create"

        opts = ""

        for k, v in self.options.iteritems():
            opts = '{} {} "{}"'.format(opts, v[0], v[1])

        return base_command + opts


def get_groups_by_name(conn, security_group_names=[]):
    vpc_security_groups = []
    filtered_security_groups = []

    # Get All groups and filter ourself since boto doesn't handle
    # similarly named groups across VPC vs EC2 very well
    all_groups = conn.get_all_security_groups()
    # Filter to VPC groups
    for group in all_groups:
        if group.vpc_id is not None:
            vpc_security_groups.append(group)

    # Filter to Groups we want
    for group in vpc_security_groups:
        if group.name.lower() in security_group_names:
            filtered_security_groups.append(group)

    return filtered_security_groups

def main(machine_type):

    instance = Machine(machine_type)
    command = instance.get_knife_command()

    print "Running %s" % command

 ## Tailing Output
    ec2_id = None
    hostname = None
    public_ip_address = None
    private_ip_address = None
    conn = EC2Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    needs_elastic_ip = True

    proc = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline().rstrip()
        # Check if we are done with the output
        if not line:
            time.sleep(0.1) # Sleep
            if proc.poll() is None:
                continue
            else:
                break


        # Check if we need an EIP for this instance
        # Make sure we dont have one already?
        # Get a new EIP
        # Assign to the instance

        # Add en EIP if we are in a public subnet
        if instance.VPC and instance.subnet in SUBNETS['public'] and needs_elastic_ip:
            # We want to know our instance ID before checking
            # We also want to wait for the private IP address so we know we are in a state
            # where we can attach an EIP
            if private_ip_address is not None and ec2_id is not None:
                # Get our instance's public IP, if it exists
                # Since we filter by instance ID, we should only have 1 result
                i = conn.get_all_instances(instance_ids=[ec2_id])[0].instances[0]
                if i.ip_address is None:
                    allocation = conn.allocate_address(domain='vpc')
                    conn.associate_address(instance_id=ec2_id, allocation_id=allocation.allocation_id)
                    needs_elastic_ip = False


        # Process the output
        if "Instance ID" in line:
            if ec2_id is None:
                ec2_id = line.split()[-1]
        if "Public DNS Name" in line:
            if hostname is None:
                hostname = line.split()[-1]
        if "Public IP Address" in line:
            if public_ip_address is None:
                public_ip_address = line.split()[-1]
        if "Private IP Address" in line:
            if private_ip_address is None:
                private_ip_address = line.split()[-1]
        print line


    created_tags = conn.create_tags([ec2_id], {"Name": instance.name})
    print "Rebooting new machine..."

    # #if proc.returncode == 0: # Knife Return Code is always 0
    conn.reboot_instances([ec2_id])

    # Update Run List (useful in case a chef-client run doesn't succeed)
    # Re-adding the same element is idempotent
    print "Updating Run List..."
    command = "knife node run_list add {0} 'role[{1}]' -c {2} -E {3}".format(instance.name, instance.role, instance.KNIFE_CONFIG, instance.CHEF_ENV)
    subprocess.call(command, shell=True)
    print

    if instance.VPC:
        # Weird bug where we end with the "recipe[roles] when we manually add the instance role"
        command = "knife node run_list remove {0} recipe[roles] -c {1} -E {2}".format(instance.name, instance.KNIFE_CONFIG, instance.CHEF_ENV)
        subprocess.call(command, shell=True)
        print

    # # Update Security Groups as Knife/Fog fails to do this in VPC
    if instance.VPC:
        print "Updating Security Groups..."
        # Check to see if we already have the group attached to our instance
        group_ids = [group.id for group in get_groups_by_name(conn, instance.security_groups)]
        conn.modify_instance_attribute(instance_id=ec2_id, attribute='GroupSet', value=group_ids)
        print "Security Groups Set to {}".format(instance.security_groups)
        print

    print "Add to yipit/config/ssh_config:"

    if instance.VPC:
        print VPC_SSH_CONFIG_BLOCK % {'hostname': private_ip_address, 'host': instance.name, 'environment': instance.ENV}

    else:
        print SSH_CONFIG_BLOCK % {'hostname': hostname, 'host': instance.name}


if __name__ == '__main__':
    machine_type = sys.argv[1]
    if 'prod' in machine_type:
        ENV = 'prod'
        AWS_ACCESS_KEY = "foo"
        AWS_SECRET_KEY = "bar"
        KNIFE_CONFIG = 'prod/knife.rb'
    else:
        ENV = 'staging'
        AWS_ACCESS_KEY = 'foo'
        AWS_SECRET_KEY = 'bar'
        KNIFE_CONFIG = 'staging/knife.rb'

    main(machine_type)
