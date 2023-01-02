import numpy as np
from PyLTSpice import LTSpice_RawRead
import matplotlib.pyplot as plt

# plt.figure(figsize=(17/2,3/2))

# S12, S22 = [np.load("rc_fixed_ans_12.npy"), np.load("taper_fixed_ans_12.npy"),], [np.load("rc_fixed_ans_22.npy"), np.load("taper_fixed_ans_22.npy")]
# freq = [np.load("rc_fixed_ans_f.npy"), np.load("taper_fixed_ans_f.npy")]

fig, ax = plt.subplots(figsize= (6, 2), nrows=1, ncols=2, dpi=300)

# freq = 1/np.sqrt(1e-6*1e-3)
a1 = None
k = -1
labels = ["old 3"]
for file in ["timedomainLC_1e-3.raw", "timedomainLC_1e-6.raw"]: # driven by 5.88e9
    k+=1
    LT = LTSpice_RawRead.LTSpiceRawRead(file)
    IR1 = LT.get_trace("I(R1)")
    IR2 = LT.get_trace("I(R2)")
    x = LT.get_trace(0)  # Zero is always the X axis
    steps = LT.get_steps()
    for step in range(len(steps)):
        # print(steps[step])
        
        # ax[k%2, int(k/2)].set_title(labels[k])
        # ax[k%2].plot(abs(x.get_wave(step))*1e9, IR1.get_wave(step)*1e6, label=labels[k], color=["royalblue", "green"][k%2])
        # ax[k%2].scatter(abs(x.get_wave(step))*1e9, IR1.get_wave(step)*1e6, marker='x', color='darkorange', s=20)
        # delta = lambda x: np.max(x) - np.min(x)
        
        V = IR1.get_wave(step)
        #REF = -20*np.log10(abs(S22))
        V2 = IR2.get_wave(step)
        
        P = np.angle(IR1.get_wave(step))
        
        F = 1#delta(20*np.log10(V)) / delta(REF)
        print("F", F)
        S = 0#(V[0]) - (REF[0]/F)
        
        ax[k].plot(abs(x.get_wave(step))*1e9, V*1e6, label="spiced model", color="#8C001A", alpha=0.8)
        ax[k].plot(abs(x.get_wave(step))*1e9, V2*1e6, label="Actual circuit", color="#FF9000", alpha=0.8)
        # ax[k].plot(freq[k]/1e9, 20*np.log10(S22[k]), '--', label="source $S_{22}$", color="#FF9000", linewidth="1.5", dashes=(1, 3))
        # ax[k].plot(abs(x.get_wave(step))/1e12, P*np.pi, color="red")
        # ax[k, 1].plot(abs(x.get_wave(step))/1e9, V2, label="Measured from Model", color="royalblue", linewidth="2")
        # ax[k, 1].plot(freq[k]/1e9, 20*np.log10(S12[k]), '--', label="Analytic", color="black", linewidth="1")
        
        # ax[0].plot(freq/1e12, -20*np.log10(S22), label="Analytical Exponential Taper S-parameters", color="green")
        # ax[1].plot(freq/1e12, -20*np.log10(S12), label="Analytical Exponential Taper S-parameters", color="green")
        
        # ax[0].plot(freq/1e12, (REF/F)+S, label="Analytical Exponential Taper S-parameters", color="red")
        # # ax[1].plot(freq/1e12, S12, label="Analytical Exponential Taper S-parameters", color="red")
        
        ax[k].set_ylabel("$R_{\mathrm{out}}$ Current ($\mu$A)")
        ax[k].set_xlabel("Time (ns)")
        # ax[k, 1].set_ylabel("Power (dB)")
        # ax[k, 1].set_xlabel("Frequency (GHz)")
        
        # ax[k%2, int(k/2)].legend()
        
        # anal = 100e-6*np.sin(freq*x.get_wave(step)[:-10])
        
        # if a1 is None: a1 = IR1.get_wave(step)[:-10]

        # print(max(IR1.get_wave(step)[:-10]))
# plt.plot(x.get_wave(step)[:-10], , label="Analytic Solution")

        # plt.plot(x.get_wave(step)[:len(a1)], a1-IR1.get_wave(step)[:len(a1)], label="Error " + labels[k])

# ax[0].set_xlim((0, 5))
    

for ax1, col in zip(ax, [("reltol$=10^{-3}$", "lower right"), 
                         ("reltol$=10^{-6}$", "lower right")]):
    col, loc = col
    ax1.set_title(col)
    ax1.legend(loc=loc)

# for ax1, row in zip(ax[:,0], ["reltol $10^{-3}$", "reltol $10^{-6}$"]):
#     ax1.annotate(row, xy=(0, 0.5), xytext=(-ax1.yaxis.labelpad - 5, 0),
#         xycoords=ax1.yaxis.label, textcoords='offset points',
#         size='large', ha='right', va='center')

plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.5)

 # order a legend.
plt.show()