#config xml file - /tmp/agent_config.xml
#config file validator - /tmp/agent_config_validator.py


import logging
import sys
import os
import subprocess
import argparse
from PySTAF import *
from PySTAFLog import *
import time
import getopt

def main(argv):
	if(len(argv) != 2):
		print "Usage: rpc_agent.py [agent_name] [service_name]"
		exit(0)

	agent_name = argv[0]
	service_name = argv[1]
	

	filename = 'tmp/' + agent_name + 'agent_config.xml'
	config_file = os.path.realpath(filename)
	config_file_validator = os.path.realpath("/tmp/agent_config_validator.py")

	#TODO check and [!create network objects!]
	subprocess.call([config_file_validator, config_file], shell = True)

	filename = 'tmp/' + config_file + '.test'
	test_file = os.path.realpath(filename)

	print "OK"

if __name__ == "__main__":
    main(sys.argv[1:])