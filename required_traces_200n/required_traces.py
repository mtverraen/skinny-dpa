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
std=float(sys.argv[1])
number_of_experiments=int(sys.argv[2])

keys=np.random.randint(2147483647, 9223372036854775807, size=number_of_experiments, dtype=np.int64)

i=1
# multivariate, majority vote, unanimous, individual
required_traces=[]
while True:
    res=[]
    for key in (keys):
        P=helpers.gen_plaintexts(i)
        val=dpautils.compute_intemediate_values(P,int(key))
        interm_values=val[0]
        clear_text=val[1]
        TK1=val[2].A1
        T = dpautils.gen_traces(interm_values, std)

        TK1_0_guess=[]
        
        # Attack TK1 nibble i (first row of TK1)
        for j in range(4): 
            nibble_guess=dpautils.simultanous_atk(T,clear_text,j)
            TK1_0_guess.append(nibble_guess)
            
        #_____SUCCESS/FAIL_________________
        if(np.array_equal(TK1[0:4],TK1_0_guess)):
            res.append(1)
        else:
            res.append(0)
    if np.average(res)>=float(sys.argv[3]):
        required_traces.append(i)
        break
    i+=1

i=1
while True:
    res=[]
    for key in (keys):
        P=helpers.gen_plaintexts(i)
        val=dpautils.compute_intemediate_values(P,int(key))
        interm_values=val[0]
        clear_text=val[1]
        TK1=val[2].A1
        T = dpautils.gen_traces(interm_values, std)

        TK1_0_guess=[]
        
        # Attack TK1 nibble i (first row of TK1)
        for j in range(4): 
            nibble_guess=dpautils.majority_vote_atk(T,clear_text,j)
            TK1_0_guess.append(nibble_guess)
            
        #_____SUCCESS/FAIL_________________
        if(np.array_equal(TK1[0:4],TK1_0_guess)):
            res.append(1)
        else:
            res.append(0)
    if np.average(res)>=float(sys.argv[3]):
        required_traces.append(i)
        break
    i+=1

i=1
while True:
    res=[]
    for key in keys:
        P=helpers.gen_plaintexts(i)
        val=dpautils.compute_intemediate_values(P,int(key))
        interm_values=val[0]
        clear_text=val[1]
        TK1=val[2].A1
        T = dpautils.gen_traces(interm_values, std)

        TK1_0_guess=[]
        
        # Attack TK1 nibble i (first row of TK1)
        for j in range(4): 
            nibble_guess=dpautils.unanimous_attack(T,clear_text,j)
            TK1_0_guess.append(nibble_guess)
            
        #_____SUCCESS/FAIL_________________
        if(np.array_equal(TK1[0:4],TK1_0_guess)):
            res.append(1)
        else:
            res.append(0)
    if np.average(res)>=float(sys.argv[3]):
        required_traces.append(i)
        break
    i+=1
    
i=1
while True:
    res=[]
    for key in keys:
        P=helpers.gen_plaintexts(i)
        val=dpautils.compute_intemediate_values(P,int(key))
        interm_values=val[0]
        clear_text=val[1]
        TK1=val[2].A1
        T = dpautils.gen_traces(interm_values, std)

        TK1_0_guess=[]
        
        # Attack TK1 nibble i (first row of TK1)
        for j in range(4): 
            nibble_guess=dpautils.individual_atk(T,clear_text,j)
            TK1_0_guess.append(nibble_guess)
            
        #_____SUCCESS/FAIL_________________
        if(np.array_equal(TK1[0:4],TK1_0_guess)):
            res.append(1)
        else:
            res.append(0)
    if np.average(res)>=float(sys.argv[3]):
        required_traces.append(i)
        break
    i+=1

outfile="requires_traces_"+str(std)+".npy"
np.save(outfile,np.array(required_traces))



