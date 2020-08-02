import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
import math
import sys

import skinny
import helpers 
import dpautils


def main():
    P=helpers.gen_plaintexts(N)

    # Precompute intermediate values and power traces for different keys

    intermediate_values=[]
    for key in keys:
        val=dpautils.compute_intemediate_values(P,int(keys[0]))
        interm_values=val[0]
        clear_text=val[1]
        TK1=val[2].A1
        T = dpautils.gen_traces(interm_values, std)
        intermediate_values.append([interm_values,clear_text,TK1,T])

    
  
main()