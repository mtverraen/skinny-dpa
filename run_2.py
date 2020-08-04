import subprocess

std=[0.1,0.3,0.5,0.7,0.9]
number_of_experiments=100
alfa=0.1
sucess_rate=float(1-alfa)
for s in std:
    subprocess.Popen("python3 required_traces.py "+ str(s) +" "+str(number_of_experiments)+" "+str(sucess_rate), shell=True)



