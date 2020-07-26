import random
import string
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def hw(int_no):

    c = 0
    while(int_no):
        int_no &= (int_no - 1)
        c += 1
    return c

def gen_plaintexts(n):
    plaintexts=[]
    for i in range(n):
        plaintext=""
        for j in range(16):
            plaintext+=str(np.random.randint(0, 16))
        plaintexts.append(int(plaintext))
    return plaintexts

# Majority voting algorithm
def majority_vote(votes):
    # votes = list of integer votes
    votes_table = {} 
    for vote in votes:
        if vote in votes_table:    
            votes_table[vote] += 1 
        else:
            votes_table[vote] = 1  
    return votes_table

# Get list of all corresponding key dependant sboxes
def determine_kdi(target_nibble):
    if target_nibble in [0,4,12]:
        return [0,4,12]
    elif target_nibble in [1,5,13]:
        return [1,5,13]
    elif target_nibble in [2,6,14]:
        return [2,6,14]
    elif target_nibble in [3,7,15]:
        return [3,7,15]
    
def plot_multiple_attacks(plot_0,plot_1,plot_2,plot_3, label_0,label_1,label_2,label_3,outfile):
    plot_label= "TK1_0 recovery rate | experiments: "+ str(len(keys))+", std: "+str(std)
    plt.figure()
    plt.ylabel('Success rate')
    plt.xlabel('Traces')
    plt.plot(np.array(plot_0), label=label_0, c="red")
    plt.plot(np.array(plot_1), label=label_1, c="blue")
    plt.plot(np.array(plot_2), label=label_2, c="green")
    plt.plot(np.array(plot_3), label=label_3, c="black")

    plt.legend()
    plt.draw()
    plt.savefig(outfile)

def plot_single_attack(plot_0, label_0, outfile):
    plot_label= "TK1_1 recovery rate | experiments: "+ str(len(keys))+", std: "+str(std)
    plt.figure()
    plt.title(plot_label)
    plt.ylabel('Success rate')
    plt.xlabel('Traces')
    plt.plot(np.array(plot_0), label=label_0, c="black")
    plt.legend()
    plt.draw()

    plt.savefig(outfile)