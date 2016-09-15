#!/usr/bin/env python
import os
import sys
import signal
import time
from core import pycore
from core.misc import ipaddr
from core import service

myservices_path = os.getcwd() + '/myservices'
services = 'DefaultRoute|ServalRPCService|BroadcastFixService|NetmonService'
session = pycore.Session(persistent=True)


def signal_handler(num, stack):
    pass

signal.signal(signal.SIGINT, signal_handler)


def create_node(node_number):
    node = session.addobj(cls=pycore.nodes.CoreNode, name='n{}'.format(node_number))
    session.services.addservicestonode(node, '', services, verbose=False)
    return node


def build_islands(nodecount):
    if nodecount % 2 != 0:
        print "Only supporting even number of nodes."
        sys.exit(0)

    service.CoreServices(session).importcustom(myservices_path)
    hub1 = session.addobj(cls=pycore.nodes.HubNode, name='hub1')
    hub2 = session.addobj(cls=pycore.nodes.HubNode, name='hub2')
    bridge = session.addobj(cls = pycore.nodes.PtpNet)

    nodes1 = []
    nodes2 = []

    for i in range(1, (nodecount / 2) + 1):
        nodes1.append(create_node(i))
        nodes1[i-1].newnetif(hub1, ['10.0.0.{}/24'.format(i)])
    j = 0
    for i in range((nodecount / 2) + 1, nodecount + 1):
        nodes2.append(create_node(i))
        nodes2[j].newnetif(hub2, ['10.0.1.{}/24'.format(j+1)])
        j = j + 1

    for n in nodes1:
        service.CoreServices(session).bootnodeservices(n)
    for n in nodes2:
        service.CoreServices(session).bootnodeservices(n)
    print "Waiting..."
    time.sleep(20)
    print "Done Waiting..."
    nodes1[-1].newnetif(bridge, ['10.0.2.1/24'])
    nodes2[0].newnetif(bridge, ['10.0.2.2/24'])

    signal.pause()

    session.shutdown()


def build_chain(nodecount):
    service.CoreServices(session).importcustom(myservices_path)
    nodes = []

    left = None
    prefix = None

    for i in xrange(1, nodecount + 1):
        tmp = create_node(i)

        if left:
            tmp.newnetif(left, ["%s/%s" % (prefix.addr(2), prefix.prefixlen)])

        prefix = ipaddr.IPv4Prefix("10.0.%d.0/24" % i)
        right = session.addobj(cls = pycore.nodes.PtpNet)
        tmp.newnetif(right, ["%s/%s" % (prefix.addr(1), prefix.prefixlen)])
        nodes.append(tmp)
        left = right

    for n in nodes:
        service.CoreServices(session).bootnodeservices(n)

    signal.pause()

    session.shutdown()


def build_hub(nodecount):
    service.CoreServices(session).importcustom(myservices_path)
    hub = session.addobj(cls=pycore.nodes.HubNode, name='hub')
    nodes = []
    for i in range(1, nodecount + 1):
        nodes.append(create_node(i))
        nodes[i-1].newnetif(hub, ['10.0.0.{}/24'.format(i)])

    for n in nodes:
        service.CoreServices(session).bootnodeservices(n)

    signal.pause()

    session.shutdown()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} <topology> <nodecount>'.format(sys.argv[0]))
        sys.exit(1)

    parsed_ard = sys.argv[1].split('_')
    topology = parsed_ard[0]
    nodecount = int(parsed_ard[1])

    if topology == 'chain':
        build_chain(nodecount)
    elif topology == 'hub':
        build_hub(nodecount)
    elif topology == 'islands':
        build_islands(nodecount)
    else:
        print 'Topology "{}" not known. Aborting.'.format(topology)
