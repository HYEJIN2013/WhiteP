#!/usr/bin/python
#Copyright (c) 2013, Dinoop Balakrishnan
#All rights reserved. See License
#Droplet Search Script

from os import getenv
import requests
import sys
import getopt
from prettytable import PrettyTable

#---Variables---#
api_path = 'https://api.digitalocean.com/droplets/'
client_id = getenv('dig_client_id', 'defaultVal')  # Need to set env var dig_client_id
secret_key = getenv('dig_secret_key', 'defaultVal')  # Need to set env var dig_secret_key


def helpUsage():
    """
    Help function
    """
    print """
Usage:
  python dropletSearch.py [option] [argument]
  It will take only one option at a time.
General Options:
-i			argument value : [droplet-id]   to list all info abt a particular droplet
-n			argument value : [droplet-name] to list all details abt a particular droplet name
-a			argument value : [ip-address]   to list all details abt a particular droplet with that ip-address
-r			argument value : [region]       to list all droplets of a particular region
-s			argument value : [status]       to list all droplets of a particular status ex: active, off
-d			argument value : [date-format : YYYY-MM-DD] to list all droplet created on that particular date
-m			argument value : [image-id]     to list all droplets of a particular image-id.
          """


def getOptions(argv):
    """This function collects the options from user and returns the value"""
    try:
        opts, args = getopt.getopt(argv, "hi:a:n:r:s:d:m:")
    except getopt.GetoptError:
        helpUsage()
        exit()

    for opt, arg in opts:
        if opt == '-i':
            # Method to list all Info regarding dropletId id is called
            if arg.isdigit():
                infoDropletid(arg)
            else:
                print "Droplet-id should be Numeric"
                helpUsage()
        elif opt == '-a':
            # Method to list all info regarding particular ip-addr
            infoIpaddress(arg)
        elif opt == '-n':
            # Method to list all info regarding the name of droplet
            infoName(arg)
        elif opt == '-r':
            # Method to list all droplets info within a region
            if arg in ('1', '2', '3', '4'):
                infoRegion(arg)
        elif opt == '-s':
            # Method to list all droplets with that status
            infoStatus(arg)
        elif opt == '-d':
            # Method to list all droplets with that date
            infoDate(arg)
        elif opt == '-m':
            # Method to list all droplets with Image-Id
            if arg.isdigit():
                infoImage(arg)
            else:
                print "Image-Id should be Numeric"
                helpUsage()


def tableCreator(func):
    """
    This decorator will create a table using the list of dict
    """
    table = PrettyTable(["Droplet", 'Name', 'Ip-Address', 'Region', 'Image',
                         'Size', 'Backup Active', 'Private-Ip', 'Locked',
                         'Status', 'Date'])

    def wrapper(*args):
        table_body = func(*args)
        for data in table_body:
            table.add_row([data['id'], data['name'], data['ip_address'],
                           data['region_id'], data['image_id'], data['size_id'],
                           data['backups_active'], data['private_ip_address'],
                           data['locked'], data['status'],
                           data['created_at'].rpartition('T')[0]])
        print table

    return wrapper


@tableCreator
def infoDropletid(droplet_id):
    """
    Here the droplet-id is taken as input and droplet-Info is returned
    """
    info_dict = connectDroplet(droplet_id)
    filtered_list = []
    if 'droplet' in info_dict:
        filtered_list.append(info_dict['droplet'])
    else: print "Warning : No Droplets Found"
    return filtered_list


@tableCreator
def infoIpaddress(ip_addr):
    """
    Here ip-addr as input and corresponding droplet-Info is returned
    """
    info_dict = connectDroplet()
    filtered_list = [droplet for droplet in info_dict['droplets']
                             if droplet['ip_address'] == ip_addr]
    if len(filtered_list) == 0: print "Warning : No droplet with that IP"
    return filtered_list


@tableCreator
def infoImage(img):
    """
    Here image-id is input and list of all droplet of same image-id is returned
    """
    info_dict = connectDroplet()
    filtered_list = [droplet for droplet in info_dict['droplets']
                             if droplet['image_id'] == int(img)]
    if len(filtered_list) == 0: print "Warning : No droplet with the Image-Id"
    return filtered_list


@tableCreator
def infoDate(date):
    """
    Here date is taken as input in form YYYY-MM-DD
    and the droplets created on same date are listed
    """
    info_dict = connectDroplet()
    filtered_list = [droplet for droplet in info_dict['droplets']
                           if droplet['created_at'].rpartition('T')[0] == date]
    if len(filtered_list) == 0: print "Warning : No droplet created on that date"
    return filtered_list


@tableCreator
def infoStatus(status):
    """
    Here status is taken as input and a list of droplet with
    same status is displyed
    """
    info_dict = connectDroplet()
    filtered_list = [droplet for droplet in info_dict['droplets']
                             if droplet['status'] == status]
    print "Number of droplets "+str(len(filtered_list))
    return filtered_list


@tableCreator
def infoRegion(region):
    """
    Here region-id is taken as input and list of droplet with same region
    is returned
    """
    info_dict = connectDroplet()
    filtered_list = [droplet for droplet in info_dict['droplets']
                             if droplet['region_id'] == int(region)]
    if len(filtered_list) == 0: print "Warning: No Droplets in that Region"
    return filtered_list


@tableCreator
def infoName(name):
    """
    Here name of the  droplet is taken as input and info abt particular
    droplet is returned
    """
    info_dict = connectDroplet()
    filtered_list = [droplet for droplet in info_dict['droplets']
                             if droplet['name'] == name]
    if len(filtered_list) == 0: print "No Droplets in the given name"
    return filtered_list

@tableCreator
def fullInfo():
    """
    Here all droplets of a particular account is returned
    """
    info_dict = connectDroplet()
    filtered_list = [droplet for droplet in info_dict['droplets']]
    return filtered_list


def connectDroplet(droplet_id="None"):
    """
    Here we connect the digital-ocean apis to collect droplet Info
    """
    auth_dict = {'client_id': client_id, 'api_key': secret_key}
    if droplet_id == "None":
        req_obj = requests.get(api_path, params=auth_dict)
        if req_obj.status_code == 200:
            return req_obj.json()
        else:
            print "Error: in connecting the Droplet API"
            exit()
    else:
        req_obj = requests.get(api_path+droplet_id+"/", params=auth_dict)
        if req_obj.status_code == 200:
            return req_obj.json()
        else:
            print "Error: in connecting the Droplet API"
            exit()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        helpUsage()
        print "Here we show all droplets in your account"
        fullInfo()
    else:
        getOptions(sys.argv[1:3])
