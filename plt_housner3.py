import numpy as np
import pandas as pd
import matplotlib as mpl
import os
import matplotlib.pyplot as plt
###---define "n"  and Vs_list---###
###---time-dispz on wall ---###

os.chdir(os.path.dirname(os.path.abspath(__file__)))



vs_list1 = ["vs0"]
vs_list2 = ["vs0m"]


dispz_data1 = []

for vs in vs_list1:
    dir = "./"+vs+"/dispz.dat"
    dispz = pd.read_table(dir,header=None,usecols=[1],sep="    ",engine='python')
    vardir = "./"+vs+"/var.txt"
    var = pd.read_table(vardir,sep=" ",header=None,engine='python').tail(1)
    fsamp = float(var.iloc[0,0])
    duration = float(var.iloc[0,1])
    tim,dt = np.linspace(0,duration,int(fsamp*duration),endpoint=False,retstep=True)

plt.rcParams['font.family'] ='Times New Roman'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


###mode-1
fig = plt.figure(figsize=(6,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel=r"$time\mathrm{[s]}$",ylabel=r"$displacement\mathrm{[m]}$",xmargin=0,ylim=(-0.03,0.03))
# ax1.xaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
ax1.plot(tim,dispz,c="r",linestyle="solid")
# plt.legend(edgecolor="None",facecolor="None")
fig.savefig("dispz-t",bbox_inches="tight",pad_inches=0.05)
plt.show()
