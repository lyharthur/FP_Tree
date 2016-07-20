#coding=utf-8

import tree_builder
import copy

class Tree_miner(object):
    """tree_miner类. 作用:对Tree进行频繁项集的挖掘"""
    def __init__(self, Tree=None, min_sup=-1, headerTable={}):
        """tree_miner的初始化. Tree即为构造好的FP_Tree, min_sup是最小支持度计数, headerTable是FP_Tree的头结点表"""
        self.min_sup = min_sup
        self.tree_mining(Tree=Tree, headerTable=headerTable)


    def tree_mining(self, Tree, A=[], headerTable={}):
        """功能: 递归实现对树Tree频繁项集的挖掘. A相当于伪代码中的α，B相当于β"""
        B = []
        allElem = {}        #用来保存单个路径情况时，路径上的所有节点
        node = Tree.root       #node取得树的根节点
        while len(node.children) > 0:        #判断是否是单个路径
            if len(node.children) != 1:          #如果路径上的某个节点的孩子数不止一个，则它不是单个路径
                break
            node = list(node.children.values())[0]        #node取得下一个节点
            allElem.setdefault(node.data,node.count)        #记录路径上的节点，如果是单个路径的话会用到
        if len(node.children) < 1:                  #Tree只包含单个路径
            L = self.getL(items=allElem, min_sup=self.min_sup, A=A)     #L即为我们要求的频繁项集
            self.showResult(L)      #对结果进行输出
            return
        else:
            for item in headerTable:            #对于头结点表中的元素，逐个找以其结尾的频繁项集
                if A:                   #产生项目集B
                    for elem in A:
                        if elem != []:
                            temp = copy.copy(elem)
                            B.append(temp)
                            B.append([item]+temp)
                else:
                    B.append([item])
                pattem,counts = self.findPattemBase(item, headerTable)      #得到以项item结尾的所以条件模式基,counts存放条件模式基的计数
                myHeaderTable = {}          
                conditionTree_builder = tree_builder.Tree_builder(routines=pattem, counts=counts, headerTable=myHeaderTable)        #新建一个Tree_builder对象，用它来构造条件FP-Tree
                if conditionTree_builder.tree.root.children:            #如果构造的条件FP-树不空
                    self.tree_mining(Tree=conditionTree_builder.tree, A=B, headerTable=myHeaderTable)       #递归调用
                B = []
        return


    def findPattemBase(self, item, headerTable):
        """功能: 根据树的头结点表去搜索树中item的条件模式基"""
        itemPattem = []                 #存放项item的所有模式基
        counts = []                     #存放模式基的计数
        addressTable = headerTable[item]    #头节点表中item链上所以节点的地址
        for itemNode in addressTable:           #对头结点表表中存放的每个item节点
            itemInPattem = []               #用来存放item模式基中的各项
            nodeInPattem = itemNode.parent         #item模式基的项，用它来回溯到树根，即为一条模式基
            if nodeInPattem.data == 'null':         #如果父亲节点就是树根，则跳过
                continue
            while nodeInPattem.data != 'null':                  #如果还没到树根，则一直回溯
                itemInPattem.append(nodeInPattem.data)           #把它压进item的模式基
                nodeInPattem = nodeInPattem.parent          #让当前节点跳到它的父亲节点，进行回溯
            itemInPattem = tuple(itemInPattem)
            itemPattem.append(itemInPattem)             #找完了一条item的模式基了
            counts.append(itemNode.count)           #模式基的计数
        return itemPattem,counts


    def showResult(self, result=[[]]):
        """功能: 将挖掘到的频繁项集进行展示"""
        for elem in result:
            num = elem.pop()        #频繁项集的计数
            print(tuple(elem),':',num)
        return


    def combiner(self, myList, n): 
        """功能: 对list列表里的所有元素进行排列组合,生成n个元组组合在一起的列表"""
        answers = []
        one = [0] * n 
        def next_c(li = 0, ni = 0): 
            if ni == n:
                answers.append(copy.copy(one))
                return
            for lj in range(li, len(myList)):
                one[ni] = list(myList)[lj]
                next_c(lj + 1, ni + 1)
        next_c()
        return answers


    def findMinimum(self, items, elem):
        """功能: 根据items字典找出elem列表中各项计数的最小值"""
        minimum = items[elem[0]]
        for a in elem:
            if items[a] < minimum:              #如果某元素的计数更小，则记录它的计数
                minimum = items[a]
        return minimum


    def getL(self, items, min_sup=-1, A=[]):
        """功能: 对于只含单路径的树,进行生成频繁项集"""
        tempResult = []
        finnalResult = []
        nodes = items.keys()        #取得items字典的键，即单路径上的所有节点
        for i in range(1,len(nodes)+1):         #对nodes，即路径上的所有节点生成各种组合
            tempResult += self.combiner(myList=nodes, n=i)
        for elem in tempResult[::-1]:           #elem逆序对dearResult访问，因为接下来会删除元素，逆序好操作
            elemMinimum = self.findMinimum(items, elem)         #找出elem里面的最小计数
            if elemMinimum < min_sup:               #如果组合elem的最小计数小于最小支持度计数，则删除.
                tempResult.remove(elem)
            else:                           #否则把它压入结果列表中进行输出，但它只是条件模式基，要加上最后一个项构成频繁项集，同时把最小计数也加上
                for Aelem in A:         #A可能含有多项
                    if Aelem:
                        temp = elem
                        temp += Aelem
                        temp.append(elemMinimum)
                        finnalResult.append(temp)               #将挖掘出的频繁项集保存在finnalResult列表
        return finnalResult
