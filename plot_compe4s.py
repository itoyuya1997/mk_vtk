###---USE ONLY IN "output/<YYYYMMDD-time>"---###
#GL-1.5
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import gc
import os
if os.path.dirname(__file__):       #currentdirectoryをfile位置にセット
    os.chdir(os.path.dirname(__file__))

dir = "./id3rifp1.0tp2.5amp2.0/finite/vs0/"
dir1 = "./id3rifp1.0tp2.5amp2.0/finite/vs1/"
dir2 = "./id3rifp1.0tp2.5amp2.0/finite/vs2/"
dir3 = "./id3rifp1.0tp2.5amp2.0/finite/vs3/"
label= "Vs=0[m/s]"
label1= "Vs=1[m/s]"
label2= "Vs=2[m/s]"
label3= "Vs=3[m/s]"

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
# dispx = pd.read_table(dir+'dispx.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
# dispz = pd.read_table(dir+'dispz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
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
# dispx1 = pd.read_table(dir1+'dispx.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
# dispz1 = pd.read_table(dir1+'dispz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
# velx = pd.read_table('velx.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')
# velz = pd.read_table('velz.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')

strxz_absmax_tim1 = strxz1.abs().max(axis=1).idxmax()
vstr_max_tim1 = vstr1.abs().max(axis=1).idxmax()      #最大volstrainのindex

strxx2 = pd.read_table(dir2+'strainxx.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
strzz2 = pd.read_table(dir2+'strainzz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
vstr2 = strxx2+strzz2
del strxx2,strzz2
gc.collect()
strxz2 = pd.read_table(dir2+'strainxz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
# dispz2 = pd.read_table(dir2+'dispz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
# dispx2 = pd.read_table(dir2+'dispx.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
# velx = pd.read_table('velx.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')
# velz = pd.read_table('velz.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')

strxz_absmax_tim2 = strxz2.abs().max(axis=1).idxmax()
vstr_max_tim2 = vstr2.abs().max(axis=1).idxmax()      #最大volstrainのindex

strxx3 = pd.read_table(dir3+'strainxx.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
strzz3 = pd.read_table(dir3+'strainzz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
vstr3 = strxx3+strzz3
del strxx3,strzz3
gc.collect()
strxz3 = pd.read_table(dir3+'strainxz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
# dispx3 = pd.read_table(dir3+'dispx.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
# dispz3 = pd.read_table(dir3+'dispz.dat',header=None,sep="    ",usecols=list(range(1,43)),engine='python')
# velx = pd.read_table('velx.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')
# velz = pd.read_table('velz.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')

strxz_absmax_tim3 = strxz3.abs().max(axis=1).idxmax()
vstr_max_tim3 = vstr3.abs().max(axis=1).idxmax()      #最大volstrainのindex


#make plot
fig = plt.figure(figsize=(10,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel=r"$x$[m]",ylabel="shear strain",xlim=(0,210),ylim=(0.0,0.0125))
_x1,dx=np.linspace(0,210,42,endpoint=False,retstep=True)
x1 = _x1+dx/2
ax1.plot(x1,strxz.iloc[strxz_absmax_tim,:42].abs(),c="g",linestyle="solid",label=label)
ax1.plot(x1,strxz1.iloc[strxz_absmax_tim1,:42].abs(),c="b",linestyle="solid",label=label1)
ax1.plot(x1,strxz2.iloc[strxz_absmax_tim2,:42].abs(),c="r",linestyle="solid",label=label2)
ax1.plot(x1,strxz3.iloc[strxz_absmax_tim3,:42].abs(),c="#a65628",linestyle="solid",label=label3)
plt.legend(edgecolor="None",facecolor="None")
filename = "shearst-c-vs1.png"
fig.savefig(filename, bbox_inches="tight", pad_inches=0.05)

plt.clf()
fig = plt.figure(figsize=(10,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel=r"$x$[m]",ylabel="volume strain",xlim=(0,210),ylim=(0,0.018))
ax1.plot(x1,vstr.iloc[vstr_max_tim,:42].abs(),c="g",linestyle="--",label=label )
ax1.plot(x1,vstr1.iloc[vstr_max_tim1,:42].abs(),c="b",linestyle="--",label=label1 )
ax1.plot(x1,vstr2.iloc[vstr_max_tim2,:42].abs(),c="r",linestyle="--",label=label2 )
ax1.plot(x1,vstr3.iloc[vstr_max_tim3,:42].abs(),c="#a65628",linestyle="--",label=label3 )
plt.legend(edgecolor="None",facecolor="None")
filename = "volst-c-vs1.png"
fig.savefig(filename, bbox_inches="tight", pad_inches=0.05)
#ax.plot後て元arraydelしてもいいんすかね...
