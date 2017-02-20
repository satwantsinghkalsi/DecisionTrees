import math
from sys import argv
from random import randint
class Attribute:
      def __init__(self,index,name):
          self.index=index
          self.name=name
      def getIndex(self):
          return self.index
      def getName(self):
          return self.name
      def setName(self,value):
          self.name=value
class TreeNode:
      def __init__(self,index,name):
          self.name=name
          self.attrvalue=None
          self.label=None
          self.index=index
          self.child=[]
          self.positives=0.0
          self.negatives=0.0
          self.data=[]
          self.orderno=None
      def getIndex(self):
          return self.index
      def addChild(self,newnode):
          self.child.append(newnode)          
      def getChildren(self):
          return self.child
      def updateChild(self,value):
          self.child=value
      def getName(self):
          return self.name
      def setName(self,value):
          self.name=value
      def getAttrValue(self):
          return self.attrvalue
      def setAttrValue(self,value):
          self.attrvalue=value
      def setLabel(self,value):
          self.label=value
      def getLabel(self):
          return self.label
      def setPositives(self,value):
          self.positives=value
      def setNegatives(self,value):
          self.negatives=value
      def getNegatives(self):
          return self.negatives
      def getPositives(self):
          return self.positives
      def setData(self,value):
          self.data=value
      def getData(self): 
          return self.data
      def getOrderNo(self):
          return self.orderno
      def setOrderNo(self,value):
          self.orderno=value
def entropy(examples):
    ones=0.0
    zeros=0.0
    entropy=0.0
    for example in examples:
        if example[-1]=="1":
           ones+=1
        else:
           zeros+=1
    total=len(examples)
    if zeros==total or ones==total:
       entropy=0.0
    else:
       entropy=(-1*(ones/total)*math.log((ones/total),2))+(-1*(zeros/total)*math.log((zeros/total),2))
    return entropy
def getClassification(examples):
    ones=0.0
    zeros=0.0
    for example in examples:
        if example[-1]=='1':
           ones+=1
        else:
           zeros+=1
    return {"positives":ones,"negatives":zeros}
def varianceImpurity(examples):
    ones=0.0
    zeros=0.0
    impurity=0.0
    for example in examples:
        if example[-1]=='1':
           ones+=1
        else:
           zeros+=1
    total=zeros+ones
    impurity=(ones/total)*(zeros/total)
    return impurity
def divideSet(examples,attribute):
    sets=[]
    for value in range(0,2):
        exampleV=[]
        for example in examples:
            toAppend=False
            for i in range(0,len(example)-1):
                if i==attribute.getIndex() and example[i]==str(value):
                   toAppend=True
            if toAppend:
               exampleV.append(example)
        sets.append(exampleV)
    return sets
def getOccurences(examples,attr):
    zeros=0.0
    ones=0.0
    for example in examples:
        if example[attr.getIndex()]=='1':
           ones+=1
        else:
           zeros+=1
    return {"zeros":zeros,"ones":ones}    
def dataClassifier(examples,attributes):
    entropyS=entropy(examples)
    gain=0.0
    change=float("-inf")
    for i in range(0,len(attributes)): 
        valueSets=divideSet(examples,attributes[i])
        entropy0=entropy(valueSets[0])
        entropy1=entropy(valueSets[1])
        classify=getOccurences(examples,attributes[i])
        total=len(examples)
        gain=entropyS-((classify["ones"]/total)*entropy1)-((classify["zeros"]/total)*entropy0)
        if gain>change:
           change=gain
           node=attributes[i]
        
    return node
def dataClassifierVrnceImprty(examples,attributes):
    variance = varianceImpurity(examples)
    gain=0.0
    change=float("-inf")
    for i in range(0,len(attributes)):
        valueSets=divideSet(examples,attributes[i])
        impurity0=varianceImpurity(valueSets[0])
        impurity1=varianceImpurity(valueSets[1])
        classify=getOccurences(examples,attributes[i])
        total=len(examples)
        gain=variance-((classify["ones"]/total)*impurity1)-((classify["zeros"]/total)*impurity0)
        if gain>=change:
           change=gain
           node=attributes[i]
    return node  
    
