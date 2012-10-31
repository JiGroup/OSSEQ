#!/usr/bin/env python

#
#
#
#  Created by Erik Hopmans on 10/30/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####
import sys
import csv
import pysam
import pybedtools
from datetime import datetime
import getpass

##### INPUTS AND OUTPUTS #####
now = datetime.now()

#Creating outputfile with inputfileOUTPUT name and header line
outputFile =  open(sys.argv[1][:-4]+"OUTPUT.txt", 'w')
print >> outputFile, "Filename",'\t',"Reads:",'\t',"Mapped Reads:",'\t',"NonMapped Reads",'\t',"% Align",'\t',"OligoC in NM",'\t',"OligoD in NM",'\t',"On target",'\t',"% On Target",'\t',"Off Target",'\t',"% Off Target",'\t'

#### DEFINE FUNCTIONS #####

def percentCalc(number, divisor):
    if divisor > 0:
        percentage =  ((1.0*number)/divisor)*100
    else:
        percentage = "NA"
    return percentage

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
       
    # Open bam files and bed files for processing
    inputFile = pysam.Samfile(bam, 'rb')
    bedtool = pybedtools.BedTool(bam)
    bed450 = pybedtools.BedTool(bedFile450)
    bed1500 = pybedtools.BedTool(bedFile1500)
    
    



    
    
    #total nr of reads is mapped + unmapped (if zero, an exception is required for calculating the percAlignment to prevent error)
    percAlignment = percentCalc(inputFile.mapped, inputFile.mapped+inputFile.unmapped)

    #nr of unmapped reads containing oligoC/D sequence (Georges used these strings for oligoC/D in previous analyses)
    oligoC = 0
    oligoD = 0

    for read in inputFile.fetch(until_eof=True):
        if read.is_unmapped:
            if 'CATTAAAAAA' in read.seq:
                oligoC += 1
            if 'CTTGAAAAAA' in read.seq:
                oligoD += 1
    
    
    #On/Off target intersectbed (within 450bp or outside or 1500bp of capture probes (450bp region is searched within 1500bedtool (less sequences))
  
    bam_bed1500 = bedtool.intersect(bed1500)
    bam_bed1500Count = bam_bed1500.count()
  
    bam_bed450 = bam_bed1500.intersect(bed450)
    bam_bed450Count = bam_bed450.count()
    

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





