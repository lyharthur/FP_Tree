from pyfpgrowth import generate_association_rules, find_frequent_patterns  # flake8: noqa
from fpgrowth import find_frequent_itemsets
import csv
import time

with open('Dataset/D1kT10N500.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile ,delimiter = ',',quotechar = '|')
    data = []
    for row in spamreader:
        row = [num.replace(' ', '') for num in row]
        data.append(row)
min_sup = 1000 * 0.1/100

routines = [    
           ['Cola','Egg','Ham'],
           ['Cola','Diaper','Beer'],
           ['Cola','Beer','Diaper','Ham'],
           ['Diaper','Beer']
        ]                                  #事务数据集


start = time.time()
print(len(list(find_frequent_itemsets(data, 2))))
#for itemset in find_frequent_itemsets(data, min_sup):
#    print(itemset)
end = time.time()
elapsed = end - start
print("Time taken: ", elapsed, "seconds.")