from collections import defaultdict, namedtuple
import itertools
import FPclass

def find_frequent_itemsets(transactions, minimum_support_rate, include_support=True):


    items = defaultdict(lambda: 0)
    transactions_done = []
    trans_num = 0
    for transaction in transactions:
        done = []
        trans_num += 1
        for item in transaction:
            items[item] += 1
            done.append(item)
        transactions_done.append(done)
    #print(trans_num)
    minimum_support = trans_num * minimum_support_rate
    #0. Remove items  < min-support
    items = dict((item, support) for item, support in list(items.items())
        if support >= minimum_support)


    # Build our FP-tree.
    def freq(v):
        return items[v],v
    def transaction_sort(transaction): #1. sorted transaction by min-support
        transaction = [v for v in transaction if v in items]
        transaction.sort(key=lambda v: freq(v), reverse=True)
        return transaction

    origin_tree = FPclass.FPTree()
    for transaction in map(transaction_sort, transactions_done):#2. build tree
        origin_tree.add(transaction)
    #print(origin_tree.inspect())
    

    def find_with_suffix(tree, suffix):
        for item, nodes in list(tree.items()):
            support = sum(n.count for n in nodes) #sum the n.count for the node
            if support >= minimum_support and item not in suffix: 
                found_set = [item] + suffix
                yield (found_set, support) if include_support else found_set #mode:include support or not
                
                # Build a conditional tree  
                cond_tree = conditional_tree_from_paths(tree.prefix_paths(item), minimum_support)
                #Recursively search for frequent itemsets.
                for itemset in find_with_suffix(cond_tree, found_set):
                    yield itemset 

    # Search for frequent itemsets, and output the result
    for itemset in find_with_suffix(origin_tree, []):
        yield itemset


def conditional_tree_from_paths(paths, minimum_support):
    """Builds a conditional FP-tree from the given prefix paths."""
    tree = FPclass.FPTree()
    condition_item = None
    items = set()

    for path in paths:
        if condition_item is None:
            condition_item = path[-1].item #get last item

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



def generate_association_rules(patterns, confidence_threshold):
    """
        Given a set of frequent itemsets, return a dict
        of association rules in the form
        {(left): ((right), confidence)}
        """
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
