#!/usr/bin/python

import subprocess
import sys
import time
import getopt

def crt_brdg(br, ip):
	sp = subprocess.Popen(['ip', 'link', 'set', 'dev', br, 'down'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = sp.communicate()
	sp = subprocess.Popen(['sudo', 'brctl', 'delbr', br], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = sp.communicate()
	subprocess.check_call(['sudo', 'brctl', 'addbr', br])
	subprocess.check_call(['brctl', 'stp', br, 'off'])
	subprocess.check_call(['ip', 'addr', 'add', ip, 'dev', br])
	subprocess.check_call(['ip', 'link', 'set', 'dev', br, 'up']) 

def crt_veth(ns, ip):
    veth = "veth" + str(ns)
    br = "br" + str(ns)
    ip = ip + str("/24")
    #subprocess.check_call(['ip', 'netns', 'add', ns])
    subprocess.check_call(['ip', 'link', 'add', veth, 'type', 'veth', 'peer', 'name', br])
    subprocess.check_call(['brctl', 'addif', 'br-rpctest', br])
    subprocess.check_call(['ip', 'link', 'set', veth, 'netns', ns])
    
    subprocess.check_call(['ip', 'netns', 'exec', ns, 'ip', 'addr', 'add', ip, 'dev', veth])
    subprocess.check_call(['ip', 'link', 'set', br, 'up']) 
    subprocess.check_call(['ip', 'netns', 'exec', ns, 'ip', 'link', 'set', veth, 'up']) 
    subprocess.check_call(['ip', 'netns', 'exec', ns, 'ip', 'link', 'set', 'lo', 'up'])

def main(argv):
	if(len(argv) != 3):
		print "Script usage: vethconf.py -ns/-br [NS/BRIDGE] [NS/BRIDGE ip]"
		exit(1)

	if(argv[0] == "-ns"):
		ns = argv[1]
		ip = argv[2]
		crt_veth(ns, ip)

	elif(argv[0] == "-br"):
		br = argv[1]
		ip = argv[2]
		crt_brdg(br, ip)
	exit(0)


###################### script body ##############################

if __name__ == "__main__":
    main(sys.argv[1:])