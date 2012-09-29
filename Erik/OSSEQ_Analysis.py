#!/usr/bin/env python

#
#
#
#  Created by Erik Hopmans on 08/24/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####
import sys
import pysam
import pybedtools


##### INPUTS AND OUTPUTS #####
bam = sys.argv[1]
if bam[-4:] != ".bam":
    print "ERROR! The input file is expected to be in the bam file format"

samfile = pysam.Samfile(bam, 'rb')
bedtool = pybedtools.BedTool(bam)


bed450 = pybedtools.BedTool('/mnt/cluster2-analysis/Data/Reference_and_Resources/Bed_files/OS0007_JamesBond_450cov.st.collapsed.bed')
bed1500 = pybedtools.BedTool('/mnt/cluster2-analysis/Data/Reference_and_Resources/Bed_files/OS0007_JamesBond_1500cov.st.collapsed.bed')

#/mnt/cluster2-analysis/Data/Run_Directories/20120309_SG1_0121/Analysis/Alignment/bam/20120309_SG1_0121.c1_p1.st.bam

##### DEFINE FUNCTIONS #####
totalReads = 0
totalAligningReads = 0



##### SCRIPT #####

#total nr of reads
samfileTotalReads = samfile.mapped + samfile.unmapped

print "Total nr of mapped Reads:", samfile.mapped
print "Total nr of unmapped Reads:", samfile.unmapped
print "Total nr of Reads:", samfileTotalReads

percAlignment =  ((1.0*samfile.mapped)/samfileTotalReads)*100

print "Percentage Alignment:", percAlignment,"%"

#################################################################################################################################################
#On target (within 450bp of capture probes)
bam_bed450 = bedtool.intersect(bed450).count()

print "Nr of reads on target", bam_bed450

onTargetPerc450 = (1.0*bam_bed450)/totalAligningReads*100

print "Percentage On target:", onTargetPerc450,"%"

#Off target (outside 1500bp of capture probes)

bam_bed1500 = bedtool.intersect(bed1500).count
offTargetPerc1500 = (1.0*(totalAligningReads-bam_bed1500))/totalAligningReads*100

print "Percentage Off target:", offTargetPerc1500,"%"

#I tried to first do an intersectbed on the bed1500, followed by an intersectbed on that subset with bed450 to increase efficiency, however I get an error that seems to be a bedtools bug

#Qscores and Q score drop? #TODO




#Which file was analyzed, when, with what version of script, by whom? #TODO



#####OUTPUT########