def ID3(examples,attributes):
    root=None
    attributes=attributes[:]
    classify=getClassification(examples)
    if classify["positives"]==len(examples):
        root=TreeNode(-1,"1")
        root.setData(examples)
        root.setLabel(1)
        return root
    if classify["negatives"]==len(examples):
        root = TreeNode(-1,"0")
        root.setData(examples)
        root.setLabel(0)
        return root
    if len(attributes)==0:
       if classify["positives"]>classify["negatives"]:
          root= TreeNode(-1,"1")
          root.setData(examples)
          root.setLabel(1)
          return root
       else:
          root=TreeNode(-1,"0")
          root.setData(examples)
          root.setLabel(0)
          return root
    bestAttr=dataClassifier(examples,attributes)
    if bestAttr==None:
       if classify["positives"]>classify["negatives"]:
          node=TreeNode(-1,"1")
          root.setLabel(1)
          node.setData(examples)
          return node
       else:
          node= TreeNode(-1,"0")
          node.setData(examples)
          root.setLabel(0)
          return node
    attributes.remove(bestAttr)
    root=TreeNode(bestAttr.getIndex(),bestAttr.getName())
    root.setPositives(classify["positives"])
    root.setNegatives(classify["negatives"])
    root.setData(examples)
    for i in range(0,2):
        exampleV=[]
        for example in examples:
            toAppend=False
            for j in range(0,len(example)-1):
                if j==root.getIndex() and example[j]==str(i):
                   toAppend=True
            if toAppend:
               exampleV.append(example)
        if len(exampleV)==0:
           label=0
           if classify["negatives"]>classify["positives"]:
              label=0
           else:
              label=1   
           leafnode=TreeNode(-1,str(label))
           leafnode.setData(exampleV)
           leafnode.setLabel(label)
           leafnode.setAttrValue(i)
           root.addChild(leafnode)
        else:
           child=ID3(exampleV,attributes)
           child.setAttrValue(i)
           child.setData(exampleV)
           root.addChild(child)
    return root
def varianceImpurityHeuristic(examples,attributes):
    root=None
    attributes=attributes[:]
    classify=getClassification(examples)
    if classify["positives"]==len(examples):
        root=TreeNode(-1,"1")
        root.setData(examples)
        root.setLabel(1)
        return root
    if classify["negatives"]==len(examples):
        root = TreeNode(-1,"0")
        root.setData(examples)
        root.setLabel(0)
        return root
    if len(attributes)==0:
       if classify["positives"]>classify["negatives"]:
          root= TreeNode(-1,"1")
          root.setData(examples)
          root.setLabel(1)
          return root
       else:
          root=TreeNode(-1,"0")
          root.setData(examples)
          root.setLabel(0)
          return root
    bestAttr=dataClassifierVrnceImprty(examples,attributes)
    if bestAttr==None:
       if classify["positives"]>classify["negatives"]:
          node=TreeNode(-1,"1")
          root.setLabel(1)
          node.setData(examples)
          return node
       else:
          node= TreeNode(-1,"0")
          node.setData(examples)
          root.setLabel(0)
          return node
    attributes.remove(bestAttr)
    root=TreeNode(bestAttr.getIndex(),bestAttr.getName())
    root.setPositives(classify["positives"])
    root.setNegatives(classify["negatives"])
    root.setData(examples)
    for i in range(0,2):
        exampleV=[]
        for example in examples:
            toAppend=False
            for j in range(0,len(example)-1):
                if j==root.getIndex() and example[j]==str(i):
                   toAppend=True
            if toAppend:
               exampleV.append(example)
        if len(exampleV)==0:
           label=0
           if classify["negatives"]>classify["positives"]:
              label=0
           else:
              label=1   
           leafnode=TreeNode(-1,str(label))
           leafnode.setData(exampleV)
           leafnode.setLabel(label)
           leafnode.setAttrValue(i)
           root.addChild(leafnode)
        else:
           child=ID3(exampleV,attributes)
           child.setAttrValue(i)
           child.setData(exampleV)
           root.addChild(child)
    return root   
def printTree(root,level):
   if len(root.getChildren())==0:
      print ""+str(root.getLabel())
      return
   else:
      if level!=0:
         print ""
   i=1
   children=root.getChildren()
   while(i>=0):
       for j in range(0,level):
           print "|",
       print root.getName()+"="+str(children[i].getAttrValue())+":",
       printTree(children[i],level+1)
       i-=1
def nonLeafNodes(root):
    count=0
    if len(root.getChildren())==0:
       return count
    count=1
    children=root.getChildren()
    for child in children:
        count+=nonLeafNodes(child)
    return count
def orderTreeNodes(root,n):
    if len(root.getChildren())==0:
       return n-1
    root.setOrderNo(n)
    children=root.getChildren()
    for child in children:
        n=orderTreeNodes(child,n+1)
    return n
def copyTree(root):
    node=None
    if len(root.getChildren())==0:
       node=TreeNode(root.getIndex(),root.getName())
       node.setLabel(root.getLabel())
       node.setData(root.getData())
       return node
    node=TreeNode(root.getIndex(),root.getName())
    node.setPositives(root.getPositives)
    node.setNegatives(root.setNegatives)
    node.setData(root.getData())
    children = root.getChildren()
    for child in children:
        val=child.getAttrValue()
        tmpNode=copyTree(child)
        tmpNode.setAttrValue(val)
        node.addChild(tmpNode)
    return node
def findNode(root,pos):
    if root.getOrderNo()==pos:
       return root
    children =  root.getChildren()
    for child in children:
        node=findNode(child,pos)
        if node!=None:
           return node
    return None
