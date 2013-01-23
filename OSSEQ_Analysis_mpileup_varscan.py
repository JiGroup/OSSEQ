 #!/usr/bin/env python

# OSSEQ_Analysis_mpileup_varscan v1.5
#   
#   Script performs intersectBed to determine on target regions, performs mpileup, which it uses to determine SNP in on target regions
#   Input file is tab delimited text file with column 1: path to bam file; 2 bam file name; 3 path to bed file; 4 bed file name
#  
#  Created by Erik Hopmans on 08/24/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

import os, sys, csv, getpass
from datetime import datetime
from subprocess import Popen, PIPE

#Aji program locations:
humanFasta = "/mnt/cluster2-analysis/Data/Reference_and_Resources/genomes/human_g1k_v37/human_g1k_v37.fasta"
varScanApp = "/opt/VarScan.v2.3.3.jar"



#Call shell command and pipe the command output (to stderr) into the logfile:
def shell_command(command, logFile):                   
    pp = Popen(command, shell=True, stderr=PIPE)
    stderr = pp.communicate()
    print >> logFile, stderr



# MAIN PROGRAM #
#Ensure that valid input files are provided in input file
f=csv.reader(open(sys.argv[1], 'rU'), dialect=csv.excel_tab)
for row in f:
    pathBam = row[0]
    fileBam = row[1]
    pathBed = row[2]
    fileBed = row[3]
    bam = pathBam+fileBam
    bedFile = pathBed+fileBed
    
    
    
    
    
    if fileBam[-4:] != '.bam':
        print "File does not have the right extension and will not be analyzed:", fileBam
        continue
    elif fileBed[-4:] != '.bed':
        print "File does not have the right extension and associated bam file will not be analyzed:", fileBed, fileBam
        continue    

    try:
        log = fileBam.replace('bam', 'mpVarLOG.txt')
        logFile = open(log, 'w')
    except:
        print "Unable to open output file, write permissions OK? ", logFile
        sys.exit(1)
    
    #Creation of logfile
    now = datetime.now()
    print "Started processing file", fileBam, "at", now.strftime("%Y-%m-%d %H:%M:%S")  
    print >> logFile, "Script was run by user:", getpass.getuser()
    print >> logFile, "Name of the script:", __file__
    print >> logFile, "Name of bam and bed file being processed:"
    print >> logFile, bam
    print >> logFile, bedFile
    print >> logFile, "Date and time when file processing  was started:", now.strftime("%Y-%m-%d %H:%M")
    print >> logFile, "Input file of this script:", sys.argv[1]
    print >> logFile, "Description of output data: ontarget.bam & mp & snp.out.vcf files"
    
  
    intersectBed = "intersectBed -abam "+bam+" -b "+bedFile+" > "+bam.replace("bam", "ontarget.bam")
    shell_command(intersectBed, logFile)

    samPileUp = "samtools mpileup  -B -d100000000  -f "+humanFasta+" "+bam.replace("bam", "ontarget.bam")+" > "+bam.replace("bam", "mp")
    shell_command(samPileUp, logFile)


    varScan = "java -jar "+varScanApp+" mpileup2snp "+bam.replace("bam", "mp")+" --output-vcf 1 > " +bam.replace("bam", "snp.out.vcf")
    shell_command(varScan, logFile)

    logFile.close()

 
now = datetime.now()
print "Date and time when script was finished:", now.strftime("%Y-%m-%d %H:%M")










