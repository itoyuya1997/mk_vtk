import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
###---define d_list and f1---###
###---frequency response---###
###---compare dispz on wall with Housner-theory ---###

os.chdir(os.path.dirname(os.path.abspath(__file__)))

f1 = 0.392          #Housner 1'slosing frequency
# f1 = 0.2669

d_list = [0.003066,0.004183,0.0071671,0.021552]
# d_list = [0.006105,0.007581,0.0143404,0.043534]       #5*10
# d = d_dic[n]
#FD mode
n_list1 = ["0.3","0.5","0.7","0.9"]


dispz_data1 = []
dispz_data2 = []

for n in n_list1:
    dir = "./Housner"+n+"/finite/vs0/dispz.dat"
    maxdispz = pd.read_table(dir,header=None,usecols=[1],sep="    ",engine='python').max()
    dispz_data1.append(maxdispz.iloc[0])
    del maxdispz

f_list = np.array([0.3,0.5,0.7,0.9])*f1

plt.rcParams['font.family'] ='Times New Roman'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


###mode-1
fig = plt.figure(figsize=(6,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel=r"$f\mathrm{[Hz]}$",ylabel=r"$displacement\mathrm{[m]}$",xmargin=0)
ax1.plot(f_list,dispz_data1,label="Simultion results",c="g",linestyle="solid")
ax1.plot(f_list,d_list,label="Housner Theory",c="b",linestyle="solid")
plt.legend(edgecolor="None",facecolor="None")
filename1 = "housner-results.png"
fig.savefig(filename1,bbox_inches="tight",pad_inches=0.05)
plt.show()
