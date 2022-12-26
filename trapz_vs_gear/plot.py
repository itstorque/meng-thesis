import numpy as np
from PyLTSpice import LTSpice_RawRead
import matplotlib.pyplot as plt

freq = 1/np.sqrt(1e-6*1e-3)
a1 = None
k = -1
labels = ["Trapezoidal Method", "Modified Trapezoidal Method", "Gear Method"]
for file in ["trapz.raw", "mod_trapz.raw", "gear.raw"]:
    k+=1
    LT = LTSpice_RawRead.LTSpiceRawRead(file)
    IR1 = LT.get_trace("I(L1)")
    x = LT.get_trace(0)  # Zero is always the X axis
    steps = LT.get_steps()
    for step in range(len(steps)):
        # print(steps[step])
        plt.plot(x.get_wave(step)[:-10], IR1.get_wave(step)[:-10], label=labels[k])
        
        # anal = 100e-6*np.sin(freq*x.get_wave(step)[:-10])
        
        # if a1 is None: a1 = IR1.get_wave(step)[:-10]

        # print(max(IR1.get_wave(step)[:-10]))
# plt.plot(x.get_wave(step)[:-10], , label="Analytic Solution")

        # plt.plot(x.get_wave(step)[:len(a1)], a1-IR1.get_wave(step)[:len(a1)], label="Error " + labels[k])

plt.legend() # order a legend.
plt.show()