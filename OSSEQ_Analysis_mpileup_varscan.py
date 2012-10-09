#!/usr/bin/env python

# OSSEQ_Analysis v1.0
#
#
#  Created by Erik Hopmans on 08/24/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####
import os
import sys
import csv
import pysam
import pybedtools
from datetime import datetime
import getpass

##### INPUTS AND OUTPUTS #####
now = datetime.now()


#Logfile
logFile = open(sys.argv[1][:-4]+"LOG.txt", 'w')
print >> logFile, "Script was run by user:", getpass.getuser()
print >> logFile, "Name of the script:", __file__
print >> logFile, "Date and time when script was started:", now.strftime("%Y-%m-%d %H:%M")
print >> logFile, "Input file of this script:", sys.argv[1]
print >> logFile, "Output file of this script:", outputFile
print >> logFile, "Description of output data: On off target nr's and percentages"



##### SCRIPT #####


f=csv.reader(open(sys.argv[1], 'rU'), dialect=csv.excel_tab)
for row in f:
    pathBam = row[0]
    fileBam = row[1]
    pathBed = row[2]
    fileBed450 = row[3]
    bam = pathBam+fileBam
    bedFile450 = pathBed+fileBed450


#Check if input files are correct
    if bam[-4:] != ".bam":
        print "ERROR in load file! The bam file is expected to be in the bam file format"
    if bedFile450[-4:] != ".bed":
        print "ERROR in load file! The bed450 file is expected to be in the bed file format"


# Open bam files and bed files for processing
    inputFile = pysam.Samfile(bam, 'rb')
    bedtool = pybedtools.BedTool(bam)
    bed450 = pybedtools.BedTool(bedFile450)


#### DEFINE FUNCTIONS #####






#On/Off target intersectbed (within 450bp or outside or 1500bp of capture probes (450bp region is searched within 1500bedtool (less sequences))

    now = datetime.now()
    print "Started processing bed450 at", now.strftime("%Y-%m-%d %H:%M:%S")

    bam_bed450 = bedtool.intersect(bed450)

    now = datetime.now()
    print "Finished processing bed450 at", now.strftime("%Y-%m-%d %H:%M:%S")

    
















#finishing logfile
now = datetime.now()
print >> logFile, "Date and time when script was finished:", now.strftime("%Y-%m-%d %H:%M")
logFile.close()












