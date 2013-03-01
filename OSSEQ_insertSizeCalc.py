#!/usr/bin/env python

#  OSSEQ_NatBiotech_SizeFiltering.py
#  
# Uses the p1 and p2 sam files (sorted on -n) as command line input files, and keeps following reads:
#   -reads within 1KB and not overlapping the capture probe
#   -both reads are aligned 
#   -both reads are on same chromosome
#
#  Created by Erik Hopmans on 11/23/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####
import sys, os, glob



##### INPUTS AND OUTPUTS #####






##### DEFINE FUNCTIONS #####


def flag(i): 
    return list((0,1)[i>>j & 1] for j in xrange(11-1,-1,-1)) 
    #Returns a list of the flag values: 1 (description is TRUE) or 0 (discription is FALSE), 
    #with bit 0x1 being the last number and 0x400 being the first in the list
    #(Got his from a forum, don't know how, but is works :) )
    # Bit    Description
    # 0x1    template having multiple segments in sequencing
    # 0x2    each segment properly aligned according to the aligner
    # 0x4    segment unmapped
    # 0x8    next segment in the template unmapped
    # 0x10   SEQ being reverse complemented
    # 0x20   SEQ of the next segment in the template being reversed
    # 0x40   the rst segment in the template
    # 0x80   the last segment in the template
    # 0x100  secondary alignment
    # 0x200  not passing quality controls                               
    # 0x400  PCR or optical duplicate  


##### SCRIPT #####

path = './'
for infile in glob.glob( os.path.join(path, 'p1.*.sam') ):    
    p1SamFile = open(infile,'r')
    p2Sam = infile.replace('p1', 'p2')
    p2SamFile = open(p2Sam,'r')
    p1SamFileInsert = infile.replace('sam', 'InsertSize.txt')
    p1SamInsert =  open(p1SamFileInsert, 'w')

    while True:
        p1Line = p1SamFile.readline()
        p2Line = p2SamFile.readline()
        if p1Line.startswith( "@" ):         #Skip the header lines (start with @)
            continue  
        if not p1Line: 
            break

        p1Tab = p1Line.split('\t')
        p2Tab = p2Line.split('\t')
        p1Flag = int(p1Tab[1])
        p2Flag = int(p2Tab[1])
        p1Len = len(p1Tab[9])
        p2Len = len(p2Tab[9])
        p1Pos = int(p1Tab[3])
        p2Pos = int(p2Tab[3])
    
        if p1Tab[0] != p2Tab[0]:
            sys.exit("Error: p1 and p2 samfiles are not sorted correctly or are not paired")
        

        if flag(p1Flag)[8] == 1 or flag(p2Flag)[8] == 1: #filter out if one of the reads is unmapped
            continue

        if p1Tab[2] != p2Tab[2]:        #filter out if reads are on different chromosomes
            continue

        def insertsize():
            dist = 0
            if flag(p1Flag)[6] == 0 and flag(p2Flag)[6] == 1: #read 1 is on positive strand, read 2 on reverse/negative strand
                dist = p2Pos-(p1Pos+p1Len) 
            elif flag(p1Flag)[6] == 1 and flag(p2Flag)[6] ==0: #read 1 is on reverse/negative strand, read 2 on positive strand 
                dist = p1Pos-(p2Pos+p2Len)
            return dist

        if insertsize() > 0 and insertsize() < 1000:
            print >> p1SamInsert, insertsize()


    p1SamFile.close()
    p2SamFile.close()
    p1SamInsert.close()


##TODO: in def insertsize, if read 1+2 are mapped on the same strand, I don't know what will happen, not really clean
