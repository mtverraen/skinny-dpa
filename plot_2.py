import numpy as np
import helpers
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
import math
import sys
from numpy import arange

#std=[0.1,0.3,0.5,0.7]
std=arange(0.1, 1.1, 0.05)
requires_traces_for_s_rate=[]
for s in std:
    infile="requires_traces_"+str(s)+".npy"
    traces=np.load(infile)
    requires_traces_for_s_rate.append(traces)


req_t =np.matrix(requires_traces_for_s_rate)

simultanous=req_t[:,0]
majority_vote=req_t[:,1]
unanimous=req_t[:,2]
individual=req_t[:,3]
outfile= "required_traces_pr_sigma"
helpers.plot_required_traces(simultanous, majority_vote, 
                 unanimous, individual,
                 "simultanous","majority vote",
                 "unanimous","individual",
                outfile,std)

