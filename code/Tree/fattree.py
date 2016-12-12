#!/usr/bin/env python

import sys
import time

from mininet.net import Mininet
from mininet.node import Host, OVSSwitch, Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf, TCLink
from mininet.topo import Topo
from mininet.util import dumpNodeConnections
import os


CoreSwitchList = []
AggSwitchList = []
EdgeSwitchList = []
HostList = []

pod = 8 
iCoreLayerSwitch = 16
iAggLayerSwitch = 32
iEdgeLayerSwitch = 32
iHost = 128
end = 4

net = Mininet()
#net.addController('c0', controller=RemoteController, ip='192.168.56.1')

MAC_LAST = 0

#CoreSwitch
core = 1
for x in range(1, 17):
    PREFIX = "s100"
    if x >= int(10):
        PREFIX = "s10"
    if x%4 == 0:
        IP = "10.8." + str((x/5) + 1) + "." + str(4)
    else:
        IP ="10.8." + str((x/5) + 1) + "." + str(x % 4) 
    MAC_LAST_16 = str(hex(MAC_LAST))
    MAC_new = MAC_LAST_16.split('x')[1]
    MACADDR = "00:00:00:00:00:0" + MAC_new
    CoreSwitchList.append(net.addSwitch(PREFIX + str(x), ip = IP, mac = MACADDR))
    CoreSwitchList[core-1].setIP(ip = IP)
    CoreSwitchList[core-1].setMAC(mac = MACADDR)
    core = core + 1
    MAC_LAST = MAC_LAST + 1

#AggSwitch
agg = 1
for i in range(pod):
    for j in range(pod/2,pod):
        PREFIX = "s200"
        if agg >= int(10):
            PREFIX = "s20"
        IPString = "10." + str(i) + "." + str(j) + "." + "1";
        Name = PREFIX + str(agg)
        MAC_LAST_16 = str(hex(MAC_LAST))
        MAC_new = MAC_LAST_16.split('x')[1]
        MACADDR = "00:00:00:00:00:" + MAC_new
        AggSwitchList.append(net.addSwitch(Name))
        AggSwitchList[agg-1].setIP(ip = IPString)
        AggSwitchList[agg-1].setMAC(mac = MACADDR)
        agg = agg + 1
        MAC_LAST = MAC_LAST + 1

#EdgeSwitch
edg = 1
for i in range(pod):
    for j in range(pod/2):
        PREFIX = "s300"
        if edg >= int(10):
            PREFIX = "s30"
        Name = PREFIX + str(edg)
        IPString = "10." + str(i) + "." + str(j) + ".1"
        MAC_LAST_16 = str(hex(MAC_LAST))
        MAC_new = MAC_LAST_16.split('x')[1]
        MACADDR = "00:00:00:00:00:" + MAC_new
        EdgeSwitchList.append(net.addSwitch(Name, ip = IPString))
        EdgeSwitchList[edg-1].setIP(ip = IPString)
        EdgeSwitchList[edg-1].setMAC(mac = MACADDR)
        edg = edg + 1
        MAC_LAST = MAC_LAST + 1

#Hosts
h = 1
for i in range(pod):
    for j in range(pod/2):
        for m in range(2,pod/2+2):
            PREFIX = "h00"   
            if h >= int(10):
                PREFIX = "h0"
            elif h >= int(100):
                PREFIX = "h"
            Name = PREFIX + str(h)
            IPString = "10." + str(i) + "." + str(j) + "." + str(m)
            MAC_LAST_16 = str(hex(MAC_LAST))
            MAC_new = MAC_LAST_16.split('x')[1]
            MACADDR = "00:00:00:00:00:" + MAC_new
            HostList.append(net.addHost(Name, ip=IPString, mac = MACADDR))
            #HostList[h-1].setIP(IPString, intf=intf)
            h = h + 1   
            MAC_LAST = MAC_LAST + 1


#Add C2A link
for x in range(0,iAggLayerSwitch,end):
    for i in range(0,end):
        for j in range(0,end):
            net.addLink(CoreSwitchList[i*end+j],AggSwitchList[x+i])

#Add A2E link
for x in range(0,iEdgeLayerSwitch,end):
        for i in range(0,end):
                for j in range(0,end):
                        net.addLink(AggSwitchList[x+i],EdgeSwitchList[x+j])
        
#Add E2H link
for x in range(0,iEdgeLayerSwitch):
        for i in range(0, end):
                net.addLink(EdgeSwitchList[x],HostList[end * x + i])

net.start()

#test
print "h001: IP:", HostList[0].IP(), "MAC:", HostList[0].MAC()
print "h128: IP:", HostList[127].IP(), "MAC:", HostList[127].MAC()
print "s1001: IP:", CoreSwitchList[0].IP(), "MAC:", CoreSwitchList[0].MAC()
print "s2001: IP:", AggSwitchList[0].IP(), "MAC:", AggSwitchList[0].MAC()
print "s3001: IP:", EdgeSwitchList[0].IP(), "MAC:", EdgeSwitchList[0].MAC()


CLI(net)
net.stop()
