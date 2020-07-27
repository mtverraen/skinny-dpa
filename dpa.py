import numpy as np
import scipy as sp

def recover_pk(val):

    # Inverse Mix Col
    mix_1 = val[0] ^ val[3]
    mix_2 = val[1] ^ val[3]
    mix_3 = val[2] ^ mix_2
    internal_state = [val[1], mix_3,mix_2, mix_1]

    # Inverse Shift Rows 
    internal_state = [internal_state[0],
                    [internal_state[1][1], internal_state[1][2], internal_state[1][3], internal_state[1][0]],
                    [internal_state[2][2], internal_state[2][3], internal_state[2][0], internal_state[2][1]],
                    [internal_state[3][3], internal_state[3][0], internal_state[3][1], internal_state[3][2]],]

    return internal_state

def simultanous_atk(T,clear_text_nibbles,target_nibble):
    kdi=helpers.determine_kdi(target_nibble) 
    V = []
    scores=[]
    for ind in kdi:
        V.append(np.matrix(dpautils.compute_v(ind,clear_text_nibbles)))
    scores=dpautils.distinguisher_multivariate(V,T,kdi)
    
    return(scores.index(max(scores)))

def majority_vote_atk(T,clear_text_nibbles,target_nibble):
    kdi=helpers.determine_kdi(target_nibble) 
    V = []
    scores=[]
    for ind in kdi:
        V.append(np.matrix(dpautils.compute_v(ind,clear_text)))
        scores.append(dpautils.distinguisher(V[kdi.index(ind)],T,ind))

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
        V.append(np.matrix(dpautils.compute_v(ind,clear_text)))
        scores.append(dpautils.distinguisher(V[kdi.index(ind)],T,ind))

    argmax_scores = [score.index(max(score)) for score in scores] #Argmax of list of scores 

    if len(set(argmax_scores))== 1:
        return argmax_scores[0]
    else:
        return -1

def individual_atk(T,clear_text_nibbles,target_nibble):
    V = np.matrix(dpautils.compute_v(ind,clear_text_nibbles))
    scores=dpautils.distinguisher(V,T,target_nibble)
    
    return(scores.index(max(scores)))
