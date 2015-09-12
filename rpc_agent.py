#config xml file - /tmp/agent_config.xml
#config file validator - /tmp/agent_config_validator.py

import xml.etree.ElementTree as ET
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
	if(len(argv) == 0):
		print "Script usage: agent.py [params string in xml format]"
		exit(0)

	agent_name = argv[0]
	#agent_config = ET.fromstring(argv[1])	
	config_file_validator = os.path.realpath("/tmp/agent_config_validator.py")
	config_file = os.path.realpath("tmp/" + str(agent_name) + ".xml")
	print config_file

	#TODO check and [!create network objects!]
	subprocess.call([config_file_validator, config_file], shell = True)

	print "OK"

if __name__ == "__main__":
    main(sys.argv[1:])