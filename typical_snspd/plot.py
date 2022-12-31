import numpy as np
from PyLTSpice import LTSpice_RawRead
import matplotlib.pyplot as plt

# plt.figure(figsize=(6,3))
fig, axs = plt.subplots(figsize=(6,3), nrows=2, sharex=True, dpi=300)

freq = 1/np.sqrt(1e-6*1e-3)
a1 = None
k = -1
labels = ["Photon Event Driven", "Relaxation Oscillations"]#["Output of Behavioural Source B1"]
for file in ["out.raw", "relax_osc.raw"]:
    k+=1
    LT = LTSpice_RawRead.LTSpiceRawRead(file)
    IR1 = LT.get_trace("I(R1)")
    x = LT.get_trace(0)  # Zero is always the X axis
    steps = LT.get_steps()
    for step in range(len(steps)):
        # print(steps[step])
        axs[k].plot(abs(x.get_wave(step))*1e9, IR1.get_wave(step)*1e6)
        # plt.scatter(abs(x.get_wave(step))*1e9, IR1.get_wave(step)*1e6, marker='x', color='black')
        
        axs[k].set_ylabel("Current ($\mu$A)")
        
        axs[k].set_title(labels[k])
        
        # anal = 100e-6*np.sin(freq*x.get_wave(step)[:-10])
        
        # if a1 is None: a1 = IR1.get_wave(step)[:-10]

        # print(max(IR1.get_wave(step)[:-10]))
# plt.plot(x.get_wave(step)[:-10], , label="Analytic Solution")

        # plt.plot(x.get_wave(step)[:len(a1)], a1-IR1.get_wave(step)[:len(a1)], label="Error " + labels[k])

plt.xlabel("time (ns)")

plt.tight_layout(pad=1.4, w_pad=0.5, h_pad=0.3)

# plt.legend(loc="upper right") # order a legend.
plt.show()