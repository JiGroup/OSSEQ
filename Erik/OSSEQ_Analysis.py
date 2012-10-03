#!/usr/bin/env python

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


##### INPUTS AND OUTPUTS #####
##TODO: make indicator for for where it is in the process.
##TODO: incorporate scriptinformation.py for outputlogfile of analysis
##TODO: All' 'NMs' 'NMs_oligoC' 'NMs_oligoD' 'Align' 'Align_on_target' 'Align_off_target'

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
    samfile = pysam.Samfile(bam, 'rb')
    bedtool = pybedtools.BedTool(bam)
    bed450 = pybedtools.BedTool(bedFile450)
    bed1500 = pybedtools.BedTool(bedFile1500)


##### DEFINE FUNCTIONS #####
    totalReads = 0
    totalAligningReads = 0
    oligoC = 0
    oligoD = 0


##### SCRIPT #####

#total nr of reads (if zero, an exception is required for calculating the percAlignment to prevent error)
    samfileTotalReads = samfile.mapped + samfile.unmapped
    if samfileTotalReads > 0:
        percAlignment =  ((1.0*samfile.mapped)/samfileTotalReads)*100
    else:
        percAlignment = "NA"

    for read in samfile.fetch(until_eof=True):
        if read.is_unmapped:
            if 'CATTAAAAAA' in read.seq:                     #Georges has used this sequence for oligoC/D in previous analyses
                oligoC += 1
            if 'CTTGAAAAAA' in read.seq:
                oligoD += 1

    print fileBam
    print "Total nr of mapped Reads:", samfile.mapped
    print "Total nr of unmapped Reads NM:", samfile.unmapped
    print "Total nr of Reads:", samfileTotalReads
    print "Percentage Alignment:", percAlignment,"%"

#
#First write everything in rows to file, then reload it and use zip to get it into columns:
#>>> my_list=[[1,2,3],[4,5,6],[7,8,9,10]]
#>>> print zip(*my_list)
#[(1, 4, 7), (2, 5, 8), (3, 6, 9)]




#################################################################################################################################################
##On target (within 450bp of capture probes)
#bam_bed450 = bedtool.intersect(bed450).count()
#
#print "Nr of reads on target", bam_bed450
#
#onTargetPerc450 = (1.0*bam_bed450)/totalAligningReads*100
#
#print "Percentage On target:", onTargetPerc450,"%"
#
##Off target (outside 1500bp of capture probes)
#
#bam_bed1500 = bedtool.intersect(bed1500).count
#offTargetPerc1500 = (1.0*(totalAligningReads-bam_bed1500))/totalAligningReads*100
#
#print "Percentage Off target:", offTargetPerc1500,"%"
#
##I tried to first do an intersectbed on the bed1500, followed by an intersectbed on that subset with bed450 to increase efficiency, however I get an error that seems to be a bedtools bug
#
##Qscores and Q score drop? #TODO
#



#Which file was analyzed, when, with what version of script, by whom? #TODO



#####OUTPUT########




