import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
###---define "n"  and Vs_list---###
###---compare dispz on wall with Housner-theory ---###

os.chdir(os.path.dirname(os.path.abspath(__file__)))

L = 5
n = 0.3

d_dic = {0.3:0.003066,0.5:0.004183,0.7:0.0071671,0.9:0.021552,1.0:2.189240}
d = d_dic[n]
#FD mode
# vs_list1 = ["vs0","vs1","vs2","vs3","vs4","vs5","vs10","vs50","vs100"]
# vs_list2 = ["vs0","vs1","vs2","vs3","vs4","vs5","vs10"]
# mode = 0

#micro mode
vs_list1 = ["vs0m","vs1m","vs2m","vs3m","vs4m","vs5m","vs10m","vs50m","vs100m"]
vs_list2 = ["vs0m","vs1m","vs2m","vs3m","vs4m","vs5m","vs10m"]
mode = 1

dispz_data1 = []
dispz_data2 = []

for vs in vs_list1:
    dir = "./micro/"+vs+"/dispz.dat"
    maxdispz = pd.read_table(dir,header=None,usecols=[1],sep="    ",engine='python').max()
    dispz_data1.append(maxdispz.iloc[0])
    if vs in vs_list2:
        dispz_data2.append(maxdispz.iloc[0])
    del maxdispz

x1 = [0,1,2,3,4,5,10,50,100]
x2 = [0,1,2,3,4,5,10]

plt.rcParams['font.family'] ='Times New Roman'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


###mode-1
fig = plt.figure(figsize=(6,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel=r"$V_s\mathrm{[m/s]}$",ylabel=r"$displacement\mathrm{[m]}$",xmargin=0,yscale="log",ylim=(10**(-18),10**(-1)))
ax1.scatter(0,d,marker="x",label="Housner Theory",c="b",s=50,clip_on=False)
ax1.plot(x1,dispz_data1,label="Simultion results",c="g",linestyle="solid",marker=".",ms=5)
plt.legend(edgecolor="None",facecolor="None")
if mode == 0:
    filename1 = "housner"+str(n)+"fL.png"
else:
    filename1 = "housner"+str(n)+"mL.png"
fig.savefig(filename1,bbox_inches="tight",pad_inches=0.05)
# plt.show()

##mode-2
fig = plt.figure(figsize=(6,4),dpi=300)
ax2 = fig.add_subplot(1,1,1,xlabel=r"$V_s\mathrm{[m/s]}$",ylabel=r"$displacement\mathrm{[m]}$",xmargin=0,yscale="log",ylim=(10**(-18),10**(-1)))
ax2.scatter(0,d,marker="x",label="Housner Theory",c="b",s=50,clip_on=False)
ax2.plot(x2,dispz_data2,label="Simultion results",c="g",linestyle="solid",marker=".",ms=5)
plt.legend(edgecolor="None",facecolor="None")
if mode == 0:
    filename2 = "housner"+str(n)+"fR.png"
else:
    filename2 = "housner"+str(n)+"mR.png"
fig.savefig(filename2,bbox_inches="tight",pad_inches=0.05)
# plt.show()
