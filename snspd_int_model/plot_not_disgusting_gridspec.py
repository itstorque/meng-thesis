import numpy as np
from PyLTSpice import LTSpice_RawRead
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import matplotlib.gridspec as gridspec
import matplotlib.transforms as transforms


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

T1, T2 = 4, 1
PPP = 8
delta1, delta2 = 4, 5

gs = gridspec.GridSpec(1,(T2+T1)*PPP+1+delta1+delta2)
fig = plt.figure(figsize=(6,3), dpi=300)

# fig, ax = plt.subplots(figsize=(6,4), nrows=2, sharex=True, dpi=300)

freq = 1/np.sqrt(1e-6*1e-3)
a1 = None
k = -1
labels = ["another_jumbled_both_squares_post"]
for file in ["beautiful_malicious_circuits_correct_range.raw"]:
    k+=1
    LT = LTSpice_RawRead.LTSpiceRawRead(file)
    IR1 = LT.get_trace("V(source)")
    IR2 = LT.get_trace("V(N3)")
    x = LT.get_trace(0)  # Zero is always the X axis
    steps = LT.get_steps()
        
    ax0 = fig.add_subplot(gs[k, 0:T1*PPP])
    ax2 = fig.add_subplot(gs[k, -1])
    ax1 = fig.add_subplot(gs[k, T1*PPP+delta1:(T1+T2)*PPP+delta1])
    
    for step in range(len(steps)):
        # print(steps[step])
        
        LW = 1
        ax0.plot(np.abs(x.get_wave(step))*1e9-69.9, IR1.get_wave(step)*1e3, c=cm.inferno(0.8*step/len(steps)), linewidth=LW)
        ax1.plot(np.abs(x.get_wave(step))*1e9-69.9, IR2.get_wave(step), c=cm.inferno(0.8*step/len(steps)), linewidth=LW)
        
        
        
        # plt.scatter(np.abs(x.get_wave(step))*1e9, IR1.get_wave(step)*1e6, marker='x', color=['black', 'black'][k], label="Computation Steps")
        # plt.legend()
        
        # ax[0].set_yscale("logit")
        # ax[1].set_yscale("symlog")
        
        # plt.xlim((0, 50))
        ax0.set_xlim((0, 5))
        ax1.set_xlim((0.09, 0.35))
        
        ax0.set_xlabel("time [ns]")
        ax1.set_xlabel("time [ns]")
        
        ax0.set_ylabel("Voltage [mV]")
        ax1.set_ylabel("Hotspot Resistance [$\Omega$]")
        
        ax0.tick_params(axis="y",direction="in")
        ax1.tick_params(axis="y",direction="in")
        
        T = ax1.get_yticks()
        
        # k=0
        # for i in range(len(T)):
        #     k+=1
        #     T[i] = T[i] if k%2 else ""
        
        
        # ax2.set_yticklabels(ax2.get_yticks(), rotation = 45)
        
        if step==0:
            
                plt.ylabel("I(R1) [$\mu$A]")
                
                # cax = fig.add_axes([0.85, 0.21, 0.02, 0.55])
                
                fig.colorbar(cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=11, vmax=12), cmap=truncate_colormap(cm.inferno, 0, 0.8)), cax=ax2, orientation='vertical', label="Bias Current [$\mu$A]")
        
                # plt.ylabel("Bias Current [$\mu$A]")
                
                ax2.yaxis.set_ticks_position('left')
        
                # ax[1].plot(np.abs(x.get_wave(step))*1e9, LT.get_trace("V(NC_01)").get_wave(step)*1e6, label="Malicious V1 Pulse")
                # ax[1].plot(np.abs(x.get_wave(step))*1e9, LT.get_trace("V(NC_02)").get_wave(step)*1e6, label="Malicious V2 Pulse")
                
                # ax[1].legend()
                
                # ax[1].set_ylabel("Voltage [V]")
        
        # anal = 100e-6*np.sin(freq*x.get_wave(step)[:-10])
        
        # if a1 is None: a1 = IR1.get_wave(step)[:-10]

        # print(max(IR1.get_wave(step)[:-10]))
# plt.plot(x.get_wave(step)[:-10], , label="Analytic Solution")

        # plt.plot(x.get_wave(step)[:len(a1)], a1-IR1.get_wave(step)[:len(a1)], label="Error " + labels[k])

plt.tight_layout(pad=20)

T = T[1::2]
# T = [0.0]+list(T)

ax1.set_yticks(T)
ax1.set_ylim((-50, 1500))
ax1.set_yticklabels(T, rotation='vertical')#, rotation = 90)

offset = lambda y: transforms.ScaledTranslation(2/72, y/72, fig.dpi_scale_trans)
k=0
# apply offset transform to all x ticklabels.
for label in ax1.yaxis.get_majorticklabels():
    k+=1
    print(label)
    label.set_transform(label.get_transform() + offset([0, 5, 12, 12, 17, 17, 15][k]))

plt.show()