import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


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

mode = 2

if mode == 0:       ##housner
    wavename = "tapered_sin"
    fsamp = 5000
    duration = 30.0
    n = 0.5
    fs = 0.392      #sloshing frequency rely on mesh
    fp = n*fs
    taper = 2.0/fp      #tapered wave

    tim,dt = np.linspace(0,duration,int(fsamp*duration),endpoint=False,retstep=True)
    wave_acc = tapered_sin(tim,fp,taper,duration=80.0,amp=0.01)
    wave_vel = np.cumsum(wave_acc) * dt
    ntim = len(tim)


elif mode == 1:     ##housner v2
    wavename = "tapered_sin"
    fsamp = 4000
    duration = 60.0
    n = 0.5
    fs = 0.2669      #sloshing frequency rely on mesh
    fp = n*fs
    taper = 2.0/fp      #tapered wave

    tim,dt = np.linspace(0,duration,int(fsamp*duration),endpoint=False,retstep=True)
    wave_acc = tapered_sin(tim,fp,taper,duration=120.0,amp=0.01)
    wave_vel = np.cumsum(wave_acc) * dt
    ntim = len(tim)

elif mode == 2:
    wavename = "ricker"
    fsamp = 4000
    duration = 8.0

    tim,dt = np.linspace(0,duration,int(fsamp*duration),endpoint=False,retstep=True)
    wave_acc = ricker(tim,fp=1.0,tp=2.5,amp=2.0)
    wave_vel = np.cumsum(wave_acc) * dt
    ntim = len(tim)


# elif mode == 2:     #seisemic
#     wavefilename = "CHB008.vel"
#     wavename = "seisemic-"+wavefilename
#     fsamp = 2000
#     duration = 285
#
#     tim,dt = np.linspace(0,duration,int(fsamp*duration),endpoint=False,retstep=True)
#     wave_vel = seismic_wave("./input/"+wavefilename)
#     ntim = len(tim)


plt.rcParams['font.family'] ='Times New Roman'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
fig = plt.figure(figsize=(6,4),dpi=300)
ax1 = fig.add_subplot(1,1,1,xlabel=r"$time\mathrm{[s]}$",ylabel=r"$acceleration\mathrm{[m/s^2]}$",xmargin=0,ylim=(-2.5,2.5))
# ax1.xaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
# ax1.yaxis.set_major_locator(mpl.ticker.LinearLocator(5))
ax1.plot(tim,wave_acc,label="input wave",c="r",linestyle="solid")
plt.legend(edgecolor="None",facecolor="None")
fig.savefig("inputwave.png",bbox_inches="tight",pad_inches=0.05)
# plt.show()
