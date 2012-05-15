
from collections import defaultdict
from matplotlib import pyplot as plt
import numpy as np
import pylab



with open(('/Users/erikhopmans/Documents/DATA-ANALYSIS/Programming/TESTAREA/p1.st.dist.srt.sam'), 'r') as f:    
    test = np.loadtxt(f, dtype='int', comments="#", skiprows=0, usecols=[0])

          
          

d = defaultdict(int)
for item in test:
    d[item] += 1




plt.plot(X, Y, key=lambda line: int(line.split(":")[0, 1]))
plt.show()
