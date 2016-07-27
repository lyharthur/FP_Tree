from fpgrowth import find_frequent_itemsets ,generate_association_rules
from pyfpgrowth import find_frequent_patterns ,generate_association_rules

import csv
import time

with open('Dataset/D100kT10N1k.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile ,delimiter = ',',quotechar = '|')
    data = []
    for row in spamreader:
        row = [num.replace(' ', '') for num in row]
        data.append(row)
min_sup = 1000 * 1/100

routines = [    
           ['Cola','Egg','Ham'],
           ['Cola','Diaper','Beer'],
           ['Cola','Beer','Diaper','Ham'],
           ['Diaper','Beer']
        ]                                  #事务数据集



f = open('itemset.txt', 'w')

start = time.time()
#find_frequent_itemsets(data, 2)

for itemset in find_frequent_itemsets(data, 100):
    f.write(str(itemset)+'\n')
f.close()

patterns={}
with open('itemset.txt') as f:
    for line in f:
        line = line.replace('(','')
        line = line.replace(')','')
        line = line.replace('[','')
        line = line.replace(' ','')

        (key, val) = line.split(']',1)
        val = val.replace('\n','')
        val = val.replace(',','')
        key = key.replace('\'','')
        s = tuple(key.split(','))
        patterns[s] = int(val)
#print(patterns)

f = open('rules.txt', 'w')
f.write(str(generate_association_rules(patterns,0.4)).replace(', (','\n('))

end = time.time()
elapsed = end - start
print("Time taken: ", elapsed, "seconds.")