import numpy as np
import matplotlib.pyplot as plt
import os

def main():
    rho = 1000  #kg/m^3
    L = 2.5     #rectangle tank width/2
    D = 5       #depth
    n = 0.5     #周波数倍率


    M = rho*2*L*D
    m = M*0.83*np.tanh(1.6*D/L)/1.6/D*L     #M1
    k = 3*m**2*9.8*D/M/L/L
    # f = 1/(2*np.pi)*np.sqrt(k/m)
    f = 0.39244
    h = 0.0        #attenuation
    c = 2 * np.sqrt(m*k)*h
    dt = 0.01
    N = 2**15
    Nprd = 1
    beta = 1 / 6

    Maxdisb = []
    Maxvelb = []
    Maxacc = []
    Dis = np.zeros((N))
    Vel = np.zeros((N))
    Acc = np.zeros((N))
    Zacc = np.zeros((N))

    # for T in np.linspace(0.1, 10, Nprd):
    T = 1/(f*n)
    NT=T/dt
    acc = np.zeros(N)
    for i in range(1, N):
        acc[i]+=np.sin(2*np.pi*i/NT)*0.01       #amp
        Acc1 = m + 0.5 * dt * c + beta * dt * dt * k
        Acc2 = -m * acc[i] - c * (Vel[i - 1] + 0.5 * dt * Acc[i - 1]) - k * (
            Dis[i - 1] + dt * Vel[i - 1] + (0.5 - beta) * dt * dt * Acc[i - 1])
        Acc[i] = Acc2 / Acc1
        Vel[i] = Vel[i - 1] + dt * (Acc[i - 1] + Acc[i]) / 2
        Dis[i] = Dis[i - 1] + dt * Vel[i - 1] + \
            (0.5 - beta) * dt * dt * Acc[i - 1] + beta * dt * dt * Acc[i]
    Zacc = Acc + acc
    a = np.max(np.abs(Dis))
    Maxdisb.append(np.max(np.abs(Dis)))
    Maxvelb.append(np.max(np.abs(Vel)))
    Maxacc.append(np.max(np.abs(Zacc)))

    d = 0.84*a*(k*L/m/9.8)/(1-a/L*(k*L/m/9.8)**2)

    print("f=",f)   #1次スロッシング周波数
    print("n=",n)   #周波数倍率
    print("m1",m)   #振動質量
    print("k1",k)   #振動バネ
    print("A1=",a)  #相対変位振幅
    print("d=",d)   #壁面鉛直変位

    Maxdisb=np.array(Maxdisb)
    # plt.figure()
    # plt.plot( np.linspace(0.1, 10, Nprd),Maxdisb)
    # plt.show()
    return

if __name__=="__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    # print(path)
    os.chdir(path)
    main()
