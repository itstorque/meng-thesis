import numpy as np
from PyLTSpice import LTSpice_RawRead
import matplotlib.pyplot as plt

fig, ax = plt.subplots(nrows=2)

freq = 1/np.sqrt(1e-6*1e-3)
a1 = None
k = -1
labels = ["Without Malicious Circuit", "With Malicious Circuit"]
for file in ["without_M.raw", "with_M.raw"]:
    k+=1
    LT = LTSpice_RawRead.LTSpiceRawRead(file)
    IR1 = LT.get_trace("I(R1)")
    x = LT.get_trace(0)  # Zero is always the X axis
    steps = LT.get_steps()
    for step in range(len(steps)):
        # print(steps[step])
        ax[k].plot(np.abs(x.get_wave(step))*1e9, IR1.get_wave(step)*1e6, ['b', 'g'][k], label=labels[k])
        ax[k].scatter(np.abs(x.get_wave(step))*1e9, IR1.get_wave(step)*1e6, marker='x', color=['black', 'black'][k], label="Computation Steps")
        ax[k].legend()
        
        ax[k].set_ylabel("I(R1) [uA]")
        
        # anal = 100e-6*np.sin(freq*x.get_wave(step)[:-10])
        
        # if a1 is None: a1 = IR1.get_wave(step)[:-10]

        # print(max(IR1.get_wave(step)[:-10]))
# plt.plot(x.get_wave(step)[:-10], , label="Analytic Solution")

        # plt.plot(x.get_wave(step)[:len(a1)], a1-IR1.get_wave(step)[:len(a1)], label="Error " + labels[k])

plt.xlabel("time [ns]")
plt.show()