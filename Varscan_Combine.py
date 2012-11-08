#!/usr/bin/env python

# Varscan_combine.py takes all varscan files (based on ".out" extension) in the directory, combines the variants in each file into 1 combined table
# It creates 2 types of files for this: the final file (infile.csv
###TODO: explean more clearly
##TODO: rename filenames to make them better understandable
#  Created by Erik Hopmans on 11/6/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####
import csv
import sys
import os

#########################################             PART 1                ############################################################
##### INPUTS AND OUTPUTS #####


#Creating the infile Header:
headers = [x for x in os.listdir('.') if x.endswith('.out')] #List the files ending with '.out' in the directory
outputfile = open('infile.csv', 'wb')
outwriter =  csv.writer(outputfile, delimiter=',')
outwriter.writerow(['Chrom_position'] + ['RefBase']+headers)



##### SCRIPT #####

#Iterate through the snp.out files: create the infile.csv that has all chrompos in there and create the outtemp.csv files for each snp.out file to use as a dictionary in part2


for fname in os.listdir('.'):
    if fname.endswith('.out'):
        checkfile = open(fname+'.outtemp.csv', 'wb')        #Create Header for checkfiles
        checkwriter =  csv.writer(checkfile, delimiter=',')
        checkwriter.writerow(['Chrompos'] + ['varBase'])

        with open(fname) as f:                                 #iterate through snp.out files
            for line in f:
                if line.startswith("Chrom"):
                    continue
                tab = line.split('\t')
                pos = tab[0]+"_"+tab[1]
                refBase = tab[2]
                varBase = tab[3]
                checkwriter.writerow([pos] + [varBase])        #add chrompos+varbase to snp.out.outtemp.csv file
                outwriter.writerow([pos] + [refBase])           #Add chrom pos + refbase to infile
        checkfile.close()
outputfile.close()

#Sort and keep unique locations with shell code
sortUnique = "cat infile.csv | sort -n | uniq > infile2.csv"
os.system(sortUnique)





#########################################             PART 2                ############################################################
#This part is basically a similar function as excels vlookup, it creates a dict(ionary) named "checkfile" in which it searches for a specific value (comparable to the table in which excels vlookup searches)

##### INPUTS AND OUTPUTS #####
infile2 = "infile2.csv"

for fname in os.listdir('.'):
    if fname.endswith('.outtemp.csv'):
        outputColumn = fname[:-12]

	# Open the check file in a context manager. This ensures the file will be closed
	# correctly if an error occurs.EH: Adapted from http://codereview.stackexchange.com/questions/7113/searching-a-value-from-one-csv-file-in-another-csv-file-python
	with open(fname, 'rb') as checkfile:                          
		checkreader = csv.DictReader(checkfile)
		
		
		# This does the real work. The middle line is a generator expression which
		# iterates over each line in the check file. The base code and stock
		# level are extracted from each line. This is then converted
		# into a dictionary. This dictionary has the base codes as its keys and
		# their result code as its values.
		varBase = dict(
							  (v['Chrompos'], v['varBase']) for v in checkreader
							  )
	
	# Open the input and output files.
	with open(infile2, 'rb') as infile:
		with open('outfile.csv', 'wb') as outfile:
			reader = csv.DictReader(infile)
			# Use the same field names for the output file.
			writer = csv.DictWriter(outfile, reader.fieldnames)
			#writer = csv.DictWriter(outfile, fieldnames=('StockNumber', 'SKU', 'ChannelProfileID'), delimiter=',')
			writer.writeheader()
			
			# Iterate over the bases in the input.
			for base in reader:
				# Find the stock level from the dictionary we created earlier. Using
				# the get() method allows us to specify a default value if the SKU
				# does not exist in the dictionary.
				result = varBase.get(base['Chrom_position'], " ")
				
				# Update the base info.
				base[outputColumn] = result
				
				# Write it to the output file.
				writer.writerow(base)
	os.rename("outfile.csv", "infile2.csv")	




#Cleanup
os.remove("infile.csv"+)
