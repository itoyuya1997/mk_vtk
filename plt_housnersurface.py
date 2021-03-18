import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

###---壁面変位が最大の時の水面形を標準化---### 

###---data input---###
input = "vs0z.disp"
output = "housner_stdsurface"
x_nnode = 21
area_x = 10
x = np.linspace(0,area_x,x_nnode,endpoint=True)       #グラフ横軸

#------------------------------------------------------#
dispz = pd.read_table(input,header=None,usecols=list(range(1,x_nnode+1)),sep=" ",engine='python')
surf = dispz.iloc[dispz.iloc[:,0].idxmax(),:]
max = surf.max()
min = surf.min()
std = (surf-min)/(max-min)


###---plot graph---###
# plt.rcParams['font.family'] ='Times New Roman'
# plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams["font.size"] = 12  #default 12

fig = plt.figure(figsize=(6,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel=r"$V_s\mathrm{[m]}$",ylabel="normalized displacement",xmargin=0,ymargin=0)
ax1.set_yticks([])
ax1.plot(x,std,c="k",linestyle="solid")


###---save image file---###
# fig.savefig(output+".png",bbox_inches="tight",pad_inches=0.05)
# fig.savefig(output+".svg",bbox_inches="tight",pad_inches=0.05)
plt.show()
