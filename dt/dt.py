import numpy as np
import sys
import math
from collections import Counter

bound_purity = 0.8
max_depth = 6

class node:
    def __init__(self, data):
        self.data = data
        self.label = ''
        self.children = []
        self.isend = False
        self.depth = -1
        self.final_val = []
        for d in data:
            self.final_val.append(d[len(attr)-1])
        self.final_per = np.zeros(len(final))
        
        for i in self.final_val:
            for f in range(len(final)):
                if(i == final[f]):
                    self.final_per[f] += 1
        self.final_sum = sum(self.final_per)
        for f in range(len(final)):
            if(self.final_per[f] >= float(self.final_sum)*bound_purity and self.final_sum > 0):
                self.isend = True
                self.label = final[f]

def entropy(p):
    val = 0
    for i in p:
        i = float(i)/float(sum(p))
        if(i == 0):
            continue
        val -= i * math.log(i,2.0)
    return val

def divnum(list):
    num = 0
    for l in list:
        if(len(l)>0):
            num += 1
    return num

def findmost(list):
    c = Counter(list)
    m = c.most_common(1)
    return m[0][0]

def makenode(nod):
    global depth
    list = nod.data
    attr_num = len(attr)-1
    final_len = len(final)
    lenlist = len(list)
    max_gain = -100
    idx = -1
    answer = []
    final_list = []

    origin = np.zeros(final_len)
    for d in list:
        for f in range(final_len):
            if(d[attr_num] == final[f]):
                origin[f] += 1
    origin_ent = entropy(origin)
    for d in list:
        final_list.append(d[attr_num])
    if(nod.isend):
        return
    if(nod.depth >= max_depth):
        nod.label = findmost(final_list)
        nod.isend = True
        return
    for i in range(attr_num):
        size = len(vars[i])
        sinfo = np.zeros(size)
        divided_list = []
        for tmp in range(size):
            divided_list.append([])
        for j in range(lenlist):
            for k in range(len(vars[i])):
                if(list[j][i] == vars[i][k]):
                    divided_list[k].append(j)
                    sinfo[k] += 1
        for s in sinfo:
            s = float(s)/sum(sinfo)
        splitinfo = entropy(sinfo)
        ents = []
        all = 0
        if(divnum(divided_list) <= 1):
            continue
        for d in divided_list:
            all+=len(d)
        for dv in divided_list:
            for case in dv:
                nums = np.zeros(final_len)
                for f in range(final_len):
                    if(list[case][attr_num] == final[f]):
                        nums[f] += 1
                ents.append(entropy(nums))
            for e in range(len(ents)):
                ents[e] /= float(all)
                ents[e] *= len(dv)
        entro = sum(ents)
        gain = origin_ent - entro
        gainratio = gain/splitinfo
        if(max_gain < gainratio):
            idx = i
            max_gain = gainratio
            answer = divided_list
    if(idx < 0):
        nod.isend = True
    else:
        nod.label = attr[idx]
    
    for child in answer:
        c_list = []
        for index in child:
            c_list.append(list[index])
        if(len(c_list) > 0):
            nod.children.append(node(c_list))
        else:
            tmp_nod = node([])
            tmp_nod.isend = True
            tmp_nod.label = findmost(final_list)
            nod.children.append(tmp_nod)
    if(len(nod.children) > 0):
        for child in nod.children:
            child.depth = nod.depth + 1
            if(child.isend == False):
                makenode(child)
    return

def predict(test_list, result):
    f=open(result, 'w')
    for at in attr:
        f.write(at + "\t")
    f.write("\n")
    for testcase in test_list:
        nod = root
        for at in testcase:
            f.write(at + "\t")
        while(nod.isend == False):
            idx = attr.index(nod.label)
            v = vars[idx].index(testcase[idx])
            nod = nod.children[v]
        f.write(nod.label)
        f.write("\n")
    f.close
    return

def main(train, test, result):
    global train_list, root, attr, vars, final
    f = open(train, 'r')
    lines = f.readlines()
    train_list = []
    isFirst = True
    candi = 0
    for l in lines:
        temp = l.split('\n')
        spliter = temp[0].split('\t')
        if(isFirst):
            attr_num = len(spliter)
            attr = spliter
            isFirst = False
            continue
        train_list.append(spliter)
        candi+=1
    f.close
    
    vars = []
    
    for a in range(attr_num):
        vars.append([])
    for i in range(candi-1):
        for j in range(attr_num):
            if(train_list[i][j] not in vars[j]):
                vars[j].append(train_list[i][j])

    final = vars[attr_num-1]
    root = node(train_list)
    root.depth = 0
    print("Start making decision tree...")

    makenode(root)

    print("\nDecision tree made succesfully. Start Testing...")
    f = open(test, 'r')
    lines = f.readlines()
    test_list = []
    
    isFirst = True

    for l in lines:
        temp = l.split('\n')
        spliter = temp[0].split('\t')
        if(isFirst):
            isFirst = False
            continue
        test_list.append(spliter)
    f.close

    predict(test_list, result)

    print("\nTest complete! Output file " + result + ' created.')

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
