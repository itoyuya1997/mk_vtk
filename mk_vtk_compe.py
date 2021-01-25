###---USE ONLY IN "output/<YYYYMMDD-time>"---###
#GL-1.5
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import gc
import os
if os.path.dirname(__file__):       #currentdirectoryをfile位置にセット
    os.chdir(os.path.dirname(__file__))

dir = "./finite/vs0/"
dir1 = "./finite/vs1/"
label= "vs0"
label1= "vs1"


plt.rcParams['font.family'] ='Times New Roman'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


nnode=255
nelem=42




##---read table--##
#time column省き，indexは0始まり
strxx = pd.read_table(dir+'strainxx.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
strzz = pd.read_table(dir+'strainzz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
vstr = strxx+strzz
del strxx,strzz
gc.collect()
strxz = pd.read_table(dir+'strainxz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
dispx = pd.read_table(dir+'dispx.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
dispz = pd.read_table(dir+'dispz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
# velx = pd.read_table('velx.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')
# velz = pd.read_table('velz.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')

strxz_absmax_tim = strxz.abs().max(axis=1).idxmax()
vstr_max_tim = vstr.max(axis=1).idxmax()      #最大volstrainのindex


strxx1 = pd.read_table(dir1+'strainxx.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
strzz1 = pd.read_table(dir1+'strainzz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
vstr1 = strxx1+strzz1
del strxx1,strzz1
gc.collect()
strxz1 = pd.read_table(dir1+'strainxz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
dispx1 = pd.read_table(dir1+'dispx.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
dispz1 = pd.read_table(dir1+'dispz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
# velx = pd.read_table('velx.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')
# velz = pd.read_table('velz.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')

strxz_absmax_tim1 = strxz1.abs().max(axis=1).idxmax()
vstr_max_tim1 = vstr1.max(axis=1).idxmax()      #最大volstrainのindex

#make plot
fig = plt.figure(figsize=(10,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel=r"$x\mathrm{[m]}$",ylabel=r"$shear strain$",xlim=(0,210))
_x1,dx=np.linspace(0,210,42,endpoint=False,retstep=True)
x1 = _x1+dx/2
ax1.plot(x1,strxz.iloc[strxz_absmax_tim,:42],c="g",linestyle="solid",label="shear strain")
ax1.plot(x1,strxz.iloc[strxz_absmax_tim1,:42],c="b",linestyle="solid",label="shear strain")
plt.legend(edgecolor="None",facecolor="None")
filename = "shearst-c.png"
fig.savefig(filename, bbox_inches="tight", pad_inches=0.05)

plt.clf()
fig = plt.figure(figsize=(10,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel=r"$x\mathrm{[m]}$",ylabel=r"$volume strain$",xlim=(0,210))
ax1.plot(x1,strxz.iloc[vstr_max_tim,:42],c="r",linestyle="solid",label=label )
ax1.plot(x1,strxz.iloc[vstr_max_tim1,:42],c="m",linestyle="solid",label=label1 )
plt.legend(edgecolor="None",facecolor="None")
filename = "volst-c.png"
fig.savefig(filename, bbox_inches="tight", pad_inches=0.05)
