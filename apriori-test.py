import numpy as np
import itertools as itr
import collections

# Global Variables
final_counts = {}
#transactions_table=dict()
itemSet=set()
#Create a namedtuple class with names "a" "b" "c"
Entry = collections.namedtuple("Entry", ["itemset", "support_count"], verbose=False, rename=False) 
initialize_Entry= Entry(set(), 5)
table = list()
############################# Start of Helper Functions ###############################

def read_data_txt(file_path='ticdata2000.txt',data_size=(5822, 86)):
    ''' Read Training Data size=(5822, 86)'''
    # Prepare array for data
    data = np.zeros(data_size, dtype=np.dtype('U100'))
    
    # Read All The Data and fill the array
    datafile = open(file_path, 'r')
    
    i = 0
    
    for line in datafile:
        data[i] = [eval(val) if val.isnumeric() else val for val in line.split()]
        i += 1
    
    return data
    
def slice_attr(full_data, selected_index=47):
    # split for given index
    # selected_index -= 1
    return full_data[:, selected_index: selected_index+12]
    
def supportof(pat,dataSet):
	pat = set(pat)
	frequency = 0	
	for d in dataSet:
		ds = set(d)
		if pat.issubset(ds):
			frequency += 1
	
	return frequency

def create_itemSet(sliced_data): 
  global itemSet
  f= sliced_data
  for index in range (0,len(sliced_data)):
    data=sliced_data[index]
    for d in data: 
      itemSet.add(d)
  itemSet = set(sorted(itemSet))

def insert_table_entry(itemset,support_count):
  global table
  global Entry
  table.append(Entry(itemset=itemset,support_count=support_count))

      
############################# End of Helper Functions ###############################

# Main Program
SI = eval(input('Starting Index: '))
# support = eval(input('Enter Support: '))
# confidence = eval(input('Enter confidence: '))

data = read_data_txt(file_path='ticdata2000.txt',data_size=(5822, 86))
create_itemSet(slice_attr(data, SI))
print(itemSet)


for item in itemSet:
  #item=[item]
  insert_table_entry(item,supportof(item,slice_attr(data, SI)))
    
print(table)
