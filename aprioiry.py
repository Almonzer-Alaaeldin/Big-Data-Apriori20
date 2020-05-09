import numpy as np
import itertools as itr
import pandas as pd

# Global Variables
final_counts = {}
assoc_rules= pd.DataFrame(columns=["Rule","LHS","LHS_count","set","set_count","confidence", "Lift","Leverage"]) 
           
############################### Start of Helper Functions ###############################

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
      
############################################################## rule generation ###########################################
def find_lvl():
  # itemsts level is the max number of join symbols(commas) added by one 
  global final_counts
  lvls=[]
  for key in final_counts.keys():
    lvls.append(key.count(','))
  return max(lvls)+1

def get_ordered_key(unordered_key):    
  global final_counts
  # if key is not in ordered form 
  if unordered_key in final_counts.keys(): return unordered_key 
  # then fetch orderd key and return its form
  for ordered_key in final_counts.keys():  
         if (set(unordered_key.split(',')) == set(ordered_key.split(','))): return ordered_key

def generate_assoc_rules(itemset_lvl,mini_conf,NT): 
   # "NT" is the total number of transactions 
  global final_counts
  global assoc_rules
  rule_saperator=" --> "
  for key in final_counts.keys():
    #check if it is last Ck itemsets using commas (number of cammas == level-1)
    if(key.count(',')== itemset_lvl-1):    
      mylist=(key.split(','))
      for item in mylist:  
        RHS=set(mylist)
        RHS.remove(item)
        RHS=",".join(RHS) 
        #rule for an itemset is the itemset => rest of all itemsets
        rule= str(item)+rule_saperator+RHS 
        #calculate confidence
        confidence= float (final_counts[key]) / final_counts[item] 
        #if it is above mini_conf will calc Lift and Leverage
        if(confidence >= mini_conf):
           # check if RHS is in ordered and correct its format e.g RHS=0_0,0_1 and key=0_1,0_00            
           RHS=get_ordered_key(RHS)     
           #lift is support(all set)/support(left-side)*support(right-side)
           Lift= ( float(final_counts[key])/NT ) / ( float(final_counts[item])/NT * float(final_counts[RHS])/NT ) 
           #leverage is support(all set) - support(left-side)*support(right-side)
           Leverage=( float(final_counts[key])/NT ) - ( float(final_counts[item])/NT * float(final_counts[RHS])/NT ) 
           #create entry for assoc_rules dataframe
           entry={"Rule":rule , "LHS":item ,"LHS_count":final_counts[item] ,"set":key, "set_count":final_counts[key], "Lift":Lift , "Leverage":Leverage, "confidence":confidence} 
           assoc_rules=assoc_rules.append(entry, ignore_index=True, sort=False)
  #check if datafarme is empty then all rules are below mini confidence 
  if(len(assoc_rules)==0): print("All rules below confidence: ",mini_conf)
         
# ############################# End of Helper Functions ###############################

# Main Program
#SI = eval(input('Starting Index: '))
support = eval(input('Enter Support: '))
confidence = eval(input('Enter confidence: '))
data = read_data_txt(file_path='ticdata2000.txt',data_size=(5822, 86))
data = set_apart_attr(slice_attr(data))
# data = read_data_txt(file_path='test.txt',data_size=(3, 6))
itemset_support(data)
generate_assoc_rules(find_lvl(),confidence,5822)
print(assoc_rules)