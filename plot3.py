import numpy as np
import helpers
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
import math
import sys
from numpy import arange

std_03=np.load("TK1-10-recovery-rate-std-0.3.npy")
std_05=np.load("TK1-10-recovery-rate-std-0.5.npy")
std_07=np.load("TK1-10-recovery-rate-std-0.7.npy")
std_09=np.load("TK1-10-recovery-rate-std-0.9.npy")

L=[std_03,std_05,std_07,std_09]
STD=[0.3,0.5,0.7,0.9]

for i in range(len(L)):
    l=L[i]
    std=STD[i]
    #simultaneous=[]
    #majority_vote=[]
    #unanimous=[]
    #standard=[]
    outfile="TK1-10-recovery-rate-std-"+str(std)+".png"

    helpers.plot_multiple_attacks(l[0].tolist(), l[1].tolist(), 
                l[2].tolist(), l[3].tolist(),
                 "simultaneous","majority vote",
                 "unanimous","standard",
                outfile)