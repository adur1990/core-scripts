#
# CORE
# Copyright (c)2010-2012 the Boeing Company.
# See the LICENSE file included in this distribution.
#
''' serval service.
'''

import os

from core.service import CoreService, addservice
from core.misc.ipaddr import IPv4Prefix, IPv6Prefix

class ServalService(CoreService):
    ''' ServalRPC service
    '''
    # a unique name is required, without spaces
    _name = 'ServalRPCService'
    # you can create your own group here
    _group = 'Mesh'
    # list of other services this service depends on
    _depends = ('BroadcastFixService', )
    # per-node directories
    _dirs = ('/home/artur/serval-conf/etc/serval', '/home/artur/serval-conf/etc/serval/rpc_bin', '/home/artur/serval-conf/var/log', '/home/artur/serval-conf/var/log/serval', '/home/artur/serval-conf/var/run/serval', '/home/artur/serval-conf/var/cache/serval','/home/artur/serval-conf/var/cache/serval/sqlite3tmp','/home/artur/serval-conf/var/cache/serval/blob', '/tmp/rpc_tmp')
    # generated files (without a full path this file goes in the node's dir,
    #  e.g. /tmp/pycore.12345/n1.conf/)
    _configs = ('/home/artur/serval-conf/etc/serval/serval.conf', '/home/artur/serval-conf/etc/serval/rpc.conf', '/home/artur/serval-conf/etc/serval/rpc_bin/simple', '/home/artur/serval-conf/etc/serval/rpc_bin/complex')
    # this controls the starting order vs other enabled services
    _startindex = 50
    # list of startup commands, also may be generated during startup
    _startup = ('chmod -R 777 /home/artur/serval-conf/etc/serval/rpc_bin',)
    # list of shutdown commands
    _shutdown = ()

    @classmethod
    def generateconfig(cls, node, filename, services):
        ''' Return a string that will be written to filename, or sent to the
            GUI for user customization.
        '''
        if filename == '/home/artur/serval-conf/etc/serval/serval.conf':
            cfg = 'interfaces.0.match=eth*\n'
            cfg += 'interfaces.0.socket_type=dgram\n'
            cfg += 'interfaces.0.type=ethernet\n'
            cfg += 'api.restful.users.RPC.password=SRPC\n'
            cfg += 'api.restful.newsince_timeout=5s'
        elif filename == '/home/artur/serval-conf/etc/serval/rpc.conf':
            cfg = 'simple 1 string\n'
            cfg += 'complex 1 string'
        elif filename == '/home/artur/serval-conf/etc/serval/rpc_bin/simple':
            cfg = 'echo "$1 -> server"\n'
            cfg += 'exit 0'
        elif filename == '/home/artur/serval-conf/etc/serval/rpc_bin/complex':
            cfg = 'echo "$1"\n'
            cfg += 'exit 0'
        else:
        	cfg = ''
        return cfg

    @staticmethod
    def subnetentry(x):
    	''' Generate a subnet declaration block given an IPv4 prefix string
    		for inclusion in the config file.
    	'''
    	if x.find(':') >= 0:
    		return ''
    	else:
    		net = IPv4Prefix(x)
    		return 'echo "  network %s"' % (net)

addservice(ServalService)
