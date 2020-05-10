import numpy as np
import itertools as itr
import pandas as pd
from itertools import combinations, chain

# Global Variables
final_counts = {}
assoc_rules= pd.DataFrame(columns=["Rule","LHS_count","set_count","confidence", "Lift","Leverage"]) 
           
# ############################# Start of Helper Functions ###############################

def read_data_txt(file_path='ticdata2000.txt',data_size=(5822, 49)): 
    ''' Read Training Data size=(5822, 49)'''
    # Prepare array for data
    data = np.zeros(data_size, dtype=np.dtype('U100'))
    
    # Read All The Data and fill the array
    datafile = open(file_path, 'r')
    
    i = 0
    
    for line in datafile:
        data[i] = [eval(val) if val.isnumeric() else val for val in line.split()]
        i += 1
    
    return data
    
def slice_attr(full_data):
    # return np.delete(full_data, np.s_[7:44], axis=1)
    return np.append(full_data[:, 44: 49], full_data[:, 0:7], axis=1)

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
def get_rules(key,mini_conf):
  global final_counts
  itemsets=set(key.split(","))
  # find all subset exists in itemset
  item_subsets = chain.from_iterable(combinations(itemsets, len) 
        for len in range(len(itemsets)+1))
  item_subsets = list(map(frozenset, item_subsets))
  #print(item_subsets)
  rules = list()
  # exclude empty subsets and subsets with length of itemsets
  sub_itemsets = {subset for subset in item_subsets if (len(subset) != 0 and len(subset) != len(item_subsets))}
  for subset in sub_itemsets:
    left = subset
    #right is all itemsets excluding left subsets 
    right = itemsets.difference(subset)
    # each rule is dict with two keys right and left with its values 
    if len(right)!= 0 and len(left)!= 0: 
        LHS=get_ordered_key(",".join(left))
        #calculate confidence support_count(itemsets)/support_count(left-side)
        confidence= float (final_counts[key]) / final_counts[LHS] 
        if(confidence >= mini_conf):
          rules.append( {"left":",".join(left),"right":",".join(right), "conf": confidence} )
  return rules

def map_to_attr_names(k):
  attr_names={"0":"MOSTYPE","1":"MAANTHUI","2":"MGEMOMV","3":"MGEMLEEF","4":"MOSHOOFD","5":"MGODRK","6":"MGODPR","7":"PPERSAUT","8":"PBRAND","9":"AWAPART","10":"APERSAUT","11":"ABRAND"}
  l=list()
  l=k.split(",")
  for index in range(0,len(l)):
    col_number=l[index][l[index].find("_")+1:]
    l[index]=l[index].replace("_"+col_number,"_"+attr_names[col_number])
  return ",".join(l)
  
def find_lvl():
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
      #print("current Ck is: " ,key) 
      rules= get_rules(key,mini_conf)
      for rule in rules:  
        RHS=rule["right"]  
        LHS=rule["left"]
        LHS=get_ordered_key(LHS)
        maped_RHS= map_to_attr_names(RHS)
        maped_LHS= map_to_attr_names(LHS) 
        maped_rule=maped_LHS+rule_saperator+maped_RHS
        # check if RHS is in ordered and correct its format e.g RHS=0_0,0_1 and key=0_1,0_0            
        RHS=get_ordered_key(RHS)     
        #lift is support(all set)/support(left-side)*support(right-side)
        Lift= ( float(final_counts[key])/NT ) / ( float(final_counts[LHS])/NT * float(final_counts[RHS])/NT ) 
        #leverage is support(all set) - support(left-side)*support(right-side)
        Leverage=( float(final_counts[key])/NT ) - ( float(final_counts[LHS])/NT * float(final_counts[RHS])/NT ) 
        # itemsets names to given attributes names 
        entry={"Rule":maped_rule , "LHS_count":final_counts[LHS],"set_count":final_counts[key], "Lift":Lift , "Leverage":Leverage, "confidence":rule["conf"]} 
        assoc_rules=assoc_rules.append(entry, ignore_index=True, sort=False)
        #print(entry)
  if(len(assoc_rules)==0): print("All rules below confidence: ",mini_conf)
         
# ############################# End of Helper Functions ###############################


#Main Program
support = eval(input('Enter Support: '))
confidence = eval(input('Enter confidence: '))
data = read_data_txt(file_path='ticdata2000.txt',data_size=(5822, 49))
data = set_apart_attr(slice_attr(data))
itemset_support(data)
generate_assoc_rules(find_lvl(),confidence,5822)
pd.set_option('display.max_colwidth', -1)
pd.set_option("max_rows", -1)
print(assoc_rules)
#display(assoc_rules) #in case if using notebook 