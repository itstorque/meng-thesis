import numpy as np
from PyLTSpice import LTSpice_RawRead
import matplotlib.pyplot as plt

# plt.figure(figsize=(17/2,3/2))

fig, ax = plt.subplots(figsize=(6, 4), nrows=2, ncols=1, sharex=True, sharey=True, dpi=300)

freq = 1/np.sqrt(1e-6*1e-3)
a1 = None
k = -1
labels = ["Photon Incedent at $L/4$", "Photon Incedent at $L/2$",]
for file in ["50outof200.raw", "101outof201.raw"]:
    k+=1
    LT = LTSpice_RawRead.LTSpiceRawRead(file)
    IR1 = LT.get_trace("I(R1)")
    IR2 = LT.get_trace("I(R3)")
    x = LT.get_trace(0)  # Zero is always the X axis
    steps = LT.get_steps()
    print(steps)
    for step in range(len(steps)):
        # print(steps[step])
        
        # ax[k%2, int(k/2)].set_title(labels[k])
        ax[k%2].plot(abs(x.get_wave(step))*1e6, IR1.get_wave(step)*1e6, label="Current in R3", color="royalblue")
        ax[k%2].plot(abs(x.get_wave(step))*1e6, IR2.get_wave(step)*1e6, label="Current in R2", color="green")
        # ax[k%2].scatter(abs(x.get_wave(step))*1e9, IR2.get_wave(step)*1e6)#, marker='x', color='darkorange', s=20)
        
        ax[k%2].set_ylabel("Readout Current ($\mu$A)")
        
        ax[k%2].set_xlabel("time ($\mu$s)")
        
        ax[k%2].set_xlim((0, 33))
        
        ax[k%2].set_title(labels[k])
        
        ax[k%2].legend()
        
        # anal = 100e-6*np.sin(freq*x.get_wave(step)[:-10])
        
        # if a1 is None: a1 = IR1.get_wave(step)[:-10]

        # print(max(IR1.get_wave(step)[:-10]))
# plt.plot(x.get_wave(step)[:-10], , label="Analytic Solution")

        # plt.plot(x.get_wave(step)[:len(a1)], a1-IR1.get_wave(step)[:len(a1)], label="Error " + labels[k])

# for ax1, col in zip(ax, ["Old Nanowire Model", "New Nanowire Model"]):
#     ax1.set_title(col)

# for ax1, row in zip(ax[:,0], ["reltol $10^{-3}$", "reltol $10^{-6}$"]):
#     ax1.annotate(row, xy=(0, 0.5), xytext=(-ax1.yaxis.labelpad - 5, 0),
#         xycoords=ax1.yaxis.label, textcoords='offset points',
#         size='large', ha='right', va='center')

# plt.tight_layout(pad=1.4, w_pad=0.5, h_pad=1.0)

plt.legend() # order a legend.
plt.show()