import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

###---入力加速度をプロット---###

###---data input---###
mode = 2
duration = 8
fsamp = 5000
fp = 1.0
amp = 2.0
output = "inputwave"


def simple_sin(tim,fp,amp):
    return amp*np.sin(2*np.pi*fp*tim)


def tapered_sin(tim,fp,taper,duration,amp):
    wave = simple_sin(tim,fp,amp)
    coeff = np.ones_like(wave)

    ind = np.where((0 <= tim) & (tim < taper))
    coeff[ind] = tim[ind]/taper

    ind = np.where((duration-taper < tim) & (tim <= duration))
    coeff[ind] = (duration-tim[ind])/taper

    ind = np.where(duration < tim)
    coeff[ind] = 0.0

    return wave*coeff


def ricker(tim,fp,tp,amp):
    t1 = ((tim-tp)*np.pi*fp)**2
    return (2*t1-1)*np.exp(-t1)*amp


if mode == 0:
    wavename = "tapered_sin"
    taper = 2.0/fp      #tapered wave
    tim,dt = np.linspace(0,duration,int(fsamp*duration),endpoint=False,retstep=True)
    wave_acc = tapered_sin(tim,fp,taper,80.0,amp)
    wave_vel = np.cumsum(wave_acc) * dt
    ntim = len(tim)


elif mode == 1:
    wavename = "simple_sin"
    tim,dt = np.linspace(0,duration,int(fsamp*duration),endpoint=False,retstep=True)
    wave_acc = simple_sin(tim,fp,amp)
    wave_vel = np.cumsum(wave_acc) * dt
    ntim = len(tim)

elif mode == 2:
    wavename = "ricker"
    tim,dt = np.linspace(0,duration,int(fsamp*duration),endpoint=False,retstep=True)
    wave_acc = ricker(tim,fp,2.5,amp)
    wave_vel = np.cumsum(wave_acc) * dt
    ntim = len(tim)


# elif mode == 3:     #seisemic
#     wavefilename = "CHB008.vel"
#     wavename = "seisemic-"+wavefilename
#     fsamp = 2000
#     duration = 285
#
#     tim,dt = np.linspace(0,duration,int(fsamp*duration),endpoint=False,retstep=True)
#     wave_vel = seismic_wave("./input/"+wavefilename)
#     ntim = len(tim)


###---plot graph---###
plt.rcParams['font.family'] ='Times New Roman'
plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams["font.size"] = 18  #default 12

fig = plt.figure(figsize=(6,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel="time[s]",ylabel=r"acceleration$\mathrm{[m/s^2]}$",xmargin=0)
# ax1 = fig.add_subplot(1,1,1,xlabel="time[s]",ylabel=r"acceleration$\mathrm{[m/s^2]}$",xmargin=0,ylim=(-0.015,0.015))
ax1.xaxis.set_major_locator(mpl.ticker.MultipleLocator(1))
ax1.yaxis.set_major_locator(mpl.ticker.MultipleLocator(0.5))
ax1.yaxis.set_major_locator(mpl.ticker.MaxNLocator(7))
ax1.plot(tim,wave_acc,label="input wave",c="r",linestyle="solid")
plt.legend(edgecolor="None",facecolor="None",loc='upper right',borderaxespad=0)


###---save image file---###
# fig.savefig(output+".png",bbox_inches="tight",pad_inches=0.05)
fig.savefig(output+".svg",bbox_inches="tight",pad_inches=0.05)
plt.show()

