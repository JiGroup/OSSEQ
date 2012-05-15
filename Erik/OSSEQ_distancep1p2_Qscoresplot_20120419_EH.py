#!/usr/bin/env python

#  Goal: Script will create a figure of the average Q-score of a read plotted against the distance between p1 and p2 of that read.
#    
#  Input: It assumes p1 and p2 samfiles sorted on name (samtools sort -n) for input. 
#  
#
#  Created by Erik Hopmans on 04/19/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####
from matplotlib import pyplot as plt
import numpy as np
import pylab
import sys

##### INPUTS AND OUTPUTS #####
p1File = sys.argv[1]
p2File = sys.argv[2]
phredMinus = 33



##### DEFINE FUNCTIONS #####

# short_file removes the header and prints every 1000th line to a new file
def short_file(file):
    
    inFile = open(file, 'r')
    fileOut = file.split(".sam")[0] + ".short.sam"
    outFile = open(fileOut, 'w')
    i = 0
    
    for line in inFile:
        if line.startswith( "@" ):         #Skip the header lines (start with @)
            continue  
        i = i + 1
        if i == 1000:                          
            outFile.write(line) 
        if i == 1000:                         
            i = 0    
    inFile.close()
    outFile.close()


#turn samfile ASCII QC string into Phred Q score values and return the average
def Q_Ascii_Phred(q):    
    QC = [ord(x)-phredMinus for x in list(q)]          #ord command changes ASCII into number
    QC = QC[:-1]                                        #removes the new line character at the end of each line
    average = float(sum(QC)) / len(QC)
    return average
    

##### SCRIPT #####


short_file(p1File) # Create shorter files for data analysis
short_file(p2File)

p1In = open(p1File.split(".sam")[0] + ".short.sam", 'r') #open the shorter file
p2In = open(p2File.split(".sam")[0] + ".short.sam", 'r')
output_file = open(p1File.split(".sam")[0] + ".dist.sam", 'w')

while 1:
    p1Line = p1In.readline()            #loop: read line by line
    p2Line = p2In.readline() 
    if not p1Line: 
        break                #if no lines are left stop loop
    
    p1Tabs = p1Line.split('\t')         #this splits the line with tabs
    p2Tabs = p2Line.split('\t')    
    
    if p1Tabs[3] == '0' or p2Tabs[3] == '0':                 #skip the lines that are not mapped (field 4 =0)
        continue

    p1Pos = int(p1Tabs[3])              #calculate pos and insert length
    p2Pos = int(p2Tabs[3])
    p1Length = len(p1Tabs[9])
    p2Length = len(p2Tabs[9])
    distance = p2Pos - p1Pos
    if distance >= 0:                         # | = r1/2_pos; p1/2---> = read; cccc =40bp capture probe p2! 
        distance = distance + p2Length -40    #  |p1---->_____________|<----ccccp2
    elif distance < 0:
        distance = (distance*-1) + p1Length -40    #  |p2cccc---->_________|<-----p1

    if distance > 2000:                #skip the lines in which p1 and 2 do not align within 2000bp of each other
        continue

    qAverage = Q_Ascii_Phred(p1Tabs[10])    #skip the lines with a average Q score below 20
    if qAverage < 20:
        continue

    if p1Tabs[0] != p2Tabs[0]:          #Checks if p1 and p2 reads are still correctly aligned: QC step  
        print "p1 and p2 files are not sorted correctly, please make sure the input SAM files were sorted with 'samtools sort -n'!"
        break                         

    
    

    print >> output_file, distance, qAverage, p1Tabs[0] 

#close files
p1In.close()
p2In.close()
output_file.close()


#sort on insert size
output_file2 = open(p1File.split(".sam")[0] + ".dist.srt.sam", 'w')
sortList = [line.strip() for line in open(p1File.split(".sam")[0] + ".dist.sam")] 
sortList.sort(key=lambda line: int(line.split(" ")[0]))     #Why do I need the line strip part in the line above, doesn't this do the same thing as this line?
for line in sortList:
    print >> output_file2, line

output_file2.close()

###############################################################
#plotting

with open((p1File.split(".sam")[0] + ".dist.srt.sam"), 'r') as f:    
    X = np.loadtxt(f, dtype='float', comments="#", skiprows=0, usecols=[0])
with open((p1File.split(".sam")[0] + ".dist.srt.sam"), 'r') as f:
    Y = np.loadtxt(f, dtype='float', comments="#", skiprows=0, usecols=[1])     # TODO: why does nploadtxt close the file??


plt.plot(X, Y, 'o')
plt.xlabel('Insert length p1 p2')
plt.ylabel('Average Q score per read')
plt.title('OSSEQ distance vs quality')
plt.grid(True)
# calc the trendline (it is simply a linear fitting)
z = np.polyfit(X, Y, 1)
p = np.poly1d(z)
plt.plot(X,p(X),"r--")
# the line equation:
#print "y=%.6fx+(%.6f)"%(z[0],z[1])

plt.savefig(p1File.split(".sam")[0] + ".distance_Qscore.png")
#plt.show()
        

