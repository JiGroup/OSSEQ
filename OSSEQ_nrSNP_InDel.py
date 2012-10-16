#!/usr/bin/env python

# Determine nr of SNP and indels from varscan output
# Uses tabdelimited txt file with path in column 1 and filename in column 2 as input
#
#  Created by Erik Hopmans on 10/16/12.
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
print >> outputFile, "Filename",'\t',"SNP",'\t',"InDel"

#Logfile
logFile = open(sys.argv[1][:-4]+"LOG.txt", 'w')
print >> logFile, "Script was run by user:", getpass.getuser()
print >> logFile, "Name of the script:", __file__
print >> logFile, "Date and time when script was started:", now.strftime("%Y-%m-%d %H:%M")
print >> logFile, "Input file of this script:", sys.argv[1]
print >> logFile, "Description of output data: calculates average and stdev of coverage files (cov.out)"



##### DEFINE FUNCTIONS #####

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i                            #no +1, because I want to get rid of the header




##### SCRIPT #####

f=csv.reader(open(sys.argv[1], 'rU'), dialect=csv.excel_tab)
for row in f:
    path = row[0]
    file = row[1]
    pathFile = path+file

    #Check if input files are correct, cov.out files, otherwise stop script

    if file[-4:] != ".out":
        print "ERROR in load file, incorrect file format! "
        break

    now = datetime.now()
    print "Started calculating linenr's of file", pathFile, "at", now.strftime("%Y-%m-%d %H:%M:%S")

    print >> outputFile, file,'\t',file_len(pathFile),'\t',file_len(pathFile[:-7]+"ind.out")


#cleanup and close files
outputFile.close()

#finishing logfile
now = datetime.now()
print >> logFile, "Date and time when script was finished:", now.strftime("%Y-%m-%d %H:%M")
logFile.close()