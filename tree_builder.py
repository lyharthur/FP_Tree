#coding=utf-8

import tree_building

class Tree_builder(object):
    """tree_builder类。 作用:根据事务数据集进行数据准备及构造树."""
    def __init__(self, routines, min_sup=-1, counts=[], headerTable={}):
        """类的初始化。 routines:事务数据集; min_sup:最小支持度及数; counts:每个事务出现的次数,默认为1; headerTable:头结点表,建造的FP_tree各结点的索引表。"""
        self.routines = routines
        self.counts = counts
        self.min_sup = min_sup
        self.items = self.getItems(self.routines)          #获取所有项
        self.sortedItems = self.getSortedItems(self.items)        #对所有项进行并排序,把计数小于min_sup的项移除，生成有序的频繁1-项集
        self.itemsTable = self.initItemsTable(headerTable)
        self.tree = self.treeBuilding(self.counts)


    def getItems(self, routines):
        """功能:扫描事务数据集,返回它的项集即各项的计数"""
        items = {}
        for routine in routines:
            for elem in routine:
                    items.setdefault(elem,0)
                    items[elem] += 1
        return items


    def getSortedItems(self, items=None):
        """功能:对项集进行排序,并删去非频繁项,得到频繁1-项集"""
        sortedItems = []
        temp = sorted(items.items(), key=lambda asd:asd[1], reverse=True)       #对字典items进行排序
        for elem in temp:
            if elem[1] >= self.min_sup:             #只取计数大于等于最小支持度及数的项
                sortedItems.append(elem[0])
        return sortedItems


    def getSortedRoutine(self, routine):
        """功能:根据排序好的频繁1-项集对某一条事务routine进行排序"""
        sortedRoutine = []
        for elem in self.sortedItems:
            if elem in routine:
                sortedRoutine.append(elem)
        return sortedRoutine


    def initItemsTable(self, itemsTable):
        """功能:头结点表的初始化"""
        for item in self.sortedItems:
            itemsTable.setdefault(item,[])
        return itemsTable


    def treeBuilding(self, counts):
        """功能:逐条取出事务,控制FP_Tree树的构造"""
        tree = tree_building.Tree(itemTable=self.itemsTable)             #生成一个树对象
        for routine in self.routines:                           #对事物数据集中的事务，逐条进行构造树
            sortedRoutine = self.getSortedRoutine(routine)          #用一条事务构造树之前先进行排序
            if counts:                      #如果counts不为空，即是在用模式基在构造条件树，此时需要考虑模式基的计数
                count = counts.pop(0)
            else:
                count =1
            tree.addRoutine(routine=sortedRoutine, Rroot=tree.root, count=count) #用排序好的事务构造树
        return tree
