import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import StrMethodFormatter
import math
import sys
import copy
import helpers 
import dpautils

from scipy import stats
from array import array
from operator import xor

np.set_printoptions(threshold=sys.maxsize)

N=20
std=0.5
number_of_experiments=50
keys=np.random.randint(2147483647, 9223372036854775807, size=number_of_experiments, dtype=np.int64)
alfa=0.005 
threshold=0.995

P=helpers.gen_plaintexts(N)

required_traces=[]
target_nibble=0

STD=np.arange(0.1, 3, 0.1)

all_intermediate=[]
for std in STD:
    # Precompute intermediate values and power traces for different keys
    intermediate_values=[]
    for key in keys:
        val=dpautils.compute_intemediate_values(P,int(keys[0]))
        interm_values=val[0]
        clear_text=val[1]
        TK1=val[2].A1
        T = dpautils.gen_traces(interm_values, std)
        intermediate_values.append([interm_values,clear_text,TK1,T])
        
    i=1 
    while True:
        res=[]
        for j,key in enumerate(keys):
            clear_text = intermediate_values[j][1]
            TK1 = intermediate_values[j][2]
            T = intermediate_values[j][3]
            t=T[:i]
            ct=clear_text[:i]
            nibble_guess=dpautils.simultanous_atk(t,ct,target_nibble)

            #_____SUCCESS/FAIL_________________
            if(TK1[target_nibble] == nibble_guess):
                res.append(1)
            else:
                res.append(0)

        if np.average(res)>=float(threshold):
            required_traces.append(i)
            break
        i+=1 
    i=1 
    while True:
        res=[]
        for j,key in enumerate(keys):
            clear_text = intermediate_values[j][1]
            TK1 = intermediate_values[j][2]
            T = intermediate_values[j][3]
            t=T[:i]
            ct=clear_text[:i]
            nibble_guess=dpautils.majority_vote_atk(t,ct,target_nibble)

            #_____SUCCESS/FAIL_________________
            if(TK1[target_nibble] == nibble_guess):
                res.append(1)
            else:
                res.append(0)

        if np.average(res)>=float(threshold):
            required_traces.append(i)
            break
        i+=1 
    i=1 
    while True:
        res=[]
        for j,key in enumerate(keys):
            clear_text = intermediate_values[j][1]
            TK1 = intermediate_values[j][2]
            T = intermediate_values[j][3]
            t=T[:i]
            ct=clear_text[:i]
            nibble_guess=dpautils.unanimous_attack(t,ct,target_nibble)

            #_____SUCCESS/FAIL_________________
            if(TK1[target_nibble] == nibble_guess):
                res.append(1)
            else:
                res.append(0)

        if np.average(res)>=float(threshold):
            required_traces.append(i)
            break
        i+=1 
    i=1 
    while True:
        res=[]
        for j,key in enumerate(keys):
            clear_text = intermediate_values[j][1]
            TK1 = intermediate_values[j][2]
            T = intermediate_values[j][3]
            t=T[:i]
            ct=clear_text[:i]
            nibble_guess=dpautils.individual_atk(t,ct,target_nibble)

            #_____SUCCESS/FAIL_________________
            if(TK1[target_nibble] == nibble_guess):
                res.append(1)
            else:
                res.append(0)

        if np.average(res)>=float(threshold):
            required_traces.append(i)
            break
        i+=1 
    all_intermediate.append(required_traces)
    
    np.save("all_traces",all_intermediate)