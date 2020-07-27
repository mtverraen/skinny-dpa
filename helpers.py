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
    
def plot_multiple_attacks(plot_0,plot_1,plot_2,plot_3, label_0,label_1,label_2,label_3,outfile):
    #plot_label= "TK1_0 recovery rate | experiments: "+ str(len(keys))+", std: "+str(std)
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
    plt.figure()
    plt.ylabel('Success rate')
    plt.xlabel('Traces')
    plt.plot(np.array(plot_0), label=label_0, c="black")
    plt.legend()
    plt.draw()

    plt.savefig(outfile)
    
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
    
    #std_string="experiments: "+str(len(keys))+" \n std: "+ str(sigma)
    #axs[3].plot([], [], ' ', label=std_string) #dirty hack to get std into legend
    axs[3].plot(np.array(succcess_rate_simultanous), label="valid and correct", c="red")
    

    axs[3].legend(bbox_to_anchor=(1.1, 1.05))

    for ax in axs.flat:
        ax.set(xlabel='traces', ylabel='probability')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    fig.savefig(outfile, bbox_inches='tight')  
    