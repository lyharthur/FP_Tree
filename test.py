from pyfpgrowth import generate_association_rules, find_frequent_patterns  # flake8: noqa

import csv


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


for itemset in find_frequent_patterns(routines, 1):
    print(itemset)
