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
	print argv[0]

	#if STAF doesn't work write these commands to cli
	#export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/staf/lib"
	#export PATH=$PATH:$HOME/bin:/usr/local/staf/bin
	
	try:
		handle = STAFHandle(__file__)
	except STAFException, e:
		print "Error registering with STAF, RC: %d" % e.rc
		sys.exit(e.rc)


	for agent in config.findall('AGENT'):
		agent_name = agent.get('name')
		#Get agent properties
		params = agent.find('IF')
		#agent_xml_params = ET.tostring(agent.find('PARAM'))
		agent_machine = params.attrib.get('machine')
		agent_path_to_validator = os.path.realpath(params.attrib.get('script'))
		agent_config_file = os.path.realpath(params.attrib.get('config'))

		#Agent info input
		print "Agent name is '" + str(agent_name) + "'\nAgent machine is '" + str(agent_machine) + "'\nValidator file is '" + str(agent_path_to_validator)
		#print "Agent xml commands is '" + str(agent_xml_params)

		#Send validator script to agent machine
 		result = handle.submit("local", "FS", "COPY FILE %s TODIRECTORY /tmp TOMACHINE %s" % 
 		(STAFWrapData(agent_path_to_validator), STAFWrapData(agent_machine)))
 		print result.rc

 		#Send agent cofig to agent machine
 		result = handle.submit("local", "FS", "COPY FILE %s TODIRECTORY /tmp TOMACHINE %s" % 
 		(STAFWrapData(agent_config_file), STAFWrapData(agent_machine)))
 		print result.rc
 		#Send config file for agent

 		sp = subprocess.Popen(['python', 'Agents/agent_config_validator.py', '-c', agent_config_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 		out, err = sp.communicate()
 		print err
 		print out
 		#result = handle.submit(str(agent_machine), "PROCESS", "START SHELL COMMAND %s WAIT STDERRTOSTDOUT RETURNSTDOUT" % (STAFWrapData(command_str)))
 		#print result.rc

	handle.unregister()

if __name__ == "__main__":
    main(sys.argv[1:])