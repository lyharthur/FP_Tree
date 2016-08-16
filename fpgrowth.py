from collections import defaultdict
import FPclass
import itertools
import csv
import time
import sys

def find_frequent_itemsets(transactions, minimum_support_rate, include_support=True):

    items = defaultdict(lambda: 0) # items ,supports
    transactions_done = []
    trans_num = 0

    # Load transactions & count the support
    for transaction in transactions:
        done = []
        trans_num += 1
        for item in transaction:
            items[item] += 1
            done.append(item)
        transactions_done.append(done)
    minimum_support = trans_num * minimum_support_rate
    # Remove items if < min support .
    items = dict((item, support) for item, support in list(items.items())
        if support >= minimum_support)


    # Build FP-tree.
    def freq(v):
        return items[v],v
    def transaction_sort(transaction): #sort transaction by minimum_support
        transaction = [v for v in transaction if v in items]
        transaction.sort(key=lambda v: freq(v), reverse=True)
        return transaction

    origin_tree = FPclass.FPTree()
    for transaction in map(transaction_sort, transactions_done):
        origin_tree.add(transaction)


    def find_with_suffix(tree, suffix):
        for item, nodes in list(tree.items()):
            support = sum(n.count for n in nodes)
            if support >= minimum_support and item not in suffix: 
                found_set = [item] + suffix
                yield (found_set, support) if include_support else found_set
                
                # conditional tree
                cond_tree = conditional_tree_from_paths(tree.prefix_paths(item), minimum_support)
                #Recursively search for frequent itemsets.
                for itemset in find_with_suffix(cond_tree, found_set):
                    yield itemset 

    # Search for frequent itemsets, and output .
    for itemset in find_with_suffix(origin_tree, []):
        yield itemset




def conditional_tree_from_paths(paths, minimum_support):
    tree = FPclass.FPTree()
    condition_item = None
    items = set()

    for path in paths:
        if condition_item is None:
            condition_item = path[-1].item  #target is last item

        point = tree.root
        for node in path:
            next_point = point.search(node.item)
            if not next_point:
                # Add a new node to the tree.
                items.add(node.item)
                count = node.count if node.item == condition_item else 0
                next_point = FPclass.FPNode(tree, node.item, count)
                point.add(next_point)
                tree._update_headtable(next_point)
            point = next_point
    #print(tree.inspect())

    assert condition_item is not None

    # Calculate the counts of the non-leaf nodes.
    for path in tree.prefix_paths(condition_item):
        count = path[-1].count
        for node in reversed(path[:-1]):
            node._count += count

    for node in tree.nodes(condition_item):
        if node.parent is not None: # the node might already be an single node
            node.parent.remove(node)

    return tree




# need to fix
def generate_association_rules(patterns, confidence_threshold):
    rules = {}
    for itemset in patterns.keys():
        upper_support = patterns[itemset]
        
        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i):
                antecedent = tuple(sorted(antecedent))
                consequent = tuple(sorted(set(itemset) - set(antecedent)))
                
                if antecedent in patterns:
                    lower_support = patterns[antecedent]
                    confidence = float(upper_support) / lower_support
                    
                    if confidence >= confidence_threshold:
                        rules[antecedent] = (consequent, confidence)

    return rules

if __name__ == '__main__' :

    with open('Dataset/D1kT10N500.txt', newline='') as csvfile:
        spamreader = csv.reader(csvfile ,delimiter = ',',quotechar = '|')
        data = []
        for row in spamreader:
            row = [num.replace(' ', '') for num in row]
            data.append(row)
    
    min_sup_rate = float(sys.argv[1])/100

    routines = [
            ['Cola','Egg','Ham'],
            ['Cola','Diaper','Beer'],
            ['Cola','Beer','Diaper','Ham'],
            ['Diaper','Beer']
            ]


    f = open('itemset.txt', 'w')

    start = time.time()
    #find_frequent_itemsets(data, 2)
    c = 0
    for itemset in find_frequent_itemsets(data, min_sup_rate):
        f.write(str(itemset)+'\n')
        c += 1
    f.close()
    print('minimum_support_rate : ' + str(min_sup_rate))
    print('Total itemset num : '+ str(c))
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