def findParent(root,node):
    if len(root.getChildren())==0:
       return None
    for child in root.getChildren():
        if node==child:
           return root
    for child in root.getChildren():
        n=findParent(child,node)
        if n!=None:
           return n
    return None
        
def replaceTree(root,pos):
    replaceNode=findNode(root,pos)
    if replaceNode==root:
       return root
    replaceParent=findParent(root,replaceNode)
    children=replaceParent.getChildren()
    for i in range(0,len(children)):
          if children[i]==replaceNode:
              classify=getClassification(replaceParent.getData()) 
              if classify["positives"]>classify["negatives"]:
                  children[i]=TreeNode(-1,"1")
                  children[i].setLabel(1)
                  children[i].setAttrValue(replaceNode.getAttrValue())
                  children[i].setData(replaceNode.getData())
              else:
                  children[i]=TreeNode(-1,"0")
                  children[i].setLabel(0)
                  children[i].setAttrValue(replaceNode.getAttrValue())
                  children[i].setData(replaceNode.getData())
    replaceParent.updateChild(children)
    return root
def treeAccuracy(root,validation):
    count=0.0
    for example in validation:
        node=root
        while node is not None:
              if len(node.getChildren())==0:
                 if example[-1]==str(node.getLabel()):
                      count+=1
                 break
              children=node.getChildren()
              value=node.getIndex()
              for child in children:
                  if example[value]==str(child.getAttrValue()):
                     node=child
    accuracy=(count/len(validation))*100
    return accuracy
                   
def postPruning(l,k,root,validation):
    tmp=copyTree(root)
    bestTree=root
    accBest=0.0
    for i in range(0,l):
        accBest=treeAccuracy(bestTree,validation)
        tmpRoot=copyTree(tmp)
        m=randint(0,k)+1
        for j in range(0,m):
            n=nonLeafNodes(tmpRoot)
            orderTreeNodes(tmpRoot,0)
            p=randint(0,n-1)
            tmpRoot=replaceTree(tmpRoot,p)
        accDash=treeAccuracy(tmpRoot,validation)
        if accDash>accBest:
            bestTree=tmpRoot
    return bestTree 
                  
def main():
    if len(argv)==0:
       print "Enter the proper command line arguments. Make sure data file are in same folder as the program file(For details refer readme)"
       return
    l=int(argv[1])
    k=int(argv[2])
    trainFile=argv[3]
    validateFile=argv[4]
    testFile=argv[5]
    toPrint=argv[6]
    file =open  (trainFile,"r")
    nFile=file.read().splitlines()
    i=0
    attributes=[]
    examples=[]
    for line in nFile:
        if i==0:
           attrlist=line.split(",")
           column=0
           for attr in attrlist:
              if attr!="Class":
                tmpNode=Attribute(column,attr)
                attributes.append(tmpNode)
                column+=1
           i+=1
        else:
           datalist=line.split(",")
           examples.append(datalist)
    file.close()
    file=open(validateFile,"r")
    nFile=file.read().splitlines()
    i=0
    validation=[]
    for line in nFile:
        if i==0:
           i+=1
        else:
           datalist=line.split(",")
           validation.append(datalist)
    file.close()    
    file=open(testFile,"r")
    nFile=file.read().splitlines()
    i=0
    testdata=[]
    for line in nFile:
        if i==0:
           i+=1
        else:
           datalist=line.split(",")
           testdata.append(datalist)
    file.close()
    #examples=examples[:]
    print "ID3 with Gain Heuristics"
    print "---------------------------------------------------"
    root=ID3(examples,attributes)
    acc1=treeAccuracy(root,testdata)
    if toPrint=="yes":
      print "Decision tree with gain heuristics(without pruning):"
      printTree(root,0)
    prun=postPruning(l,k,root,validation)
    if toPrint=="yes":
      print "Decision tree with gain heuristics(with pruning):"
      printTree(prun,0)
    acc2=treeAccuracy(prun,testdata)
    print "The accuracy on the test data for gain heuristic(without pruning)::"+str(acc1)+"%"
    print "The accuracy on the test data for gain heuristic(with pruning)::"+str(acc2)+"%"
    print "======================================================================================"
    print "ID3 with Variance Impurity Heuristic"
    print "---------------------------------------------------"
    rootIm=varianceImpurityHeuristic(examples,attributes)
    acc1Im=treeAccuracy(rootIm,testdata)
    if toPrint=="yes":
      print "Decision tree with variance impurity heuristics(without pruning):"
      printTree(rootIm,0)
    prunIm=postPruning(l,k,rootIm,validation)
    acc2Im=treeAccuracy(prunIm,testdata)
    if toPrint=="yes":
       print "Decision tree with variance impurity heuristics(with pruning):"
       printTree(prunIm,0)
    print "The accuracy on the test data for variance impurity(without pruning)::"+str(acc1Im)+"%"
    print "The accuracy on the test data for variance impurity(with pruning)::"+str(acc2Im)+"%"
if __name__=="__main__":
    main()    


