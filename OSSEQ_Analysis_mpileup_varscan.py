 #!/usr/bin/env python

# OSSEQ_Analysis_mpileup_varscan v1.0
#
#
#  Created by Erik Hopmans on 08/24/12.
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
logFile = open(sys.argv[1][:-4]+".pileupVarscanLOG.txt", 'w')
print >> logFile, "Script was run by user:", getpass.getuser()
print >> logFile, "Name of the script:", __file__
print >> logFile, "Date and time when script was started:", now.strftime("%Y-%m-%d %H:%M")
print >> logFile, "Input file of this script:", sys.argv[1]
print >> logFile, "Description of output data: .ontarget.bam & pileup files and varscan analysis of SNP and indels"



##### SCRIPT #####


f=csv.reader(open(sys.argv[1], 'rU'), dialect=csv.excel_tab)
for row in f:
    pathBam = row[0]
    fileBam = row[1]
    pathBed = row[2]
    fileBed = row[3]
    bam = pathBam+fileBam
    bedFile = pathBed+fileBed


#Check if input files are correct, skip p2 files, check if input files are bam and bed files
    if "p2." in fileBam:
        continue
    if bam[-4:] != ".bam":
        sys.exit("ERROR in load file! The bam file is expected to be in the bam file format")
    if bedFile[-4:] != ".bed":
        sys.exit("ERROR in load file! The bed file is expected to be in the bed file format")

#IntersectBed and subsequently do a mpileup on the intersected bam files. Next varscan is performed on the mp files. Filenames for output file are created by taking the input bamfile name (fileBam) and replacing the .bam extension with .ontarget.bam and subsequently .mp for the pileup, snp.out and ind.out for varscan. in mpileup -B does not automatically change phred scores close to indels (keeps sequencer phred scores); -d100000000 to prevent stopping pileup after a depth of 8000 (autosetting); -f to add reference genome.

    now = datetime.now()
    print "Started processing file", fileBam, "at", now.strftime("%Y-%m-%d %H:%M:%S")
    print "Started processing bed at", now.strftime("%Y-%m-%d %H:%M:%S")

    intersectBed = "intersectBed -abam " +bam+ " -b " +bedFile+ " > " +fileBam[:-4]+".ontarget.bam"
    os.system(intersectBed)


    now = datetime.now()
    print "Started processing pileup at", now.strftime("%Y-%m-%d %H:%M:%S")

    samPileUp = "samtools mpileup  -B -d100000000  -f  /mnt/cluster2-analysis/Data/Reference_and_Resources/genomes/human_g1k_v37/human_g1k_v37.fasta " +fileBam[:-4]+".ontarget.bam > "+fileBam[:-4]+".ontarget.mp"
    os.system(samPileUp)


    now = datetime.now()
    print "Started processing varScan SNP at", now.strftime("%Y-%m-%d %H:%M:%S")

    varscanSNP = "java -jar /opt/VarScan.v2.3.3.jar mpileup2snp "+fileBam[:-4]+".ontarget.mp --output-vcf 1 > " +fileBam[:-4]+".ontarget.snp.out.vcf"
    os.system(varscanSNP)


#finishing logfile
    print >> logFile, "Output files of this script:", fileBam[:-4]+".ontarget.bam/.ontarget.mp/.ontarget.snp.out.vcf"



 
now = datetime.now()
print >> logFile, "Date and time when script was finished:", now.strftime("%Y-%m-%d %H:%M")
logFile.close()












