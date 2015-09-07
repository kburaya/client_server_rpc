import logging
import sys
import os
import subprocess
import argparse
from PySTAF import *
from PySTAFLog import *
import xml.etree.ElementTree as ET
import time
import getopt

def main(argv):
	if(len(argv) == 0):
		print "Usage is: python rpc_controller.py [controller config file]"
		exit()
	config = ET.parse(argv[0])


	for agent in config.findall('AGENT'):
		agent_name = agent.get('name')
		params = agent.find('IF')
		agent_config = os.path.realpath(params.attrib.get('config'))
		agent_path_to_validator = os.path.realpath(params.attrib.get('validator'))
		agent_service_name = params.attrib.get('service')
		agent_path_to_test = os.path.realpath(params.attrib.get('scenario'))
		print "Agent name is '" + str(agent_name) + "'\nAgent config is '" + str(agent_config) + "'\nValidator file is '" + str(agent_path_to_validator) + "'\nService name is '" + str(agent_service_name) + "'\nTest case is '" + str(agent_path_to_test)

 	try:
		handle = STAFHandle(__file__)
	except STAFException, e:
		print "Error registering with STAF, RC: %d" % e.rc
		sys.exit(e.rc)

 	result = handle.submit("local", "FS", "COPY FILE %s TODIRECTORY /tmp TOMACHINE %s" % 
 	(STAFWrapData(agent_config), STAFWrapData(agent_name)))
 	print result.rc

 	result = handle.submit("local", "FS", "COPY FILE %s TODIRECTORY /tmp TOMACHINE %s" % 
 	(STAFWrapData(agent_path_to_validator), STAFWrapData(agent_name)))
 	print result.rc

 	result = handle.submit("local", "FS", "COPY FILE %s TODIRECTORY /tmp TOMACHINE %s" % 
 	(STAFWrapData(agent_path_to_test), STAFWrapData(agent_name)))
 	print result.rc

 	command_str = "python rpc_agent.py " + str(agent_name) + " " + str(agent_service_name)
 	print command_str
 	result = handle.submit(str(agent_name), "PROCESS", "START SHELL COMMAND %s WAIT RETURNSTDOUT" % STAFWrapData(command_str))

	handle.unregister()

if __name__ == "__main__":
    main(sys.argv[1:])