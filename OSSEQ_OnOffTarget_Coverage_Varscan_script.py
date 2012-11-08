#!/usr/bin/env python

#
#
#
#  Created by Erik Hopmans on 10/30/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####
import numpy as np
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


#Calculate percentage: if divisor is zero, an exception is required to prevent exciting in error
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
    bed450 = pathBed+fileBed450
    bed1500 = pathBed+fileBed1500
       
    # Open bam files and bed files for processing
    inputFile = pysam.Samfile(bam, 'rb')
    bedtool = pybedtools.BedTool(bam)
    bed450 = pybedtools.BedTool(bed450)
    bed1500 = pybedtools.BedTool(bed1500)
    
    
    #nr of unmapped reads containing oligoC/D sequence (Georges used these strings for oligoC/D in previous analyses)
    oligoC = 0
    oligoD = 0
    for read in inputFile.fetch(until_eof=True):
        if read.is_unmapped:
            if 'CATTAAAAAA' in read.seq:
                oligoC += 1
            if 'CTTGAAAAAA' in read.seq:
                oligoD += 1
    
    
    #On/Off target intersectbed (within 450bp or outside or 1500bp of capture probes (450bp region is searched within 1500bedtool (more efficient theoretically due to less sequences))
  
    bam_bed1500 = bedtool.intersect(bed1500)
    bam_bed1500Count = bam_bed1500.count()
    bam_bed450 = bam_bed1500.intersect(bed450)
    bam_bed450Count = bam_bed450.count()
    

    #Calculate percentages
    percAlignment = percentCalc(inputFile.mapped, inputFile.mapped+inputFile.unmapped)
    onTargetPerc450 = percentCalc(bam_bed450Count, inputFile.mapped)
    offTargetPerc1500 = percentCalc(inputFile.mapped-bam_bed1500Count, inputFile.mapped)

    
    #####OUTPUT######## print to the output file
    print >> outputFile, fileBam,'\t', inputFile.mapped+inputFile.unmapped,'\t', inputFile.mapped,'\t', inputFile.unmapped,'\t', percAlignment,'\t', oligoC,'\t', oligoD,'\t', bam_bed450Count,'\t', onTargetPerc450,'\t', inputFile.mapped-bam_bed1500Count,'\t', offTargetPerc1500,'\t'


#This next part should typically only be for p1 files, not for p2 files.

#Check if input files are correct, skip p2 files, check if input files are bam and bed files
    if "p2." in fileBam:
        continue
##TODO: Maybe it is better to check if the file is p1? Optimally all the output is created at then end in 1 print line


#Do a coverage bed of the p1 bam files vs the bed450 files. -d option is for reporting the depth in each position present in the Bed file. Subsequently run John's total_up_cov_by_regions.pl script by loading the just created cov.out as an argument in the command.

    coverageBed = "coverageBed -d -abam " +bam+ " -b " +bed450+ " > " +fileBam[:-4]+".cov.out"
    os.system(coverageBed)

##TODO: implement coveragebed from pybedtools and test
#cov.out = bam.coverage(bed450, '-d').saveas(fileBam[:-4]+".cov.out")
#
    perlCovRegions = "perl total_up_cov_by_region.pl "+fileBam[:-4]+".cov.out"
    os.system(perlCovRegions)


##TODO: is there a way to do this directly from cov.out instead of reopening the file, pipe directly from coveragebed into numpy?
covOutFile = open(fileBam[:-4]+".cov.out", 'r')
coverage = np.loadtxt(covOutFile, skiprows=0, usecols=[4])
print >> outputFile, file,'\t',np.average(coverage),'\t',np.std(coverage)





#cleanup and close files
outputFile.close()
pybedtools.cleanup()






