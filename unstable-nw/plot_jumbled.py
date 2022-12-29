import numpy as np
from PyLTSpice import LTSpice_RawRead
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

fig, ax = plt.subplots(nrows=2)
plt.xlabel("time [ns]")

freq = 1/np.sqrt(1e-6*1e-3)
a1 = None
k = -1
labels = ["another_jumbled_both_squares_post"]
for file in ["another_jumbled_both_squares_post.raw"]:
    k+=1
    LT = LTSpice_RawRead.LTSpiceRawRead(file)
    IR1 = LT.get_trace("I(R1)")
    x = LT.get_trace(0)  # Zero is always the X axis
    steps = LT.get_steps()
    for step in range(len(steps)):
        # print(steps[step])
        ax[0].plot(np.abs(x.get_wave(step))*1e9, IR1.get_wave(step)*1e6, c=cm.inferno(0.8*step/len(steps)))
        # plt.scatter(np.abs(x.get_wave(step))*1e9, IR1.get_wave(step)*1e6, marker='x', color=['black', 'black'][k], label="Computation Steps")
        # plt.legend()
        
        ax[0].set_ylabel("I(R1) [$\mu$A]")
        
        if step==0:
                
                cax = fig.add_axes([0.85, 0.57, 0.02, 0.25])
                
                fig.colorbar(cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=11, vmax=12), cmap=truncate_colormap(cm.inferno, 0, 0.8)), cax=cax, orientation='vertical')
        
                plt.ylabel("Bias Current [$\mu$A]")
                
                cax.yaxis.set_ticks_position('left')
        
                ax[1].plot(np.abs(x.get_wave(step))*1e9, LT.get_trace("V(NC_01)").get_wave(step)*1e6, label="Malicious V1 Pulse")
                ax[1].plot(np.abs(x.get_wave(step))*1e9, LT.get_trace("V(NC_02)").get_wave(step)*1e6, label="Malicious V2 Pulse")
                
                ax[1].legend()
                
                ax[1].set_ylabel("Voltage [V]")
        
        # anal = 100e-6*np.sin(freq*x.get_wave(step)[:-10])
        
        # if a1 is None: a1 = IR1.get_wave(step)[:-10]

        # print(max(IR1.get_wave(step)[:-10]))
# plt.plot(x.get_wave(step)[:-10], , label="Analytic Solution")

        # plt.plot(x.get_wave(step)[:len(a1)], a1-IR1.get_wave(step)[:len(a1)], label="Error " + labels[k])

plt.show()