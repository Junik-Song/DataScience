import numpy as np
import sys
from itertools import combinations
import time

def find(tuple, list):
    for num in tuple:
        if(num not in list):
            return False
    return True

def tuple_sort(tuple):
    tmp_list = sorted(tuple)
    tpl = ()
    for num in tmp_list:
        tpl += (num,)
    return tpl

def apriori(lines, minsup, max, strout):
    global mat
    start_time = time.time()
    
    print("Start Apriori...")
    f = open(strout, 'w')
    
    freq = []
    support_cnts = np.zeros(int(np.max(mat))+1)
    
    # First Round => Finding frequent items (1)

    for j in range(0,lines):
        for i in range(0, 1+int(np.max(mat))):
            if i in mat[j][:max]:
                support_cnts[i]+=1
    for i in range(0, 1+int(np.max(mat))):
        sup = (float(support_cnts[i]) / float(lines)) * 100.0
        if(sup >= float(minsup)):
            freq.append(i)

    # Second Round => Finding frequent items (2)
    if(np.size(freq) == 0):
        return
    idx = 2

    # Generating candidates
    candi = list(combinations(freq,2))
    candisize = len(candi)
    confi_a = np.zeros(candisize)
    confi_b = np.zeros(candisize)
    support_cnts = np.zeros(candisize)
    freq = []
    
       
    for j in range(0,lines):
        for c in range(0, len(candi)):
            if candi[c][0] in mat[j][:max]:
                confi_a[c] += 1
            if candi[c][1] in mat[j][:max]:
                confi_b[c] += 1
            if candi[c][0] in mat[j][:max] and candi[c][1] in mat[j][:max]:
                support_cnts[c]+=1

    for c in range(0, len(candi)):
        sup = (float(support_cnts[c]) / float(lines)) * 100.0
        if(sup >= float(minsup)):
            freq.append(candi[c])
            confi_a[c] = (float(support_cnts[c]) / float(confi_a[c])) * 100.0
            confi_b[c] = (float(support_cnts[c]) / float(confi_b[c])) * 100.0
            f.write("{" + str(candi[c][0]) + "}\t" + "{" + str(candi[c][1]) + "}\t" 
                    + str(format(sup,".2f")) + "\t" + str(format(confi_a[c], ".2f")) + "\n")
            f.write("{" + str(candi[c][1]) + "}\t" + "{" + str(candi[c][0]) + "}\t" 
                    + str(format(sup,".2f")) + "\t" + str(format(confi_b[c], ".2f")) + "\n")
    
   
    fsize = 1
    if(np.size(freq) == 0):
        return

    # Over 3 Round
    while(idx <= max and fsize>0):
        printed = []
        idx += 1
        candi = []
        fsize = len(freq)
        numset = []
        if(idx % 2 == 1):
            search = int((idx-1)/2)
        else:
            search = int(idx/2)

        # Generating candidates
        for fr in freq: # Frequent number set : to check all combinations
            for i in fr:
                if(i not in numset):
                    numset.append(i)
        combi = list(combinations(numset, idx))
        
        for com in combi: # Checking all combinations' combinations to see if it is frequent
            tmp_list = list(com)
            tmp_com_list = list(combinations(tmp_list, idx-1))
            ifadd = True
            for t in tmp_com_list:
                if(tuple_sort(t) not in freq):
                    ifadd = False
            if(ifadd):
                candi.append(tuple_sort(com))                       
        freq = []
        
        support_cnts = np.zeros(len(candi))
        candisize = len(candi)
        for j in range(0,lines):
            for k in range(0, candisize):
                if(find(candi[k], mat[j][:max])):
                    support_cnts[k] += 1

        for s in range(0, len(candi)-1):
            sup = (float(support_cnts[s]) / float(lines)) * 100.0
            if(sup >= float(minsup)):
                if(candi[s] not in freq):
                    freq.append(candi[s])
                target = []
                asso = []  
                
                for i in range(1,search+1):
                    test_set = list(combinations(candi[s], i))
                    for test in test_set:
                        target.append(test)
                for tg in target:
                    asc = ()
                    for num in candi[s]:
                        if(num not in tg):
                            asc += (num,)
                    asso.append(asc)
                
                confi_tg = np.zeros(len(target))
                confi_as = np.zeros(len(asso))

                for j in range(0,lines):
                    tsize = len(target)
                    for m in range(0, tsize):
                        if(find(target[m], mat[j][:max])):
                            confi_tg[m] += 1
                        if(find(asso[m], mat[j][:max])):
                            confi_as[m] += 1
                for k in range(0, tsize):
                    if(target[k] not in printed):   
                        confi_tg[k] = (float(support_cnts[s]) / float(confi_tg[k])) * 100.0
                        confi_as[k] = (float(support_cnts[s]) / float(confi_as[k])) * 100.0
                        f.write("{")
                        for i in range(0, len(target[k])):
                            f.write(str(target[k][i]))
                            if(i == len(target[k]) -1):
                                f.write("}\t")
                            else:
                                f.write(",")
                        f.write("{")
                        for i in range(0, len(asso[k])):
                            f.write(str(asso[k][i]))
                            if(i == len(asso[k]) -1):
                                f.write("}\t")
                            else:
                                f.write(",")
                        f.write(str(format(sup,".2f")) + "\t" + str(format(confi_tg[k], ".2f")) + "\n")
                        f.write("{")
                        for i in range(0, len(asso[k])):
                            f.write(str(asso[k][i]))
                            if(i == len(asso[k]) -1):
                                f.write("}\t")
                            else:
                                f.write(",")
                        f.write("{")
                        for i in range(0, len(target[k])):
                            f.write(str(target[k][i]))
                            if(i == len(target[k]) -1):
                                f.write("}\t")
                            else:
                                f.write(",")
                        f.write(str(format(sup,".2f")) + "\t" + str(format(confi_as[k], ".2f")) + "\n")
                        printed.append(asso[k])
        
    f.close
    end_time = time.time() - start_time
    print("Execution Successful, Time took: " + str(format(end_time, ".4f")))

def main(mins, strin, strout):
    global mat 
    f = open(strin, 'r')
    lines = f.readlines()
    cnt = len(lines)
    max_items = -1  # The number of items in the biggest line

    # Read file to generate matrix
    for l in lines:
        spliter = l.split('\t')

        idx = 0
        for particle in spliter:
            idx+=1

        if(idx > max_items):
            max_items = idx

    mat = np.full((cnt, max_items), -1)

    # filling matrix
    row = 0
    for l in lines:
        spliter = l.split('\t')
        col = 0
        for particle in spliter:
            mat[row][col] = int(particle)
            col += 1
        row += 1

    f.close
    apriori(cnt, mins, max_items, strout)


    

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])