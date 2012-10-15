#!/usr/bin/env python

# Take the average of the cov.out files created by coverageBed
#
#
#  Created by Erik Hopmans on 10/12/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####
import numpy as np
import os
import sys
import csv
from datetime import datetime
import getpass


##### INPUTS AND OUTPUTS #####

now = datetime.now()


#Logfile
logFile = open(sys.argv[1][:-4]+".coverageAverageSDLOG.txt", 'w')
print >> logFile, "Script was run by user:", getpass.getuser()
print >> logFile, "Name of the script:", __file__
print >> logFile, "Date and time when script was started:", now.strftime("%Y-%m-%d %H:%M")
print >> logFile, "Input file of this script:", sys.argv[1]
print >> logFile, "Description of output data: coverage files (cov.out) and cov_by_region.txt"






##### DEFINE FUNCTIONS #####





##### SCRIPT #####

f=csv.reader(open(sys.argv[1], 'rU'), dialect=csv.excel_tab)
for row in f:
    path = row[0]
    file = row[1]
    pathFile = path+file

    #Check if input files are correct, cov.out files, otherwise stop script

    if file[-7:] != "cov.out":
        print "ERROR in load file! The bam file is expected to be in the bam file format"
        break

    covOutFile = open(pathFile, 'r')
    coverage = np.loadtxt(covOutFile, skiprows=0, usecols=[4])
    print np.average(coverage)
    print np.std(coverage)