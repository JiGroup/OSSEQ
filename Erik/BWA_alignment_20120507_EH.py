#!/usr/bin/env python

#  BWA alignment for paired end reads
#  
#
#  Created by Erik Hopmans on 05/7/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####
import os
import sys


##### INPUTS AND OUTPUTS #####
refGenome = "/opt/references/human_g1k_v37.fasta"   #location of reference genome (toro)
proc = "10"                                         #nr of processors to use for alignment


##### DEFINE FUNCTIONS #####



##### SCRIPT #####

p1_fq = sys.argv[1]
p2_fq = sys.argv[2]
if p1_fq[-6:] != ".fastq" or p2_fq[-6:] != ".fastq":
    print "Exception occurred! Script expects input files to .fastq files"
    break


p1_sai = p1_fq.split(".fastq")[0] + ".sai"
p2_sai = p2_fq.split(".fastq")[0] + ".sai"
out_sam = p1_fq.split(".fastq")[0] + ".sam"



aln_p1 = "nice bwa aln -t proc -f "+p1_sai+" "+refGenome+" "+p1_fq
aln_p2 = "nice bwa aln -t proc -f "+p2_sai+" "+refGenome+" "+p2_fq

#cmd_aln1 = "nice bwa aln -t 10 -f p1.sai /opt/references/human_g1k_v37.fasta p1.fq"
os.system(aln_p1)
os.system(aln_p2)

merge = "nice bwa sampe -f"+out_sam+" "+refGenome+" "+p1_sai+" "+p2_sai+" "+p1_fq+" "+p2_fq
os.system(merge)