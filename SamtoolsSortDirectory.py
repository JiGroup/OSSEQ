#!/usr/bin/env python

#  SamtoolsSortDirectory.py
#  
#
#  Created by Erik Hopmans on 10/10/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####

import os
import glob



##### INPUTS AND OUTPUTS #####






##### DEFINE FUNCTIONS #####





##### SCRIPT #####

path = './'
for infile in glob.glob( os.path.join(path, '*.bam') ):    
    samtoolsSort = "samtools sort "+infile+" "+infile[:-4]+".st"
    os.system(samtoolsSort)
    