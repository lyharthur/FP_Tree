from collections import namedtuple
class FPNode(object):
    #A node in FP tree.
    
    def __init__(self, tree, item, count=1):
        self._tree = tree
        self._item = item
        self._count = count
        self._parent = None
        self._children = {}
        self._neighbor = None
    
    def add(self, child):
        
        if not isinstance(child, FPNode):
            raise TypeError("Can only add other FPNodes as children")
        
        if not child.item in self._children:
            self._children[child.item] = child
            child.parent = self

    def search(self, item):
    
        try:
            return self._children[item]
        except KeyError:
            return None
                
    def remove(self, child):
        try:
            if self._children[child.item] is child:
                del self._children[child.item]
                child.parent = None
                self._tree._removed(child)
                for sub_child in child.children:
                    try:
                        self._children[sub_child.item]._count += sub_child.count
                        sub_child.parent = None # no parent
                    except KeyError:
                        
                        self.add(sub_child)
                child._children = {}
            else:
                raise ValueError("that node is not a child of this node")
        except KeyError:
                    raise ValueError("that node is not a child of this node")
    
    def __contains__(self, item):
        return item in self._children
    
    @property
    def tree(self):
        return self._tree
    
    @property
    def item(self):
        return self._item
    
    @property
    def count(self):
        return self._count
    
    def increment(self):
        if self._count is None:
            raise ValueError("Root nodes have no associated count.")
        self._count += 1
    
    @property
    def root(self):
        return self._item is None and self._count is None
    
    @property
    def leaf(self):
        return len(self._children) == 0
    
    def parent():
        doc = "The node's parent."
        def fget(self):
            return self._parent
        def fset(self, value):
            if value is not None and not isinstance(value, FPNode):
                raise TypeError("A node must have an FPNode as a parent.")
            if value and value.tree is not self.tree:
                raise ValueError("Cannot have a parent from another tree.")
            self._parent = value
        return locals()
    parent = property(**parent())
    
    def neighbor():
        doc = """
        The node's neighbor; the one with the same value that is "to the right"
        of it in the tree.
            """
        def fget(self):
            return self._neighbor
        def fset(self, value):
            if value is not None and not isinstance(value, FPNode):
                raise TypeError("A node must have an FPNode as a neighbor.")
            if value and value.tree is not self.tree:
                raise ValueError("Cannot have a neighbor from another tree.")
            self._neighbor = value
        return locals()
    neighbor = property(**neighbor())
    
    @property
    def children(self):
        return tuple(self._children.values())

class FPTree(object):
    Route = namedtuple('Route', 'head tail')
    
    def __init__(self):
        # The root node of the tree.
        self._root = FPNode(self, None, None)
        
        self.headtable = {}
    
    @property
    def root(self):
        return self._root
    
    def add(self, transaction):
        point = self._root
        
        for item in transaction:
            next_point = point.search(item)
            if next_point:
                
                next_point.increment()
            else:
                
                next_point = FPNode(self, item)
                point.add(next_point)
                self._update_headtable(next_point)
            
            point = next_point

    def _update_headtable(self, point):
        assert self is point.tree
        
        try:
            HT = self.headtable[point.item]
            HT[1].neighbor = point # route[1] is tail last one
            self.headtable[point.item] = self.Route(HT[0], point)
        except KeyError:
            self.headtable[point.item] = self.Route(point, point)

    def items(self):
        for item in list(self.headtable.keys()):
            yield (item, self.nodes(item))

    def nodes(self, item):
    
        try:
            node = self.headtable[item][0]
        except KeyError:
            return

        while node:
            yield node
            node = node.neighbor

    def prefix_paths(self, item):
    
        def collect_path(node):
            path = []
            while node and not node.root:
                path.append(node)
                node = node.parent
            path.reverse()
            return path
        return (collect_path(node) for node in self.nodes(item))


    def _removed(self, node):
    
        head, tail = self.headtable[node.item]
        if node is head:
            if node is tail or not node.neighbor:
                del self.headtable[node.item]
            else:
                self.headtable[node.item] = self.Route(node.neighbor, tail)
        else:
            for n in self.nodes(node.item):
                if n.neighbor is node:
                    n.neighbor = node.neighbor
                    if node is tail:
                        self.headtable[node.item] = self.Route(head, n)
                    break

