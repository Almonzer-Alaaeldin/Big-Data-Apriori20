import numpy as np
import itertools as itr
import pprint 


# Global Variables
final_counts={}
assoc_rules=[]
test_cases=[]
###################################### append diff test cases for final counts dict ####################333

case= {   #tutorial example   #level 3 case
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
               '0_2,0_5':2,
               '0_1,0_2,0_3':2 ,
               '0_1,0_2,0_5':2,
               }
test_cases.append(case)
case={    #lec example   #level 2 case
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
############################################################## rule generation ###########################################33

def generate_assoc_rules(itemset_lvl,mini_conf,NT=1000): 
  # "NT" is the total number of transactions 
  global final_counts
  global assoc_rules
  rule_saperator=" --> "
  for key in final_counts.keys():
    if(key.count(',')== itemset_lvl-1):    #check if it is last Ck itemsets using commas (number of cammas == level-1)
      mylist=(key.split(','))
      for item in mylist:    
        rule = str(item)+rule_saperator+key.replace(str(item), "")  #constract a rule fromat  "left_side --> right_side"
        rule = rule.replace(",,",",").replace(rule_saperator+",",rule_saperator)  # replace ",," with "," and remove first item comma 
        if rule[-1] == ',': rule = rule[:-1]   #delete last char if comma 
        confidence= float (final_counts[key]) / final_counts[item] #calculate confidence support_count(all set) / support_count(left-side-set)
        if(confidence >= mini_conf):           #if it is above mini_conf will calc Lift and Leverage
           RHS=rule[rule.find(rule_saperator)+len(rule_saperator):] #extract right hand side set (part after rule saperator)
           Lift= ( float(final_counts[key])/NT ) / ( float(final_counts[item])/NT * float(final_counts[RHS])/NT ) #lift is support(all set)/support(left-side)*support(right-side)
           Leverage=( float(final_counts[key])/NT ) - ( float(final_counts[item])/NT * float(final_counts[RHS])/NT ) #leverage is support(all set) - support(left-side)*support(right-side)
           entry= {"Rule":rule , "LHS":item ,"LHS count":final_counts[item] ,"RHS":RHS ,"RHS count":final_counts[RHS] , "set":key, "set count":final_counts[key], "Lift":Lift , "Leverage":Leverage, "confidence":confidence} 
           assoc_rules.append(entry)
           pprint.pprint(entry, width=1)
       


############################# End of Helper Functions ###############################



# Main Program
confidence = eval(input('Enter mini confidence: '))
index = eval(input('Enter test case index: '))
NT = eval(input('total number of transactions: '))
lvl= eval(input('number of levels: '))
final_counts= test_cases[index]
print(test_cases[index])
generate_assoc_rules(lvl,confidence,NT)
