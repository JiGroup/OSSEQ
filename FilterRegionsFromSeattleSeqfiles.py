#!/usr/bin/env python

# Filters SeattleSeq output files for regions of interest (chrom and start to end positions)
#   usage: requires 5 arguments on commandline seperated by spaces: input file, chrom of region of interest, start pos, end pos, name for output file (e.g. region)  
#  
#
#  Created by Erik Hopmans on 02/11/13.
#  Copyright (c) 2013 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####
import sys, csv



##### INPUTS AND OUTPUTS #####
input = sys.argv[1]
chrom = sys.argv[2]
start = sys.argv[3]
end = sys.argv[4]
region = sys.argv[5]

notIndbSNP = 0
indbSNP = 0
rownum = 0
##### DEFINE FUNCTIONS #####





##### SCRIPT #####
with open(input, 'rb') as f:
    reader =csv.reader(f, dialect='excel-tab')
    with open(region+_+input, 'wb') as output:
        writer = csv.writer(output, dialect='excel-tab')
        for row in reader:
            if "#" in row[1]:
                next(reader)
            elif row[1] == chrom and row[2]>=start and row[2]<=end:
#                 if row[0] == "none":
#                     notIndbSNP +=1
#                 else:
#                     indbSNP +=1
                writer.writerow(row)        
#         writer.writerow("SNPs not in dbSNP:" notIndbSNP)
#         writer.writerow("SNPs in dbSNP:" indbSNP)
