#!/usr/bin/env python

# Take the average of the cov.out files created by coverageBed
#Uses tabdelimited txt file with path in column 1 and filename in column 2
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
outputFile =  open(sys.argv[1][:-4]+"OUTPUT.txt", 'w')
print >> outputFile, "Filename",'\t',"Average",'\t',"SD"

#Logfile
logFile = open(sys.argv[1][:-4]+"LOG.txt", 'w')
print >> logFile, "Script was run by user:", getpass.getuser()
print >> logFile, "Name of the script:", __file__
print >> logFile, "Date and time when script was started:", now.strftime("%Y-%m-%d %H:%M")
print >> logFile, "Input file of this script:", sys.argv[1]
print >> logFile, "Description of output data: calculates average and stdev of coverage files (cov.out)"



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
    print >> outputFile, file,'\t',np.average(coverage),'\t',np.std(coverage)


#cleanup and close files
outputFile.close()

#finishing logfile
now = datetime.now()
print >> logFile, "Date and time when script was finished:", now.strftime("%Y-%m-%d %H:%M")
logFile.close()