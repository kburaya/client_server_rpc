#!/usr/bin/python

import xml.etree.ElementTree as ET
import threading
import subprocess
import sys
import time
import getopt

# Global vars
sm_cli_app  = 'sm_client_c_mt_lua_cli'

default_cfg = '''
<CONFIG>
<SP name="spa">
<!-- HW -->
    <PORT name="eth0"/>
    <PORT name="eth1"/>
<!-- SW -->
<!--
    <BOND name="bond0">
        <PORT name="eth0"/>
        <PORT name="eth1"/>
    </BOND>
-->
    <NAMESPACE name="ns1">
        <NAS name="nas_1">
            <IF port="eth1" label="nas_1-if_1" ip="192.168.15.129" mask="255.255.255.0" vlan="111" gw="192.168.15.255"/>
        </NAS>
    </NAMESPACE>
    <NAMESPACE name="ns2">
        <NAS name="nas_3">
            <IF port="eth1" label="nas_1-if_1" ip="192.168.15.130" mask="255.255.255.0" vlan="111" gw="192.168.15.255"/>
        </NAS>
    </NAMESPACE>
</SP>
</CONFIG>
'''

#-------------------------------------------------------------------
def run_cli(args):

    print "# " + " ".join(["''" if not arg else arg for arg in args])   # pretty-print

    # cmd = sm_cli_app.split(' ') + args
    # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # out = p.communicate()

    # if 0 != p.returncode or 0 != len(out[1]):
    #     print "FAILED", out[1]
    #     raise Exception(out[1])

    # return out[0]

#-------------------------------------------------------------------
# sm_init_ns --ns <namespace>

def init_ns(ns):
    if ns != '':
        run_cli(['sm_init_ns', '--ns', ns])

#-------------------------------------------------------------------
# sm_close_ns --ns <namespace>

def close_ns(ns):
    if ns != '':
        run_cli(['sm_close_ns', '--ns', ns])

#-------------------------------------------------------------------
# sm_get_new_mark --ns <namespace>

def get_new_mark(ns):

    out = run_cli(['sm_get_new_mark', '--ns', ns])

    pattern = "Acquired mark="
    pos = out.find(pattern)
    if (-1 == pos):
        print "stdout:", out
        raise InputError('Cannot find proper data in response')

    result = out[pos+len(pattern):].split(" ", 1)[0]
    return result

#-------------------------------------------------------------------
# sm_del_all_by_mark --ns <namespace> --mark <mark>

def del_all_by_mark(ns, mark):

    out = run_cli(['sm_del_all_by_mark', '--ns', ns, '--mark', mark])

    pattern = "The mark={0} successfully released".format(mark)
    pos = out.find(pattern)
    if (-1 == pos):
        print "stdout", out
        raise InputError('Cannot find proper data in response')

#-------------------------------------------------------------------
# sm_add_ip --ns <namespace> --mark <mark> --port <port_name> --ip <ip> --mask <mask> --gw <gateway> --vlan <vlan_id> --label <label>

def add_interface(vdm, ifc):
    run_cli(['sm_add_ip',
            '--ns',    vdm.ns,
            '--mark',  vdm.mark,
            '--port',  ifc.get('port'),
            '--ip',    ifc.get('ip'),
            '--mask',  ifc.get('mask'),
            '--gw',    ifc.get('gw', ''),
            '--vlan',  ifc.get('vlan', '-1'),
            '--label', ifc.get('label', '')
    ])

#-------------------------------------------------------------------
# sm_del_ip_by_ip --ns <namespace> --mark <mark> --ip <ip>

def del_interface(vdm, ifc):
    run_cli(['sm_del_ip_by_ip',
            '--ns',   vdm.ns,
            '--mark', vdm.mark,
            '--ip',   ifc.get('ip')
    ])

#-------------------------------------------------------------------
# sm_set_preferred_ip --ns <namespace> --mark <mark> --ip <ip>

def set_preferred_ip(mark, ip):
    run_cli(['sm_set_preferred_ip',
            '--ns',   ns,
            '--mark', mark,
            '--ip',   ip.ip
    ])

#-------------------------------------------------------------------
def tostring(node):
    result = "<" + node.tag
    for attr, value in node.items():
        result += ' ' + attr + '="' + value + '"'
    if not node.getchildren() and not node.text:
        result += '/'
    result += '>'
    return result

