import numpy as np
from PyLTSpice import LTSpice_RawRead
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize= (6, 4), nrows=3, ncols=1, dpi=300, sharex=True, sharey=True)

freq = 1/np.sqrt(1e-6*1e-3)
a1 = None
k = -1
labels = ["Trapezoidal Method", "Modified Trapezoidal Method", "Gear Method"]
for file in ["trapz_s.raw", "mtrapz_s.raw", "gear_s.raw"]:
    k+=1
    LT = LTSpice_RawRead.LTSpiceRawRead(file)
    IR1 = LT.get_trace("I(L1)")
    x = LT.get_trace(0)  # Zero is always the X axis
    steps = LT.get_steps()
    for step in range(len(steps)):
        # print(steps[step])
        V=IR1.get_wave(step)
        
        ax[k].plot(abs(x.get_wave(step))*1e9, V*1e6, label=labels[k])
        
        ax[k].set_title(labels[k])
        
        ax[1].set_ylabel("Voltage across Tank [$\mu$V]")
        
        ax[k].hlines([min(V*1e6), max(V*1e6)], min(abs(x.get_wave(step)))*1e9, max(abs(x.get_wave(step)))*1e9, color="red")
        
        # anal = 100e-6*np.sin(freq*x.get_wave(step)[:-10])
        
        # if a1 is None: a1 = IR1.get_wave(step)[:-10]

        # print(max(IR1.get_wave(step)[:-10]))
# plt.plot(x.get_wave(step)[:-10], , label="Analytic Solution")

        # plt.plot(x.get_wave(step)[:len(a1)], a1-IR1.get_wave(step)[:len(a1)], label="Error " + labels[k])

ax[2].set_xlabel("time [ns]")

# plt.legend() # order a legend.
plt.tight_layout()
plt.show()