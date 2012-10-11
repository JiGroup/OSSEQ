#!/usr/bin/env python

# OSSEQ_Analysis v1.0:
#Uses an tab-delimeted inputfile as command line argument with 5 columns:
#column 1: path to bam file
#column 2: filename bam file
#column 3: path to bed files
#column 4: filename bed file 450bp around capture probe (On target)
#column 5: filename bed file 1500bp around capture probe (Off target)
#
#Subsequently the nr of mapped and unmapped reads are determined (+percentages), nr of unmapped reads containing oligoC or D sequences.
#In the next part an intersectBed is performed to determine the on and off target numbers and percentages.
#
#
#
#
#  Created by Erik Hopmans on 08/24/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####
import sys
import csv
import pysam
import pybedtools
from datetime import datetime
import getpass
import os

##### INPUTS AND OUTPUTS #####
now = datetime.now()

#Creating outputfile with inputfileOUTPUT name and header line
outputFile =  open(sys.argv[1][:-4]+"OUTPUT.txt", 'w')
print >> outputFile, "Filename",'\t',"Reads:",'\t',"Mapped Reads:",'\t',"NonMapped Reads",'\t',"% Align",'\t',"OligoC in NM",'\t',"OligoD in NM",'\t',"On target",'\t',"% On Target",'\t',"Off Target",'\t',"% Off Target",'\t'


#Logfile: a logfile is created that states when which script was run by who and saved to a inputfileLOG.txt file
logFile = open(sys.argv[1][:-4]+"LOG.txt", 'w')
print >> logFile, "Script was run by user:", getpass.getuser()
print >> logFile, "Name of the script:", __file__
print >> logFile, "Date and time when script was started:", now.strftime("%Y-%m-%d %H:%M")
print >> logFile, "Input file of this script:", sys.argv[1]
print >> logFile, "Output file of this script:", outputFile
print >> logFile, "Description of output data: On off target nr's and percentages"



##### SCRIPT #####
#script loops through each line of the inputfile to determine read nr's etc.

f=csv.reader(open(sys.argv[1], 'rU'), dialect=csv.excel_tab)
for row in f:
    pathBam = row[0]
    fileBam = row[1]
    pathBed = row[2]
    fileBed450 = row[3]
    fileBed1500 = row[4]
    bam = pathBam+fileBam
    bedFile450 = pathBed+fileBed450
    bedFile1500 = pathBed+fileBed1500

#Check if input files are correct
    if bam[-4:] != ".bam":
        print "ERROR in load file! The bam file is expected to be in the bam file format"
    if bedFile450[-4:] != ".bed":
        print "ERROR in load file! The bed450 file is expected to be in the bed file format"
    if bedFile1500[-4:] != ".bed":
        print "ERROR in load file! The bed1500 file is expected to be in the bed file format"

# Open bam files and bed files for processing
    inputFile = pysam.Samfile(bam, 'rb')
    bedtool = pybedtools.BedTool(bam)
    bed450 = pybedtools.BedTool(bedFile450)
    bed1500 = pybedtools.BedTool(bedFile1500)


#### DEFINE FUNCTIONS #####
    oligoC = 0
    oligoD = 0




#Processing current file for terminal output:
    now = datetime.now()
    print "Started processing file", fileBam, "at", now.strftime("%Y-%m-%d %H:%M:%S")
    
    
    
    
#total nr of reads is mapped + unmapped (if zero, an exception is required for calculating the percAlignment to prevent error)
    inputFileTotalReads = inputFile.mapped + inputFile.unmapped
    if inputFileTotalReads > 0:
        percAlignment =  ((1.0*inputFile.mapped)/inputFileTotalReads)*100
    else:
        percAlignment = "NA"

#nr of unmapped reads containing oligoC/D sequence (Georges used these strings for oligoC/D in previous analyses)
    for read in inputFile.fetch(until_eof=True):
        if read.is_unmapped:
            if 'CATTAAAAAA' in read.seq:
                oligoC += 1
            if 'CTTGAAAAAA' in read.seq:
                oligoD += 1


#On/Off target intersectbed (within 450bp or outside or 1500bp of capture probes (450bp region is searched within 1500bedtool (less sequences))
    now = datetime.now()
    print "Started processing bed1500 at", now.strftime("%Y-%m-%d %H:%M:%S")


    intersectBed = "intersectBed -abam " +bam+ " -b " +bedFile450+ " > " +fileBam[:-4]+"ontarget.bam"
    os.system(intersectBed)

    bam_bed1500 = pybedtools.BedTool(fileBam[:-4]+"ontarget.bam")

    bam_bed1500Count = bam_bed1500.count()

    now = datetime.now()
    print "Finished processing bed1500 at", now.strftime("%Y-%m-%d %H:%M:%S")



    now = datetime.now()
    print "Started processing bed450 at", now.strftime("%Y-%m-%d %H:%M:%S")

    bam_bed450 = bam_bed1500.intersect(bed450)
    bam_bed450Count = bam_bed450.count()

    now = datetime.now()
    print "Finished processing bed450 at", now.strftime("%Y-%m-%d %H:%M:%S")

    #On/Off target percentages

    if inputFile.mapped > 0:
        onTargetPerc450 = (1.0*bam_bed450Count)/inputFile.mapped*100
    else:
        onTargetPerc450 = "NA"

    if inputFile.mapped > 0:
        offTargetPerc1500 = (1.0*inputFile.mapped - bam_bed1500Count)/inputFile.mapped*100
    else:
        offTargetPerc1500 = "NA"

#####OUTPUT######## print to the output file
    print >> outputFile, fileBam,'\t', inputFileTotalReads,'\t', inputFile.mapped,'\t', inputFile.unmapped,'\t', percAlignment,'\t', oligoC,'\t', oligoD,'\t', bam_bed450Count,'\t', onTargetPerc450,'\t', inputFile.mapped-bam_bed1500Count,'\t', offTargetPerc1500,'\t'


#cleanup and close files
outputFile.close()
pybedtools.cleanup()

#finishing logfile
now = datetime.now()
print >> logFile, "Date and time when script was finished:", now.strftime("%Y-%m-%d %H:%M")
logFile.close()












