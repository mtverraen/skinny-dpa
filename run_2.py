import subprocess
from numpy import arange

std=arange(0.1, 1.5, 0.05)
# 0.1  0.15 0.2  0.25 0.3  0.35 0.4  0.45 0.5  0.55 0.6  0.65 0.7  0.75
# 0.8  0.85 0.9  0.95 1.   1.05 1.1  1.15 1.2  1.25 1.3  1.35 1.4  1.45]
print(std)
number_of_experiments=150
alfa=0.0001
sucess_rate=float(1-alfa)
for s in std:
    subprocess.Popen("python3 required_traces.py "+ str(s) +" "+str(number_of_experiments)+" "+str(sucess_rate), shell=True)



