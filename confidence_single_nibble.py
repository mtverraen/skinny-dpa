import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import StrMethodFormatter
import math
import sys

import skinny
import helpers 
import dpautils

from scipy import stats
from array import array
from operator import xor

np.set_printoptions(threshold=sys.maxsize)

#N=int(sys.argv[1])
#std=float(sys.argv[2])
#number_of_experiments=int(sys.argv[3])

N=50
std=4
number_of_experiments=200

TK1_0=[0,1,2,3] # 3x traces
TK1_1=[4,5,6,7]
TK1_2_unsorted=[0,1,2,3] # 3x traces
Tk1_3_unsorted=[8,9,10,11]

keys=np.random.randint(2147483647, 9223372036854775807, size=number_of_experiments, dtype=np.int64) 

P=helpers.gen_plaintexts(N)

# Precompute intermediate values and power traces for different keys

intermediate_values=[]
for key in keys:
    val=dpautils.compute_intemediate_values(P,int(key))
    interm_values=val[0]
    clear_text=val[1]
    TK1=val[2].A1
    T = dpautils.gen_traces(interm_values, std)
    intermediate_values.append([interm_values,clear_text,TK1,T])


target_nibble=0 
n=20
simultanous_success_rate_pr_n=[]
'''
for i,key in enumerate(keys):
    clear_text = intermediate_values[i][1]
    TK1 = intermediate_values[i][2]
    T = intermediate_values[i][3]
        
    TK1_0_guess=[]
    
    t=T[:n]
    ct=clear_text[:n]
    nibble_guess_sim=dpautils.simultanous_atk_scores(t,ct,target_nibble)
    print(nibble_guess_sim)
    print(TK1[target_nibble]) 
'''

for i,key in enumerate(keys):
    clear_text = intermediate_values[i][1]
    TK1 = intermediate_values[i][2]
    T = intermediate_values[i][3]
            
    TK1_0_guess=[]
        
    t=T[:n]
    ct=clear_text[:n]
    nibble_guess_unanimous=dpautils.unanimous_attack_scores(t,ct,target_nibble)
    print("_________")
    print(nibble_guess_unanimous)
    nibble_guess_sim=dpautils.simultanous_atk_scores(t,ct,target_nibble)
    nibble_guess_individual=dpautils.individual_atk_scores(t,ct,target_nibble)
    print(nibble_guess_sim)
    print("----------------")
    print(nibble_guess_individual)
    print("----------------")
    print(TK1[target_nibble])
    print(key)
        
    s=[-1802.0786226740265, -1977.4312082991619, -1837.4082796228186, -2172.8803880102405, -2157.458088471014, -1777.9296073217881, -2193.1503783663766, -1726.5123043200974, -2010.4605469575095, -2209.3005738596603, -1926.9769498159665, -2045.6974539558312, -2119.1720297814954, -1826.4460421857852, -2030.3640092518472, -1904.747614553191]
    u=[-1802.0786226740265, -1977.4312082991619, -1837.4082796228186, -2172.8803880102405, -2157.458088471014, -1777.9296073217881, -2193.1503783663766, -1726.5123043200974, -2010.4605469575095, -2209.3005738596603, -1926.9769498159665, -2045.6974539558312, -2119.1720297814954, -1826.4460421857852, -2030.3640092518472, -1904.747614553191]
    ind=[-375.93465171412174, -447.70923088332717, -387.01749186021163, -549.3297270020086, -626.5670864744395, -380.631239309466, -570.5468328821712, -360.2835254784154, -459.9156524842127, -581.7266262428548, -362.95915629537774, -442.23247408142845, -576.2218110105791, -410.08863760428864, -519.7838233910561, -365.97811022354756]
    # key = 8571468538266339536
    # Correct k = 7






