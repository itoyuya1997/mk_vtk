###---USE ONLY IN "output/<YYYYMMDD-time>"---###
#GL-1.5
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import gc
import os
if os.path.dirname(__file__):       #currentdirectoryをfile位置にセット
    os.chdir(os.path.dirname(__file__))

dir = "./"
label= ""
fsamp=4000
print("fsamp=",fsamp,",ヨシ！")
duration = 8
nid = int(70/5*2+1)         #応答スペクトルを求めたいnode id

plt.rcParams['font.family'] ='Times New Roman'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


nnode=255
nelem=42
#表面nodeの鉛直変位と表面elmのひずみプロット



##---read table--##
#time column省き，indexは0始まり
strxx = pd.read_table(dir+'strainxx.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
strzz = pd.read_table(dir+'strainzz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
vstr = strxx+strzz
del strxx,strzz
gc.collect()
strxz = pd.read_table(dir+'strainxz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
# dispx = pd.read_table(dir+'dispx.dat',header=None,sep="    ",usecols=list(range(1,86)),engine='python')
dispz = pd.read_table(dir+'dispz.dat',header=None,sep="    ",usecols=list(range(1,86)),engine='python')
# velx = pd.read_table('velx.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')
# velz = pd.read_table('velz.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')

strxz_absmax_tim = strxz.abs().max(axis=1).idxmax()
vstr_max_tim = vstr.abs().max(axis=1).idxmax()      #最大volstrainのindex
dispz_max_tim = dispz.max(axis=1).idxmax()
nid_dispz_max_tim = dispz.iloc[:,nid-1:nid].idxmax()

_x1,dx=np.linspace(0,210,42,endpoint=False,retstep=True)
x1 = _x1+dx/2
x2 = np.linspace(0,210,85)
x3 = tim = np.linspace(0,duration,int(fsamp*duration),endpoint=False)

#make plot
fig = plt.figure(figsize=(10,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel=r"$x$[m]",ylabel="shear strain",xlim=(0,210))
ax1.plot(x1,strxz.iloc[strxz_absmax_tim,:42],c="k",linestyle="solid")
filename = "topelem-shearst.png"
fig.savefig(filename, bbox_inches="tight", pad_inches=0.05)

plt.clf()
fig = plt.figure(figsize=(10,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel=r"$x$[m]",ylabel="volume strain",xlim=(0,210))
ax1.plot(x1,vstr.iloc[vstr_max_tim,:42],c="k",linestyle="solid")
filename = "topelem-volst.png"
fig.savefig(filename, bbox_inches="tight", pad_inches=0.05)

plt.clf()
fig = plt.figure(figsize=(10,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel=r"$x$[m]",ylabel="displacement[m]",xlim=(0,210))
ax1.plot(x2,dispz.iloc[dispz_max_tim,:85],c="k",linestyle="solid")
filename = "surface-dispz.png"
fig.savefig(filename, bbox_inches="tight", pad_inches=0.05)

plt.clf()
fig = plt.figure(figsize=(10,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel="time[s]",ylabel="displacement[m]")
ax1.plot(x3,dispz.iloc[:,nid-1:nid],c="k",linestyle="solid")
filename = "dispzspe-"+nid_dispz_max_tim.iloc[0].astype(str)+".png"
fig.savefig(filename, bbox_inches="tight", pad_inches=0.05)
