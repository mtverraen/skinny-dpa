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

N=15
std=1
number_of_experiments=50

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

simultanous_success_rate_pr_n=[]
Ns=list(range(1,N,1))
for n in Ns:
    correct=[]
    incorrect=[]
    discarded=[]
    
    for i,key in enumerate(keys):
        clear_text = intermediate_values[i][1]
        TK1 = intermediate_values[i][2]
        T = intermediate_values[i][3]
        
        TK1_0_guess=[]
        
        # Attack TK1 nibble i (first row of TK1)
        for i in range(4): 
            t=T[:n]
            ct=clear_text[:n]
            nibble_guess=dpautils.simultanous_atk(t,ct,i)
            TK1_0_guess.append(nibble_guess)
            
        #_____SUCCESS/FAIL_________________
        if(np.array_equal(TK1[0:4],TK1_0_guess)):
            correct.append(1)
            incorrect.append(0)
        else:
            incorrect.append(1)
            correct.append(0)
    simultanous_success_rate_pr_n.append([np.average(correct),np.average(incorrect)])

majority_vote_success_rate_pr_n=[]
Ns=list(range(1,N,1))
for n in Ns:
    correct=[]
    incorrect=[]
    discarded=[]
    
    for i,key in enumerate(keys):
        clear_text = intermediate_values[i][1]
        TK1 = intermediate_values[i][2]
        T = intermediate_values[i][3]
        TK1_0_guess=[]
        
        # Attack TK1 nibble i (first row of TK1)
        for i in range(4): 
            t=T[:n]
            ct=clear_text[:n]
            nibble_guess=dpautils.majority_vote_atk(t,ct,i)
            TK1_0_guess.append(nibble_guess)
            
        #_____SUCCESS/FAIL_________________
        if(np.array_equal(TK1[0:4],TK1_0_guess)):
            correct.append(1)
            discarded.append(0)
            incorrect.append(0)

        elif -1 in TK1_0_guess:
            discarded.append(1)
            correct.append(0)
            incorrect.append(0)
        else:
            incorrect.append(1)
            correct.append(0)
            discarded.append(0)
    majority_vote_success_rate_pr_n.append([np.average(correct),np.average(incorrect),np.average(discarded)])

unanimous_success_rate_pr_n=[]
Ns=list(range(1,N,1))
for n in Ns:
    correct=[]
    incorrect=[]
    discarded=[]
    
    for i,key in enumerate(keys):
        clear_text = intermediate_values[i][1]
        TK1 = intermediate_values[i][2]
        T = intermediate_values[i][3]
        TK1_0_guess=[]
        
        # Attack TK1 nibble i (first row of TK1)
        for i in range(4): 
            t=T[:n]
            ct=clear_text[:n]
            nibble_guess=dpautils.unanimous_attack(t,ct,i)
            TK1_0_guess.append(nibble_guess)
            
        
        #_____SUCCESS/FAIL_________________
        if(np.array_equal(TK1[0:4],TK1_0_guess)):
            correct.append(1)
            discarded.append(0)
            incorrect.append(0)

        elif -1 in TK1_0_guess:
            discarded.append(1)
            correct.append(0)
            incorrect.append(0)
        else:
            incorrect.append(1)
            correct.append(0)
            discarded.append(0)
    unanimous_success_rate_pr_n.append([np.average(correct),np.average(incorrect),np.average(discarded)])

individual_attack_success_rate_pr_n=[]
Ns=list(range(1,N,1))
for n in Ns:
    correct=[]
    incorrect=[]
    
    for i,key in enumerate(keys):
        clear_text = intermediate_values[i][1]
        TK1 = intermediate_values[i][2]
        T = intermediate_values[i][3]
        TK1_0_guess=[]
        
        # Attack TK1 nibble i (first row of TK1)
        for i in range(4): 
            t=T[:n]
            ct=clear_text[:n]
            nibble_guess=dpautils.individual_atk(t,ct,i)
            TK1_0_guess.append(nibble_guess)
            
        
        #_____SUCCESS/FAIL_________________
        if(np.array_equal(TK1[0:4],TK1_0_guess)):
            correct.append(1)
            incorrect.append(0)
        else:
            incorrect.append(1)
            correct.append(0)
    individual_attack_success_rate_pr_n.append([np.average(correct),np.average(incorrect)])


simultanous_confidence=np.matrix(simultanous_success_rate_pr_n)
correct=simultanous_confidence[:,0]
incorrect=simultanous_confidence[:,1]
outfile="confidence_simultanous.png"
plt.figure()
plt.plot(correct, label="valid and correct", c="red")
plt.plot(incorrect, label="valid and incorrect", c="blue")
plt.grid(axis='y')
plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places
plt.legend()
plt.draw()
plt.savefig(outfile)

majority_voting_confidence=np.matrix(majority_vote_success_rate_pr_n)
correct=majority_voting_confidence[:,0]
incorrect=majority_voting_confidence[:,1]
discarded=majority_voting_confidence[:,2]
outfile="confidence_majority_vote.png"
plt.figure()
plt.plot(correct, label="valid and correct", c="red")
plt.plot(incorrect, label="valid and incorrect", c="blue")
plt.plot(discarded, label="discarded", c="green")
plt.grid(axis='y')
plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places
plt.legend()
plt.draw()
plt.savefig(outfile)

unanimous_confidence=np.matrix(unanimous_success_rate_pr_n)
correct=unanimous_confidence[:,0]
incorrect=unanimous_confidence[:,1]
discarded=unanimous_confidence[:,2]
outfile="confidence_unanimous.png"
plt.figure()
plt.plot(correct, label="valid and correct", c="red")
plt.plot(incorrect, label="valid and incorrect", c="blue")
plt.plot(discarded, label="discarded", c="green")
plt.grid(axis='y')
plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places
plt.legend()
plt.draw()
plt.savefig(outfile)

individual_confidence=np.matrix(individual_attack_success_rate_pr_n)
correct=individual_confidence[:,0]
incorrect=individual_confidence[:,1]
outfile="confidence_individual.png"
plt.figure()
plt.plot(correct, label="valid and correct", c="red")
plt.plot(incorrect, label="valid and incorrect", c="blue")
plt.grid(axis='y')
plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places
plt.legend()
plt.draw()
plt.savefig(outfile)