import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import gc

###---変位・ひずみの水平位置プロット---###
"""
--- plt_compe.py
 |-> vs0 -> ~.disp, ~.str, ~.vel
 |-> vs1-...
 |-> vs2-...
"""


###---define input---###
fdic = {0:"./vs0/",1:"./vs1/",2:"./vs2/"}
labeldic = {0:"Vs=0[m/s]",1:"Vs=1[m/s]",2:"Vs=2[m/s]"}
colordic = {0:"g",1:"b",2:"r"}
linedic = {0:"solid",1:"solid",2:"solid"}
y_label = "shear strain"

strainxx = "xx.str"
strainzz = "zz.str"
strainxz = "xz.str"
displacementx = "x.disp"
displacementz = "z.disp"
velocityx = "x.vel"
velocityz = "z.vel"

_x1,dx=np.linspace(0,210,42,endpoint=False,retstep=True)
x1 = _x1+dx/2
x2 = np.linspace(0,210,85)

output = "compe_plot"

###---set graph---###
# plt.rcParams['font.family'] ='Times New Roman'
# plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams["font.size"] = 12  #default 12

fig = plt.figure(figsize=(10,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel=r"$x$[m]",ylabel=y_label,xlim=(0,210))   #x_range制限


###---read table--###
for i in range(3):
    # strxx = pd.read_table(fdic[i]+strainxx,header=None,sep=" ",usecols=lambda x: x not in[0],engine='python')
    # strzz = pd.read_table(fdic[i]+strainzz,header=None,sep=" ",usecols=lambda x: x not in[0],engine='python')
    # strv = strxx+strzz      #体積ひずみ
    # del strxx,strzz
    # gc.collect()
    # strv_max_tim = strv.abs().max(axis=1).idxmax()      #volstrain絶対値の最大値のindex

    strxz = pd.read_table(fdic[i]+strainxz,header=None,sep=" ",usecols=lambda x: x not in[0],engine='python')
    strxz_absmax_tim = strxz.abs().max(axis=1).idxmax()    #shearstrain絶対値の最大値のindex

    # dispx = pd.read_table(fdic[i]+displacementx,header=None,sep=" ",usecols=lambda x: x not in[0],engine='python')
    # dispz = pd.read_table(fdic[i]+displacementz,header=None,sep=" ",usecols=lambda x: x not in[0],engine='python')
    # velx = pd.read_table(fdic[i]+velocityx,header=None,sep=" ",usecols=lambda x: x not in[0],engine='python')
    # velz = pd.read_table(fdic[i]+velocityz,header=None,sep=" ",usecols=lambda x: x not in[0],engine='python')

    ax1.plot(x1,strxz.iloc[strxz_absmax_tim,:42].abs(),c=colordic[i],linestyle=linedic[i],label=labeldic[i])        #plot範囲指定

plt.legend(edgecolor="None",facecolor="None")


###---save image file---###
# fig.savefig(output+".png",bbox_inches="tight",pad_inches=0.05)
# fig.savefig(output+".svg",bbox_inches="tight",pad_inches=0.05)
plt.show()