#!/usr/bin/env python

#  
#  
#
#  Created by Erik Hopmans on 06/19/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####
import pybedtools


##### INPUTS AND OUTPUTS #####
bam = pybedtools.BedTool(argv1)
bed = pybedtools.BedTool('/mnt/cluster2-analysis/Data/Reference_and_Resources/Bed_files/OS0007_JamesBond_450cov.st.collapsed.bed')

##### DEFINE FUNCTIONS #####





##### SCRIPT #####

bam_bed = bam.intersect(bed)   #This command equals bash "intersectBed -abam file.bam -b file.bed"
