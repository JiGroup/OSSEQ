#!/usr/bin/env python

#  ScriptInformation.py
#  
#
#  Created by Erik Hopmans on 06/22/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####

import getpass
import sys
from datetime import datetime

##### INPUTS AND OUTPUTS #####
now = datetime.now()


fileName = now.strftime("%Y-%m-%d_%H%M")+'output.txt'
ScriptInfoOutputFile = open (fileName, 'w')

inputFile = "test"
outputFile = "test"



##### DEFINE FUNCTIONS #####





##### SCRIPT #####



print >> ScriptInfoOutputFile, "Script was run by user:", getpass.getuser()
print >> ScriptInfoOutputFile, "Name of the script:", __file__
print >> ScriptInfoOutputFile, "Date and time when script was run:", now.strftime("%Y-%m-%d %H:%M")
print >> ScriptInfoOutputFile, "Input file of this script:", inputFile
print >> ScriptInfoOutputFile, "Output file of this script:", outputFile
print >> ScriptInfoOutputFile, "Description of output data: (PLEASE FILL THIS OUT)"