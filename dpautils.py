import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
import math
import sys

import skinny
import helpers 

from scipy import stats
from array import array
from operator import xor

np.set_printoptions(threshold=sys.maxsize)

def compute_intemediate_values(P,K): #Plaintexts list, K int
    known_RK=[]
    IS=[] #List of each p's IS' 
    CP=[] #P'

    for plaintext in P:
        #valid_modes = ['ECB', 'CTR', 'CBC', 'PCBC', 'CFB', 'OFB'] 
        cipher = skinny.SkinnyCipher(K,64,64) #TK1
        cipher.encrypt(plaintext)
        p=cipher.intermediary_values[0]
        RK=cipher.intermediary_values[1]
        
        p_xor_k = [array('B',map(xor,p[0], RK[0])),
                   array('B',map(xor, p[1], RK[1])),
                   array('B',map(xor, p[2], RK[2])),
                   array('B',map(xor, p[3], RK[3]))
                  ] 
        p_xor_k=np.matrix(p_xor_k)
        
        s=[]
        sbox4 = array('B', [12, 6, 9, 0, 1, 10, 2, 11, 3, 8, 5, 13, 4, 14, 7, 15])
        for x in np.nditer(p_xor_k): 
            s.append(sbox4[x])
            
        IS.append(np.matrix(s)) 
        CP.append(np.asmatrix(p).flatten())
        
    return [IS, CP, np.matrix(RK)]

def gen_traces(states, std):
    traces = []
    for i in range(len(states)):
        t=[]
        for j in range(16):
            mu=helpers.hw(states[i].item(j))
            t.append(np.random.normal(mu,std))
        traces.append(np.array(t).flatten())
    return np.array(traces)

# Formulate key hypothesis, V for single sbox
def compute_v(sbox_index,list_of_interm_p):
    sbox4 = array('B', [12, 6, 9, 0, 1, 10, 2, 11, 3, 8, 5, 13, 4, 14, 7, 15])
    V = []
    for i in range(len(list_of_interm_p)):
        row=[]
        for j in range(16):
            hyp_val = list_of_interm_p[i].item(sbox_index) ^ j
            row.append(helpers.hw(sbox4[hyp_val]))
        V.append(row)
    return V

def distinguisher(V,traces,target_nibble):
    std=0.5
    scores=[]
    for i in range(16):
        score=0
        for (t,v) in zip(traces,V):
            mu=v.item(i)
            d=sp.stats.norm(mu,std)
            l=t[target_nibble]
            score+= math.log(d.pdf(l))
        scores.append(score)
    return scores

def distinguisher_multivariate(V,T,kdi):
    V_0=V[0]
    V_1=V[1]
    V_2=V[2]
    std=0.5 #std of distinguisher
    scores=[]
    cov_matrix= np.identity(3) * std**2
        
    # Selection function   
    for i in range(16):
        score=0
        for j in range(len(T)):
           
            mu=[V_0[j].item(i),V_1[j].item(i),V_2[j].item(i)]
            Sigma=cov_matrix
            distrib = sp.stats.multivariate_normal(mu, Sigma)
            traces=[T[j][kdi[0]],T[j][kdi[1]],T[j][kdi[2]]]
            score+= math.log(distrib.pdf(traces))
        scores.append(score)
    return scores


def majority_vote_selector(candidates):
    votes_table = helpers.majority_vote(candidates)
    k_cand = max(votes_table,key=votes_table.get)
    
    if votes_table.get(k_cand) > 1:
        return k_cand # If there are a winner, return winner
    else: 
        return -1 # else Discard voting

def unanimous_selector(guesses):
    if len(set(guesses))== 1:
        return guesses[0]
    else:
        return -1

def plot_TK_recovery_rates(success_rate_unanimous,success_rate_majority_vote,success_rate_individual,succcess_rate_simultanous,outfile,sigma,keys):
    # Plot the results of each experiment and save to file

    fig, axs = plt.subplots(1,4,figsize=(28,7),sharey=True)
    #fig.suptitle('success-discard rate')
    plt.subplots_adjust(bottom=0.2)

    axs[0].set_title('unanimous')
    axs[1].set_title('majority vote')
    axs[2].set_title('individual')
    axs[3].set_title('simultanous')

    axs[0].plot(np.array(success_rate_unanimous), label="valid and correct", c="red")
    axs[1].plot(np.array(success_rate_majority_vote), label="valid and correct", c="red")
    axs[2].plot(np.array(success_rate_individual), label="valid and correct", c="red")
    
    std_string="experiments: "+str(len(keys))+" \n std: "+ str(sigma)
    axs[3].plot([], [], ' ', label=std_string) #dirty hack to get std into legend
    axs[3].plot(np.array(succcess_rate_simultanous), label="valid and correct", c="red")
    

    axs[3].legend(bbox_to_anchor=(1.1, 1.05))

    for ax in axs.flat:
        ax.set(xlabel='traces', ylabel='probability')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    fig.savefig(outfile, bbox_inches='tight')  
    
