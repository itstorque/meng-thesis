import numpy as np
from PyLTSpice import LTSpice_RawRead
import matplotlib.pyplot as plt

# plt.figure(figsize=(17/2,3/2))

fig, ax = plt.subplots(nrows=2, ncols=2)

freq = 1/np.sqrt(1e-6*1e-3)
a1 = None
k = -1
labels = ["old 3", "new 3", "old 6", "new 6"]
for file in ["old_reltol3.raw", "new_reltol3.raw", "old_reltol6.raw", "new_reltol6.raw"]:
    k+=1
    LT = LTSpice_RawRead.LTSpiceRawRead(file)
    IR1 = LT.get_trace("I(R4)")
    x = LT.get_trace(0)  # Zero is always the X axis
    steps = LT.get_steps()
    for step in range(len(steps)):
        # print(steps[step])
        
        # ax[k%2, int(k/2)].set_title(labels[k])
        ax[int(k/2), k%2].plot(abs(x.get_wave(step))*1e9, IR1.get_wave(step)*1e6, label=labels[k], color=["blue", "green"][k%2])
        ax[int(k/2), k%2].scatter(abs(x.get_wave(step))*1e9, IR1.get_wave(step)*1e6, marker='x', color='black')
        
        ax[int(k/2), k%2].set_ylabel("Current ($\mu$A)")
        
        ax[int(k/2), k%2].set_xlabel("time (ns)")
        
        # ax[k%2, int(k/2)].legend()
        
        # anal = 100e-6*np.sin(freq*x.get_wave(step)[:-10])
        
        # if a1 is None: a1 = IR1.get_wave(step)[:-10]

        # print(max(IR1.get_wave(step)[:-10]))
# plt.plot(x.get_wave(step)[:-10], , label="Analytic Solution")

        # plt.plot(x.get_wave(step)[:len(a1)], a1-IR1.get_wave(step)[:len(a1)], label="Error " + labels[k])

for ax1, col in zip(ax[0], ["Old Nanowire Model", "New Nanowire Model"]):
    ax1.set_title(col)

for ax1, row in zip(ax[:,0], ["reltol $10^{-3}$", "reltol $10^{-6}$"]):
    ax1.annotate(row, xy=(0, 0.5), xytext=(-ax1.yaxis.labelpad - 5, 0),
        xycoords=ax1.yaxis.label, textcoords='offset points',
        size='large', ha='right', va='center')

plt.tight_layout(pad=1.4, w_pad=0.5, h_pad=1.0)

# plt.legend(loc="upper right") # order a legend.
plt.show()