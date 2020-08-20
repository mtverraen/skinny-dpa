import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math
import sys

import skinny
import helpers 
import dpautils

from scipy import stats
from array import array
from operator import xor

np.set_printoptions(threshold=sys.maxsize)

N=20
std=0.5
number_of_experiments=1

keys=np.random.randint(2147483647, 9223372036854775807, size=number_of_experiments, dtype=np.int64) 
key= int(keys[0])

P=helpers.gen_plaintexts(N)
intermediate_values=[]

val=dpautils.compute_intemediate_values(P,int(key))
interm_values=val[0]
clear_text=val[1]
TK1=val[2].A1
T = dpautils.gen_traces(interm_values, std)
intermediate_values.append([interm_values,clear_text,TK1,T])

'''
Ns=list(range(1,N,1))
i=0
all_scores=[]
for n in Ns: 
    t=T[:n]
    ct=clear_text[:n]

    #scores=[]
    #for i in range(16):
    #    scores.append(dpautils.individual_atk_scores(t,ct,i))
    all_scores.append(dpautils.individual_atk_scores(t,ct,i))
m= np.matrix(all_scores)

m_rows=m.transpose()


plt.figure()
plt.ylabel('log-likelihood scores')
plt.xlabel('Traces')

for j in range(16):
    plt.plot(Ns,m_rows[j].A1,c='grey')
plt.plot(Ns,m_rows[TK1[i]].A1,c='black')
plt.draw()
plt.savefig('scores')

'''

a=dpautils.individual_atk_scores(T,clear_text,0)
b=dpautils.individual_atk_scores(T,clear_text,4)
c=dpautils.individual_atk_scores(T,clear_text,12)
L = [a, b, c]
scores_summed= np.sum(L, axis=0)

simultaneous=nibble_guess=dpautils.simultanous_atk_scores(T,clear_text,0)

print('__________________________________________')

print(a)
print('__________________________________________')

print(b)
print('__________________________________________')

print(c)
print('__________________________________________')

print(scores_summed)
print('_______________________________')

print(simultaneous)
print()
print(key)
