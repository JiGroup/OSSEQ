#!/usr/bin/env python

# Varscan_combine.py takes all varscan files (based on ".out" extension) in the directory, combines the variants in each file into 1 combined table
#
#
#  Created by Erik Hopmans on 11/6/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####
import csv
import sys
import os

#########################################             PART 1                ############################################################
##### INPUTS AND OUTPUTS #####

outputFile = open("temp", "w")
headers = [x for x in os.listdir('.') if x.endswith('.out')] #List the files ending with '.out' in the directory
print >> outputFile, "Chrom_position",'\t',"Refbase",'t','\t'.join(headers) #Create Header (it would probably be better to add this after the sort unique step with something like http://stackoverflow.com/questions/3162314/add-headers-to-a-file )



##### SCRIPT #####
#Creates a list of all the first 3 columns of the varscan files (chrom, position (combined to 1: chrom_position) and reference base), subsequently sort this list and retain the unique variant positions (by using shell sort and uniq commands)


for fname in os.listdir('.'):
    if fname.endswith('out'):
        outTemp = open(fname+".outtemp.txt", 'w')
        print >> outTemp, "ChromPosition",'\t',"VarBase"
        with open(fname) as f:
            for line in f:
                if line.startswith("Chrom"):
                    continue
                tab = line.split('\t')
                pos = tab[0]+"_"+tab[1]
                print >> outputFile, pos,'\t',tab[2]
                print >> outTemp, pos,'\t',tab[2]
        outTemp.close()

outputFile.close()

sortUnique = "cat temp | sort -n | uniq > temp2.txt"
os.system(sortUnique)


#####################















#Cleanup
os.remove("temp")











#########################################             PART 2                ############################################################
#This part is basically a similar function as excels vlookup, it creates a dict(ionary) in which it searches for a specific value (comparable to the table in which excels vlookup searches)

##### INPUTS AND OUTPUTS #####
#infile = "temp2.txt"
#
#for fname in os.listdir('.'):
#    if fname.endswith('.outtemp.txt'):
#        outputColumn = fname
#

fname = "20120309_SG1_0121.c1_p1.good.stontarget.snp.out.outtemp.txt"
outputColumn = fname
# Open the check file in a context manager. This ensures the file will be closed
# correctly if an error occurs.EH: Adapted from http://codereview.stackexchange.com/questions/7113/searching-a-value-from-one-csv-file-in-another-csv-file-python
with open('checkfile_tab2.txt', 'rU') as checkfile:                          # It is important to use rU = universal read mode, prevents errors due to delimeters
    checkreader = csv.DictReader(checkfile, delimiter='\t')
    
    
    # This does the real work. The middle line is a generator expression which
    # iterates over each line in the check file. The base code and stock
    # level are extracted from each line. This is then converted
    # into a dictionary. This dictionary has the base codes as its keys and
    # their result code as its values.
    varBase = dict(
                          (v['ChromPos'], v['VarBase']) for v in checkreader
                          )

# Open the input and output files.
with open("temp2.txt", 'rU') as infile:
    with open('outfile.csv', 'wb') as outfile:
        reader = csv.DictReader(infile, delimiter='\t')
        # Use the same field names for the output file.
        writer = csv.DictWriter(outfile, reader.fieldnames)
        #writer = csv.DictWriter(outfile, fieldnames=('StockNumber', 'SKU', 'ChannelProfileID'), delimiter=',')
        writer.writeheader()
        
        # Iterate over the bases in the input.
        for base in reader:
            # Find the stock level from the dictionary we created earlier. Using
            # the get() method allows us to specify a default value if the SKU
            # does not exist in the dictionary.
            result = varBase.get(base['Chrom_position'], "-")
            
            # Update the base info.
            base[outputColumn] = result
            
            # Write it to the output file.
            writer.writerow(base)