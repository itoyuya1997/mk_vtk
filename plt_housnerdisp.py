import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

###---壁面近傍の鉛直変位とHousner解をプロット---###

mode = 1    #0:default 1:FD-MD重ね合わせ

###---data input---###
housner = 0.1
output = "housner_disp"
vs_list = [0, 1, 2, 3, 4, 5, 6, 8, 10]

#------------------------------------------------------#
if mode == 0:
    dispz_list = []
    for vs in vs_list:
        input = "./vs"+str(vs)+"z.disp"
        maxdispz = pd.read_table(input,header=None,usecols=[1],sep=" ",engine='python').max()
        dispz_list.append(maxdispz)
elif mode == 1:
    FDdispz_list = []
    MDdispz_list = []
    for vs in vs_list:
        input1 = "./FD/vs"+str(vs)+"z.disp"
        input2 = "./MD/vs"+str(vs)+"z.disp"
        maxdispz1 = pd.read_table(input1,header=None,usecols=[1],sep=" ",engine='python').max()
        maxdispz2 = pd.read_table(input2,header=None,usecols=[1],sep=" ",engine='python').max()
        FDdispz_list.append(maxdispz1)
        MDdispz_list.append(maxdispz2)


###---plot graph---###
# plt.rcParams['font.family'] ='Times New Roman'
# plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams["font.size"] = 12  #default 12

fig = plt.figure(figsize=(6,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel=r"$V_s\mathrm{[m/s]}$",ylabel=r"displacement$\mathrm{[m]}$",xmargin=0,yscale="log")
ax1.scatter(0,housner,marker="x",label="Housner Theory",c="b",s=50,clip_on=False)
if mode == 0:
    ax1.plot(vs_list,dispz_list,label="Simultion results",c="g",linestyle="solid",marker=".",ms=5)
elif mode == 1:
    ax1.plot(vs_list,FDdispz_list,label="finite deformation",c="g",linestyle="solid",marker=".",ms=5)
    ax1.plot(vs_list,MDdispz_list,label="micro deformation",c="r",linestyle="solid",marker=".",ms=5)
plt.legend(edgecolor="None",facecolor="None", borderaxespad=0)


###---save image file---###
# fig.savefig(output+".png",bbox_inches="tight",pad_inches=0.05)
# fig.savefig(output+".svg",bbox_inches="tight",pad_inches=0.05)
plt.show()
