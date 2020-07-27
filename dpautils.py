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

# Maximum-log-likelihood distinguisher
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

# MLL via multivariate distribution of all same-key-dependent s-boxes
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

def simultanous_atk(T,clear_text_nibbles,target_nibble):
    kdi=helpers.determine_kdi(target_nibble) 
    V = []
    scores=[]
    for ind in kdi:
        V.append(np.matrix(compute_v(ind,clear_text_nibbles)))
    scores=distinguisher_multivariate(V,T,kdi)
    
    return(scores.index(max(scores)))

def majority_vote_atk(T,clear_text_nibbles,target_nibble):
    kdi=helpers.determine_kdi(target_nibble) 
    V = []
    scores=[]
    for ind in kdi:
        V.append(np.matrix(compute_v(ind,clear_text_nibbles)))
        scores.append(distinguisher(V[kdi.index(ind)],T,ind))

    argmax_scores = [score.index(max(score)) for score in scores] 

    votes_table = helpers.majority_vote(argmax_scores)
    k_cand = max(votes_table,key=votes_table.get)
    
    if votes_table.get(k_cand) > 1:
        return k_cand # If there are a winner, return winner
    else: 
        return -1 # else Discard voting

def unanimous_attack(T,clear_text_nibbles,target_nibble):
    kdi=helpers.determine_kdi(target_nibble) 
    V = []
    scores=[]
    for ind in kdi:
        V.append(np.matrix(compute_v(ind,clear_text_nibbles)))
        scores.append(distinguisher(V[kdi.index(ind)],T,ind))

    argmax_scores = [score.index(max(score)) for score in scores] #Argmax of list of scores 

    if len(set(argmax_scores))== 1:
        return argmax_scores[0]
    else:
        return -1

def individual_atk(T,clear_text_nibbles,target_nibble):
    V = np.matrix(compute_v(target_nibble,clear_text_nibbles))
    scores=distinguisher(V,T,target_nibble)
    
    return(scores.index(max(scores)))


