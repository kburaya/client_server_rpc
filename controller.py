import logging
import sys
import os
import subprocess
import argparse
#from PySTAF import *
#from PySTAFLog import *
import xml.etree.ElementTree as ET
import time
import getopt

def check_services(config):
	for agent in config.findall('AGENT'):
		agent_name = agent.get('name')
		if(agent_name != "StorageArray"):
			agent_machine = agent.get('machine')
			agent_script = os.path.realpath(agent.attrib.get('script'))
			sp = subprocess.Popen(['sudo', agent_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = sp.communicate()
			print err, out


def main(argv):
	if(len(argv) == 0):
		print "Usage is: python controller.py [TestCase config file]"
		exit()
	config_file = os.path.realpath(argv[0])
	config = ET.parse(config_file)


	# try:
	# 	handle = STAFHandle(__file__)
	# except STAFException, e:
	# 	print "Error registering with STAF, RC: %d" % e.rc
	# 	sys.exit(e.rc)


	for agent in config.findall('AGENT'):
		agent_name = agent.get('name')
		if(agent_name == "StorageArray"):
			print agent_name
			#Get agent properties
			#agent_xml_params = ET.tostring(agent.find('PARAM'))
			agent_machine = agent.get('machine')
			agent_script = os.path.realpath(agent.attrib.get('script'))
			agent_config_file = os.path.realpath(agent.attrib.get('config'))

			#Agent info input
			print "Agent name is '" + str(agent_name) + "'\nAgent machine is '" + str(agent_machine) + "'\nAgent script is '" + str(agent_script)
			#print "Agent xml commands is '" + str(agent_xml_params)

			#Send validator script to agent machine
 			#result = handle.submit("local", "FS", "COPY FILE %s TODIRECTORY /tmp TOMACHINE %s" % 
 			#(STAFWrapData(agent_path_to_validator), STAFWrapData(agent_machine)))
 			#print result.rc

 			#Send agent cofig to agent machine
 			#result = handle.submit("local", "FS", "COPY FILE %s TODIRECTORY /tmp TOMACHINE %s" % 
 			#(STAFWrapData(agent_config_file), STAFWrapData(agent_machine)))
 			#print result.rc
 			#Send config file for agent

 			sp = subprocess.Popen(['python', agent_script, '-c', agent_config_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 			out, err = sp.communicate()
 			print err
 			print out
 			#result = handle.submit(str(agent_machine), "PROCESS", "START SHELL COMMAND %s WAIT STDERRTOSTDOUT RETURNSTDOUT" % (STAFWrapData(command_str)))
 			#print result.rc


 	#TestCase Begin
 	#Test environment - rpcbind run in all namespaces, all network configurations works
 	#Check all services
 	#check_services(config)

	#handle.unregister()

if __name__ == "__main__":
    main(sys.argv[1:])