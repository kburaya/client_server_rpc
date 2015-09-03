import logging
import sys
import os
import subprocess
import argparse
from PySTAF import *
from PySTAFLog import *

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("file", help="File to copy")
parser.add_argument(metavar="machine", dest="machines", nargs="+", 
	help="List of machines to which file must be copied")
args = parser.parse_args()
args.file = os.path.realpath(args.file)
	

try:
	handle = STAFHandle(__file__)
except STAFException, e:
	print "Error registering with STAF, RC: %d" % e.rc
	sys.exit(e.rc)


for machine in args.machines:
	result = handle.submit("local", "FS", "COPY FILE %s TODIRECTORY /tmp TOMACHINE %s" % 
	(STAFWrapData(args.file), STAFWrapData(machine)))
	print result.rc

handle.unregister()

