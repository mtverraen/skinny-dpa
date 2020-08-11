import numpy as np
import helpers
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
import math
import sys
from numpy import arange

#std=[0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0,1.05]
std=arange(0.1, 1.5, 0.05)
print(std)

requires_traces_for_s_rate=[]
for s in std:
    infile="requires_traces_"+str(s)+".npy"
    traces=np.load(infile)
    requires_traces_for_s_rate.append(traces)


req_t =np.matrix(requires_traces_for_s_rate)
print(req_t)

simultanous=req_t[:,0].A1
majority_vote=req_t[:,1].A1
unanimous=req_t[:,2].A1
individual=req_t[:,3].A1
outfile= "required_traces_pr_sigma"

print(simultanous)
plt.figure()
plt.ylabel('Traces')
plt.xlabel('σ')
plt.plot(std,np.array(simultanous), label="simultanous", c="red")
plt.plot(std,np.array(majority_vote), label="majority vote", c="blue")
plt.plot(std,np.array(unanimous), label="unanimous", c="green")
plt.plot(std,np.array(individual), label="individual", c="black")
plt.grid(axis='y')
#plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places
plt.legend()
plt.draw()
plt.savefig(outfile)

