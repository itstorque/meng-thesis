import numpy as np
from PyLTSpice import LTSpice_RawRead
import matplotlib.pyplot as plt

plt.figure(figsize=(17/2,3/2))

freq = 1/np.sqrt(1e-6*1e-3)
a1 = None
k = -1
labels = ["Output of Behavioural Source B1"]
for file in ["res.raw"]:
    k+=1
    LT = LTSpice_RawRead.LTSpiceRawRead(file)
    IR1 = LT.get_trace("V(nc_01)")
    x = LT.get_trace(0)  # Zero is always the X axis
    steps = LT.get_steps()
    for step in range(len(steps)):
        # print(steps[step])
        plt.plot(abs(x.get_wave(step))*1e9, IR1.get_wave(step)*1e3, label=labels[k])
        plt.scatter(abs(x.get_wave(step))*1e9, IR1.get_wave(step)*1e3, marker='x', color='black')
        
        plt.ylabel("Voltage (mV)")
        
        # anal = 100e-6*np.sin(freq*x.get_wave(step)[:-10])
        
        # if a1 is None: a1 = IR1.get_wave(step)[:-10]

        # print(max(IR1.get_wave(step)[:-10]))
# plt.plot(x.get_wave(step)[:-10], , label="Analytic Solution")

        # plt.plot(x.get_wave(step)[:len(a1)], a1-IR1.get_wave(step)[:len(a1)], label="Error " + labels[k])

plt.xlabel("time (ns)")

plt.tight_layout(pad=1.4, w_pad=0.5, h_pad=1.0)

plt.legend(loc="upper right") # order a legend.
plt.show()