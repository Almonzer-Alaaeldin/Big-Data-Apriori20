import numpy as np
import itertools as itr

# Global Variables
final_counts = {}
# ############################# Start of Helper Functions ###############################

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

def set_apart_attr(data):
    # Data with labeled items
    data_U = np.empty(data.shape, dtype=np.dtype('U100'))
    
    # format numbers in each columns by column's number
    for cInd in range(data.shape[1]):
        for rInd in range(data.shape[0]):
            data_U[rInd][cInd] =  str(int(data[rInd][cInd]))+'_'+ str(cInd)
       
    return data_U
    

def itemset_support(uniqueData, previous_itemsets=[], itemset_lvl=1):
    
    if itemset_lvl == 1:
        itemsets_count = {}
        for cInd in range(uniqueData.shape[1]):
            for rInd in range(uniqueData.shape[0]):
                val = uniqueData[rInd][cInd]
                if val in itemsets_count.keys():
                    itemsets_count[val] += 1
                else:
                    itemsets_count[val] = 1
                    
    elif itemset_lvl > 1:
        itemsets_count = {}
        for itemset in list(itr.combinations(previous_itemsets, itemset_lvl)):
            key = ','.join(itemset)
            itemsets_count[key] = 0
            items_exist_together = True
            
            for row in uniqueData:            
                for item in itemset:
                    if not item in row:
                        items_exist_together = False
                        break
                if items_exist_together:
                    itemsets_count[key] += 1
                
                items_exist_together = True
        
    # find items with unsufficient support       
    items_under_support = []
    for itemset in itemsets_count.keys():
        if float(itemsets_count[itemset]) / uniqueData.shape[0] < support:
            items_under_support.append(itemset)
    
    # remove items with insufficient support
    for itemset in items_under_support:
        del itemsets_count[itemset]
    
    if len(itemsets_count.keys()) == 0:
        # Stop Algorithm
        return
            
    else:
        itemset_lvl += 1
        itemsets = []
        # print('')
        # print(itemsets_count)
        # print('')
        # print(itemsets_count.keys())
        for item in itemsets_count.keys():
            itemsets += list(set(item.split(',')) - set(itemsets))
        
        itemset_support(uniqueData, itemsets, itemset_lvl)
        final_counts.update(itemsets_count)
      
# ############################# End of Helper Functions ###############################


# Main Program
SI = eval(input('Starting Index: '))
support = eval(input('Enter Support: '))
confidence = eval(input('Enter confidence: '))

data = read_data_txt(file_path='ticdata2000.txt',data_size=(5822, 86))

data = set_apart_attr(slice_attr(data, SI))

# data = read_data_txt(file_path='test.txt',data_size=(3, 6))

itemset_support(data)

# print(final_counts)



# final_count={'0_0,0_1,0_2':3250, '0_0,0_1,0_3':2200, '2_3,3_4,1_0': 3012}  

# import itertools as itr
# comb = []
# for itemset in final_count.keys():
#     comb.append(list(itr.permutations(itemset.split(','), 3)))












