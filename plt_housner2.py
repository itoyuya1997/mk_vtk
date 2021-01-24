import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
###---normalized surface @maxdispz on wall ---###
###---use @ with finite micro folder---###
os.chdir(os.path.dirname(os.path.abspath(__file__)))

x_nelem = 5      #axis-x nelem(1m*1m mesh)
x_nnode = 2*x_nelem+1        #9-node elements
# vs_list1 = ["vs0"]
vs_list1 = ["vs0","vs1","vs2","vs3","vs4","vs5","vs10","vs50","vs100"]
vs_list2 = ["vs0m","vs1m","vs2m","vs3m","vs4m","vs5m","vs10m","vs50m","vs100m"]
dispz_data1 = []
x1 = np.linspace(0,x_nelem,x_nelem*2+1,endpoint=True)

plt.rcParams['font.family'] ='Times New Roman'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
fig = plt.figure(figsize=(6,4),dpi=300)


for vs in vs_list1:
    dispzdir = "./finite/"+vs+"/dispz.dat"
    vardir = "./finite/"+vs+"/var.txt"
    var = pd.read_table(vardir,sep=" ",header=None,engine='python').tail(1)
    fsamp = float(var.iloc[0,0])
    duration = float(var.iloc[0,1])
    tims = int(fsamp*duration)
    df= pd.read_table(dispzdir,header=None,sep="    ",usecols=list(range(1,x_nnode+1)),engine='python')      #rowindex0=node,surface nodes
    maxdispzid = df.iloc[:,1].idxmax()
    print(df.iloc[maxdispzid])
    min = df.iloc[maxdispzid].min()
    max = df.iloc[maxdispzid].max()
    print(min)
    print(max)
    normalized_sr=(df.iloc[maxdispzid]-min)/(max-min)
    print(normalized_sr)
    ax1 = fig.add_subplot(1,1,1,xlabel=r"$x\mathrm{[m]}$",ylabel=r"$normalized displacement$",xmargin=0,ymargin=0)
    ax1.set_yticks([])
    ax1.plot(x1,normalized_sr,c="k",linestyle="solid")
    filename = "static2"+vs+"f.png"
    fig.savefig(filename, bbox_inches="tight", pad_inches=0.05)
    # plt.show()
    plt.clf()

for vs in vs_list2:
    dispzdir = "./micro/"+vs+"/dispz.dat"
    vardir = "./micro/"+vs+"/var.txt"
    var = pd.read_table(vardir,sep=" ",header=None,engine='python').tail(1)
    fsamp = float(var.iloc[0,0])
    duration = float(var.iloc[0,1])
    tims = int(fsamp*duration)
    df= pd.read_table(dispzdir,header=None,sep="    ",usecols=list(range(1,x_nnode+1)),engine='python')      #rowindex0=node,surface nodes
    maxdispzid = df.iloc[:,1].idxmax()
    print(df.iloc[maxdispzid])
    min = df.iloc[maxdispzid].min()
    max = df.iloc[maxdispzid].max()
    print(min)
    print(max)
    normalized_sr=(df.iloc[maxdispzid]-min)/(max-min)
    print(normalized_sr)
    ax1 = fig.add_subplot(1,1,1,xlabel=r"$x\mathrm{[m]}$",ylabel=r"$normalized displacement$",xmargin=0,ymargin=0)
    ax1.set_yticks([])
    ax1.plot(x1,normalized_sr,c="k",linestyle="solid")
    filename = "static2"+vs+".png"
    fig.savefig(filename, bbox_inches="tight", pad_inches=0.05)
    # plt.show()
    plt.clf()
