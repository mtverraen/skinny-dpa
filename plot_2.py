import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
import math
import sys

std=[0.1,0.3,0.5,0.7,0.9]
requires_traces_for_s_rate=[]
for s in range(std):
    infile="requires_traces_"+str(s)+".npy"
    traces=np.load(infile)
    requires_traces_for_s_rate.append(traces)