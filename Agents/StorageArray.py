#!/usr/bin/python

import xml.etree.ElementTree as ET
import threading
import subprocess
import sys
import time
import getopt

# Global vars
sm_cli_app  = 'sm_client_c_mt_lua_cli'

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
        'SERVICE' : [
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

    print cfg
    if cfg == '':
        config = ET.fromstring(default_cfg)
    else:
        config = ET.parse(cfg)

    print config
    validate(config)

    namespaces = [] 
    

    sp = subprocess.Popen(['python', 'Agents/ns_config.py', '-br', 'br-rpctest', '192.168.16.29/24'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = sp.communicate()

    for sp in config.findall('SP'):
         #print "SP=", sp.get('name')
         for ns in sp.findall('NAMESPACE'):
            name = ns.get('name')
            for nas in ns.findall('NAS'):
                params = nas.find('IF')
                ip = params.attrib.get('ip')
                #print "NS %s params: %s" % (name, ip)
                subprocess.check_call(['python', 'Agents/ns_config.py', '-ns', name, ip])
    #start = time.time()

    # Initialize namespaces
    #for ns in namespaces:
    #    init_ns(ns.get('name'))

    print "NS initialization successfull"
    print "TestCase begin"

    #exit(1)
    
    sp = subprocess.Popen(['sudo', './Agents/StorageArray.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = sp.communicate()
    print out
    print err


    #TestCase End
    for sp in config.findall('SP'):
         #print "SP=", sp.get('name')
         for ns in sp.findall('NAMESPACE'):
            name = ns.get('name')
            subprocess.check_call(['sudo', 'ip', 'netns', 'del', name])


###################### script body ##############################

if __name__ == "__main__":
    main(sys.argv[1:])