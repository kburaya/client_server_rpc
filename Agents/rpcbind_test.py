#!/usr/bin/python

#from pyroute2 import netns
import os
import re
import sys
import signal
import subprocess
from subprocess import check_output


def get_pid(name):
    return int(check_output(["pidof","-s",name]))

if (len(sys.argv) == 3):
	nsname = sys.argv[1]
	status = sys.argv[2]
else: 
	print ("Script usage: ./nsconfig.sh [NSname] [start/stop]")
	sys.exit(1)

lockfilename = nsname + ".lock"
sockfilename = nsname + ".sock"
pidfilename = nsname + ".pid"

if (status == "start"):
	file = open('/tmp/' + lockfilename, 'w+')
	file.close()
	file = open('/tmp/' + sockfilename, 'w+')
	file.close()
	file = open('/tmp/' + pidfilename, 'w+')
	file.close()
	subprocess.check_call(['sudo','mount', '--bind', '/tmp/' + lockfilename, '/var/run/rpcbind.lock'])
	subprocess.check_call(['sudo','mount', '--bind', '/tmp/' + sockfilename, '/var/run/rpcbind.sock'])
	subprocess.check_call(['rpcbind'])
	pid = get_pid("rpcbind")
	print(str(pid))
	f = open('/tmp/' + pidfilename, 'w+')
	f.write(str(pid))
	f.close()

elif (status == "stop"):
	f = open('/tmp/' + pidfilename, 'r')
	pid = f.readline()
	print(pid)
	os.kill(int(pid), signal.SIGKILL)
	subprocess.check_call(['umount', '/tmp/' + lockfilename])
	subprocess.check_call(['umount', '/tmp/' + sockfilename])
	os.remove('/tmp/' + lockfilename)
	os.remove('/tmp/' + sockfilename)
	os.remove('/tmp/' + pidfilename)

else:
	print ("Script usage: ./nsconfig.sh [NSname] [start/stop]")
	sys.exit(1)