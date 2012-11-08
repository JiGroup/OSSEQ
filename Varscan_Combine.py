#!/usr/bin/env python

#
#
#
#  Created by Erik Hopmans on 11/6/12.
#  Copyright (c) 2012 Ji Research Group - Stanford Genome Technology Center. All rights reserved.

##### IMPORT MODULES #####




##### INPUTS AND OUTPUTS #####






##### DEFINE FUNCTIONS #####





##### SCRIPT #####

import csv
outputcolumn = 'test'



# Open the check file in a context manager. This ensures the file will be closed
# correctly if an error occurs.EH: Adapted from http://codereview.stackexchange.com/questions/7113/searching-a-value-from-one-csv-file-in-another-csv-file-python
with open('checkfile_tab.txt', 'rU') as checkfile:                          # It is important to use rU = universal read mode, prevents errors due to delimeters
    checkreader = csv.DictReader(checkfile, delimiter='\t')
    
    
    # This does the real work. The middle line is a generator expression which
    # iterates over each line in the check file. The product code and stock
    # level are extracted from each line. This is then converted
    # into a dictionary. This dictionary has the product codes as its keys and
    # their result code as its values.
    product_result = dict(
                          (v['ProductCode'], v[' Stock']) for v in checkreader
                          )

# Open the input and output files.
with open('infile.csv', 'rb') as infile:
    with open('outfile.csv', 'wb') as outfile:
        reader = csv.DictReader(infile)
        # Use the same field names for the output file.
        writer = csv.DictWriter(outfile, reader.fieldnames)
        #writer = csv.DictWriter(outfile, fieldnames=('StockNumber', 'SKU', 'ChannelProfileID'), delimiter=',')
        writer.writeheader()
        
        # Iterate over the products in the input.
        for product in reader:
            # Find the stock level from the dictionary we created earlier. Using
            # the get() method allows us to specify a default value if the SKU
            # does not exist in the dictionary.
            result = product_result.get(product['SKU'], "-")
            
            # Update the product info.
            product[outputcolumn] = result
            
            # Write it to the output file.
            writer.writerow(product)