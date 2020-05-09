import numpy as np
import itertools as itr
import pandas as pd


# Global Variables
final_counts={}
assoc_rules= pd.DataFrame(columns=["Rule","LHS","LHS_count","set","set_count","confidence", "Lift","Leverage"]) 
test_cases=[]
###################################### append diff test cases for final counts dict ####################333

case= {   #tutorial example    #level 3 case
               '0_1':7,
               '0_2': 6,
               '0_3':6,
               '0_4':2,
               '0_5': 5,
               '0_1,0_2':3 ,
               '0_1,0_3':5,
               '0_1,0_5':2,
               '0_2,0_3':3,
               '0_2,0_4':2,
               '0_5,0_2':2,
               '0_1,0_2,0_3':2 ,
               '0_1,0_2,0_5':2,
               }
test_cases.append(case) 
case={    #lec example    #level 2 case  # trasactions =1000
              'credit_bad':300,
              'credit_good':700,
              'free_housing':108,
              'home_owner':713,
              'renter':179,
              'credit_good,free_housing': 64,
              'credit_good,home_owner':527,
              'credit_good,renter':109,
              'credit_bad,free_housing':44,
              'credit_bad,home_owner':186,
              'credit_bad,renter':70,
  }
test_cases.append(case)
############################################################## rule generation ###########################################
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
      mylist=(key.split(','))
      for item in mylist:  
        RHS=set(mylist)
        RHS.remove(item)
        RHS=",".join(RHS) 
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
           entry={"Rule":rule , "LHS":item ,"LHS_count":final_counts[item] ,"set":key, "set_count":final_counts[key], "Lift":Lift , "Leverage":Leverage, "confidence":confidence} 
           assoc_rules=assoc_rules.append(entry, ignore_index=True, sort=False)
           #print(entry, width=1)
  if(len(assoc_rules)==0): print("All rules below confidence: ",mini_conf)
         
# ############################# End of Helper Functions ###############################



# Main Program
confidence = eval(input('Enter mini confidence: '))
index = eval(input('Enter test case index: '))
NT = eval(input('total number of transactions: '))
# final count is a dict with itemset as key and its support count as value  
final_counts= test_cases[index]
print("calculated number of levels is: ",find_lvl())
generate_assoc_rules(find_lvl(),confidence,NT)
print(assoc_rules)