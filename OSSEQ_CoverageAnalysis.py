#!/usr/bin/env python

# performs coverage bed between p1 bam files (column1+2) and 450 bed files (column3+4) from the input text file. Subsequenly runs Johns total_up_cov_by_regions.pl perl script.
#
#
#  Created by Erik Hopmans on 10/10/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####
import os
import sys
import csv
from datetime import datetime
import getpass


##### INPUTS AND OUTPUTS #####

now = datetime.now()


#Logfile
logFile = open(sys.argv[1][:-4]+".coverageAnalysisLOG.txt", 'w')
print >> logFile, "Script was run by user:", getpass.getuser()
print >> logFile, "Name of the script:", __file__
print >> logFile, "Date and time when script was started:", now.strftime("%Y-%m-%d %H:%M")
print >> logFile, "Input file of this script:", sys.argv[1]
print >> logFile, "Description of output data: coverage files (cov.out) and cov_by_region.txt"




##### DEFINE FUNCTIONS #####





##### SCRIPT #####
f=csv.reader(open(sys.argv[1], 'rU'), dialect=csv.excel_tab)
for row in f:
    pathBam = row[0]
    fileBam = row[1]
    pathBed = row[2]
    fileBed450 = row[3]
    bam = pathBam+fileBam
    bedFile450 = pathBed+fileBed450
    
    
    #Check if input files are correct, skip p2 files, check if input files are bam and bed files
    if "p2." in fileBam:
        continue
    if bam[-4:] != ".bam":
        print "ERROR in load file! The bam file is expected to be in the bam file format"
    if bedFile450[-4:] != ".bed":
        print "ERROR in load file! The bed450 file is expected to be in the bed file format"

#Do a coverage bed of the p1 bam files vs the bed450 files. -d option is for reporting the depth in each position present in the Bed file. Subsequently run John's total_up_cov_by_regions.pl script bhy loading the just created cov.out as an argument in the command.



    now = datetime.now()
    print "Started processing coverageBed of file", fileBam, "at", now.strftime("%Y-%m-%d %H:%M:%S")

    coverageBed = "coverageBed -d -abam " +bam+ " -b " +bedFile450+ " > " +fileBam[:-4]+".cov.out"
    os.system(coverageBed)


    now = datetime.now()
    print "Started processing ",fileBam[:-4],"cov.out with total_up_cov_by_regions.pl at", now.strftime("%Y-%m-%d %H:%M:%S")

    perlCovRegions = "perl total_up_cov_by_region.pl "+fileBam[:-4]+".cov.out"
    os.system(perlCovRegions)


#finishing logfile
    print >> logFile, "Output files of this script:", fileBam[:-4],".cov.out/.cov_by_region.txt"

now = datetime.now()
print >> logFile, "Date and time when script was finished:", now.strftime("%Y-%m-%d %H:%M")
logFile.close()