# --------------------------------------------------------------------------
def validate(node):
    if not ET.iselement(node):
        print "Error: not an XML node:", node
        return False

    rc = True
    # Declare valid tags & attributes as 3 lists: sub-tags(0) mandatory(1) and optional(2)
    valid = {
        'CONFIG' : [
            ['SP'],  # tags
            [],             # mandatory
            ['name']        # optional
        ],
        'SP' : [
            ['PORT', 'BOND', 'NAMESPACE'],      # tags
            ['name'],                           # mandatory
            []                                  # optional
        ],
        'PORT' : [
            [],             # tags
            ['name'],       # mandatory
            []              # optional
        ],
        'BOND' : [
            ['PORT'],       # tags
            ['name'],       # mandatory
            []              # optional
        ],
        'NAMESPACE' : [
            ['NAS'],        # tags
            ['name'],       # mandatory
            []              # optional
        ],
        'NAS' : [
            ['IF'],     # tags
            ['name'],   # mandatory
            []          # optional
        ],
        'IF' : [
            [],                                 # tags
            ['port', 'ip', 'mask', 'vlan'],     # mandatory
            ['label', 'gw']                     # optional
        ]
    }.get(node.tag)

    if valid == None:
        print "Error: invalid tag '" + node.tag + "':", tostring(node)
        rc = False
    else:
        # Check presence of mandatory attributes
        for attr in valid[1]:
            if not node.attrib.has_key(attr):
                print "Error: mandatory attribute '" + attr + "' not found:", tostring(node)
                rc = False
        # Check that all attributes are listed as mandatory or optional
        for attr in node.attrib.keys():
            if not attr in valid[1] and not attr in valid[2]:
                print "Error: invalid attribute '" + attr + "':", tostring(node)
                rc = False

    # Validate child nodes
    for child in node:
        if not child.tag in valid[0]:
            print "Error: invalid nested tag '" + child.tag + "':", tostring(node)
            rc = False
        elif not validate(child):
            rc = False

    return rc

class NasThread(threading.Thread):
    def __init__(self, ns, nas_node, counter):
        threading.Thread.__init__(self)
        self.counter = counter
        self.ns      = ns
        self.name    = nas_node.get('name')
        self.ifs     = nas_node.findall('IF')
    def run(self):
        self.mark = 1
        print "Starting NAS '" + self.name + "' in namespace '" + self.ns + "' -> mark=" + self.mark
        while self.counter:
            for i in self.ifs:
                add_interface(self, i)
            for i in self.ifs:
                del_interface(self, i)
            self.counter -= 1
        print "Exiting NAS '" + self.name + "' in namespace '" + self.ns + "' -> mark=" + self.mark
       # del_all_by_mark(self.ns, self.mark)

#----------------------------------------------------------------

def PrintUsage():
    print 'syntax: ' + sys.argv[0] + ' [ -c <config_file> | --cfg=<config_file> ] [ -a <application> | --app=<application> ]'

def main(argv):

    global sm_cli_app   # allow modification of global var

    try:
        opts, args = getopt.getopt(argv, "hc:a:", ["cfg=", "app="])
    except getopt.GetoptError:
        PrintUsage()
        sys.exit(2)

    cfg = ''
    for opt, arg in opts:
        if opt == '-h':
            PrintUsage()
            sys.exit()
        elif opt in ("-c", "--cfg"):
            cfg = arg
        elif opt in ("-a", "--app"):
            sm_cli_app = arg

    if cfg == '':
        config = ET.fromstring(default_cfg)
    else:
        config = ET.parse(cfg)

    validate(config)

    namespaces = []
    threads    = []

    for sp in config.findall('SP'):
         print "SP=", sp.get('name')
         for ns in sp.findall('NAMESPACE'):
            print "NS=", ns.get('name')
            namespaces.append(ns)

    #start = time.time()

    # Initialize namespaces
    for ns in namespaces:
        init_ns(ns.get('name'))

    print "NS initialization successfull"
    # Create one thread per NAS
    #for ns in namespaces:
    #    for nas in ns.findall('NAS'):
    #        t = NasThread(ns.get('name'), nas, 0)
    #        threads.append(t)

    # Start all threads
    #for t in threads:
    #    t.start()

    # Wait for completion
    #for t in threads:
    #    t.join()

    # Close namespaces
    #for ns in namespaces:
    #    close_ns(ns.get('name'))

    #end = time.time()

    #print "Execution time ", int(end - start), "s"

###################### script body ##############################

if __name__ == "__main__":
    main(sys.argv[1:])
