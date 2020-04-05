import numpy as np
import itertools as itr
# import pandas as pd


# Prepare array for data
data_86 = np.zeros((5822, 86))

# Read All The Data and fill the array
datafile = open('ticdata2000.txt', 'r')

i = 0

for line in datafile:
    data_86[i] = [eval(val) for val in line.split()]
    i += 1


#### Temporary Code ####
# Choose Starting Index

SI = eval(input('Starting Index: '))

print(SI)

# split for given index
data_12 = data_86[:, SI: SI+12]

# User Defined Support and Confidence
support = eval(input('Enter Support: '))
confidence = eval(input('Enter confidence: '))

#### Temporary Debugging Code ####
print('support is: {}\nconfidence is: {}'.format(support, confidence))

# Data with labeled items
data_12L = np.empty(data_12.shape, dtype=np.dtype('U100'))

# format numbers in each columns by column's number
for cInd in range(data_12.shape[1]):
    for rInd in range(data_12.shape[0]):
        # vs data_12[cInd][rInd]
        # print(str(int(data_12[rInd][cInd]))+'_'+ str(cInd))
        data_12L[rInd][cInd] =  str(int(data_12[rInd][cInd]))+'_'+ str(cInd)
        

#### Debugging code ####
# itemsets_2 = list(itr.permutations(range(1,12), 2))

# for pair in itemsets_2:
#     print (pair)

# Start Counting Items and their frequencies
itemsets1_count = {}

for cInd in range(data_12L.shape[1]):
    for rInd in range(data_12L.shape[0]):
        val = data_12L[rInd][cInd]
        if val in itemsets1_count.keys():
            itemsets1_count[val] += 1
        else:
            itemsets1_count[val] = 0

# find items with unsufficient support       
items_under_support = []
for item in itemsets1_count.keys():
    if (itemsets1_count[item] / data_12L.shape[0]) < support:
        items_under_support.append(item)

# remove items with unsufficient support
for item in items_under_support:
    del itemsets1_count[item]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        