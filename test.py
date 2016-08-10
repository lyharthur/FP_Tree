from fp_growth import find_frequent_itemsets
import csv
import time

start = time.time()

with open('Dataset\D100kT10N1k.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile ,delimiter = ',',quotechar = '|')
    data = []
    for row in spamreader:
        row = [num.replace(' ', '') for num in row]
        data.append(row)

minimum_support_rate = 0.1/100


routines = [    
           ['Cola','Egg','Ham','Bread'],
           ['Cola','Diaper','Beer'],
           ['Cola','Beer','Diaper','Ham'],
           ['Diaper','Beer']
        ]                               

f = open('output.txt','w')

#print(len(list(find_frequent_itemsets(data, minimum_support_rate))))
#print(sum(1 for x in find_frequent_itemsets(routines, min_sup)))
for itemset in find_frequent_itemsets(data, minimum_support_rate):
    f.write(str(itemset)+'\n'+'12')
    #print(itemset)
f.close()

end = time.time()
elapsed = end - start
print( "Time taken: ", elapsed, "seconds.")

