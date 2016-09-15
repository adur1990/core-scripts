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
    _dirs = ('/home/meshadmin/serval-conf/etc/serval', '/home/meshadmin/serval-conf/etc/serval/rpc_bin', '/home/meshadmin/serval-conf/var/log', '/home/meshadmin/serval-conf/var/log/serval', '/home/meshadmin/serval-conf/var/run/serval', '/home/meshadmin/serval-conf/var/cache/serval','/home/meshadmin/serval-conf/var/cache/serval/sqlite3tmp','/home/meshadmin/serval-conf/var/cache/serval/blob', '/tmp/rpc_tmp')
    # generated files (without a full path this file goes in the node's dir,
    #  e.g. /tmp/pycore.12345/n1.conf/)
    _configs = ('/home/meshadmin/serval-conf/etc/serval/serval.conf', '/home/meshadmin/serval-conf/etc/serval/rpc.conf', '/home/meshadmin/serval-conf/etc/serval/rpc_bin/add', '/home/meshadmin/serval-conf/etc/serval/rpc_bin/concat', '/home/meshadmin/serval-conf/etc/serval/rpc_bin/echo_file', '/home/meshadmin/serval-conf/etc/serval/rpc_bin/ret_file', '/home/meshadmin/serval-conf/etc/serval/rpc_bin/ret_echo_file')
    # this controls the starting order vs other enabled services
    _startindex = 50
    # list of startup commands, also may be generated during startup
    #_startup = ('/home/meshadmin/serval-dna/servald start',)
    _startup = ('chmod -R 777 /home/meshadmin/serval-conf/etc/serval/rpc_bin',)
    # list of shutdown commands
    _shutdown = ()

    @classmethod
    def generateconfig(cls, node, filename, services):
        ''' Return a string that will be written to filename, or sent to the
            GUI for user customization.
        '''
        if filename == '/home/meshadmin/serval-conf/etc/serval/serval.conf':
        	cfg = 'interfaces.0.match=eth*\n'
        	cfg += 'interfaces.0.socket_type=dgram\n'
        	cfg += 'interfaces.0.type=ethernet\n'
        	#cfg += 'log.file.rotate=0\n'
        	#cfg += 'debug.rhizome=true\n'
        	#cfg += 'debug.rhizome_manifest=true\n'
        	cfg += 'debug.msp=true\n'
        	cfg += 'api.restful.users.RPC.password=SRPC\n'
        elif filename == '/home/meshadmin/serval-conf/etc/serval/rpc.conf':
            cfg = 'add 2 int int\n'
            cfg += 'concat 2 string string\n'
            cfg += 'echo_file 1 string\n'
            cfg += 'ret_file 1 string\n'
            cfg += 'ret_echo_file 1 string'
        elif filename == '/home/meshadmin/serval-conf/etc/serval/rpc_bin/add':
            cfg = 'res=$(( $1+$2 ))\n'
            cfg += 'printf "$res"\n'
            cfg += 'exit 0'
        elif filename == '/home/meshadmin/serval-conf/etc/serval/rpc_bin/concat':
            cfg = 'printf "$1$2"\n'
            cfg += 'exit 0'
        elif filename == '/home/meshadmin/serval-conf/etc/serval/rpc_bin/echo_file':
            cfg = 'cat $1\n'
            cfg += 'exit 0'
        elif filename == '/home/meshadmin/serval-conf/etc/serval/rpc_bin/ret_file':
            cfg = 'printf $1 > /tmp/resultfile\n'
            cfg += 'printf "/tmp/resultfile"\n'
            cfg += 'exit 0'
        elif filename == '/home/meshadmin/serval-conf/etc/serval/rpc_bin/ret_echo_file':
            cfg = 'RET=$(cat $1)\n'
            cfg += 'RET="$RET ---> server"\n'
            cfg += 'printf "$RET" > /tmp/resultfile\n'
            cfg += 'printf /tmp/resultfile\n'
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
