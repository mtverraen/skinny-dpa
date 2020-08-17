import numpy as np

p=[9,15,8,13,10,14,12,11,0,1,2,3,4,5,6,7]

M=np.matrix([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])

m=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
print("Permutation of TK1 throug the round functions")
for j in range(32):
    t=np.array(m).reshape(4,4)
    print("----------")
    print("round: "+str(j+1))
    print("----------")
    print(t)

    tmp=[]
    for i in range(len(p)):
        tmp.append(m[p[i]])
    m=tmp
    

