#!/usr/bin/env python

#  
#  
#
#  Created by Erik Hopmans on 06/19/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####
import pybedtools
import sys

##### INPUTS AND OUTPUTS #####
bam = pybedtools.BedTool('/Users/erikhopmans/Documents/DATA-ANALYSIS/Programming/BEDtools_testfiles/sample.bam')
bed450 = pybedtools.BedTool('/Users/erikhopmans/Documents/DATA-ANALYSIS/Programming/BEDtools_testfiles/one_region.bed')
bed1500 = pybedtools.BedTool('/Users/erikhopmans/Documents/DATA-ANALYSIS/Programming/BEDtools_testfiles/one_region.bed')
##### DEFINE FUNCTIONS #####





##### SCRIPT #####

bam_bed450 = bam.intersect(bed450).count()
bam_bed1500 = bam.intersect(bed1500).count()
bamCount = bam.count()

OnTargetPercent = float(bam_bed450)/bamCount*100
OffTargetPercent =  float(bam_bed1500)/bamCount*100



print OnTargetPercent, OffTargetPercent