import numpy as np
from PyLTSpice import LTSpice_RawRead
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# plt.figure(figsize=(17/2,3/2))

H = 4

# fig, ax = plt.subplots(nrows=2, ncols=4, sharex=True)
gs = gridspec.GridSpec(2*H, 2)
fig = plt.figure(figsize=(7,4), dpi=300)

# ax[0,0].sharey(ax[0,1])
# ax[1,0].sharey(ax[1,1])

A = []

freq = 1/np.sqrt(1e-6*1e-3)
a1 = None
k = -1
labels = ["old 6", "new 6",]
for file in ["old_reltol6.raw", "new_reltol6.raw"]:
    k+=1
    LT = LTSpice_RawRead.LTSpiceRawRead(file)
    IR1 = LT.get_trace("I(R4)")
    x = LT.get_trace(0)  # Zero is always the X axis
    steps = LT.get_steps()
    for step in range(len(steps)):
        # print(steps[step])
        
        if k==0:
            ax0 = fig.add_subplot(gs[0:H, k])
        else:
            ax0 = fig.add_subplot(gs[0:H, k], sharex = ax0)
            
        A.append(ax0)
            
        ax0.tick_params(labelbottom=False)
        
        ax0.set_xlim((-0.5, 34.5))
        
        # ax[k%2, int(k/2)].set_title(labels[k])
        ax0.plot(abs(x.get_wave(step))*1e9, IR1.get_wave(step)*1e6, label=labels[k], color=["royalblue", "green"][k%2])
        # ax[0, k%2].scatter(abs(x.get_wave(step))*1e9, IR1.get_wave(step)*1e6, marker='x', color='darkorange', s=20)
        fig.subplots_adjust(wspace=0)

        
        get_trace = lambda x: LT.get_trace(x).get_wave(step)
        
        val = get_trace("I(R1)")
        
        ax1 = fig.add_subplot(gs[H:2*H-1, k], sharex = ax0)
        ax2 = fig.add_subplot(gs[2*H-1, k], sharex = ax0)
        
        # (n1-src)/I(r1)
        val = np.where(val!=0, abs(abs(get_trace("V(n1)") - get_trace("V(source)")) / val), 0)
        
        ax1.plot(abs(x.get_wave(step))*1e9, val*1e6, label=labels[k], color=["royalblue", "green"][k%2], linewidth=1)
        ax2.plot(abs(x.get_wave(step))*1e9, val*1e6, label=labels[k], color=["royalblue", "green"][k%2], linewidth=1)
        
        if k==0: ax0.set_ylabel("Current ($\mu$A)")
        
        # ax0.set_xlabel("time (ns)")
        ax2.set_xlabel("time (ns)")
        
        ax1.set_yscale("symlog")
        ax2.set_yscale("symlog")
        
        ax2.set_ylim(-0.1,1) # most of the data
        ax1.set_ylim(3e11,1.5e14) # outliers only
        ax1.xaxis.tick_top()
        ax1.tick_params(labeltop=False)  # don't put tick labels at the top
        ax2.xaxis.tick_bottom()
        
        ax1.spines['bottom'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        
        # Get the current y-tick locations and labels
        yticks = ax1.get_yticks()
        yticklabels = ax1.get_yticklabels()

        # Keep only every 2nd tick and label
        yticks = yticks[1::]
        yticklabels = yticklabels[1::]

        # Set the new tick locations and labels
        ax1.set_yticks(yticks)
        ax1.set_yticklabels(yticklabels)
        
        if k!=0:
            ax1.tick_params(labelleft=False)
            ax2.tick_params(labelleft=False)
            ax0.tick_params(labelleft=False)
        
        if k==0: 
            ax1.set_ylabel("Hotspot Resistance ($\Omega$)")
            ax1.yaxis.set_label_coords(-0.2, 0.3)
            # ax0.yaxis.set_label_coords(-0.2, 0.48)
        
        d = .015  # how big to make the diagonal lines in axes coordinates
        # arguments to pass to plot, just so we don't keep repeating them
        kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
        ax1.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
        ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

        kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
        ax2.plot((-d, +d), (1 - d, 1 + 6*d), **kwargs)  # bottom-left diagonal
        ax2.plot((1 - d, 1 + d), (1 - d, 1 + 6*d), **kwargs)  # bottom-right diagonal
        
        # ax[k%2, int(k/2)].legend()
        
        # anal = 100e-6*np.sin(freq*x.get_wave(step)[:-10])
        
        # if a1 is None: a1 = IR1.get_wave(step)[:-10]

        # print(max(IR1.get_wave(step)[:-10]))
# plt.plot(x.get_wave(step)[:-10], , label="Analytic Solution")

        # plt.plot(x.get_wave(step)[:len(a1)], a1-IR1.get_wave(step)[:len(a1)], label="Error " + labels[k])

for ax1, col in zip(A, ["Old Nanowire Model", "New Nanowire Model"]):
    ax1.set_title(col)

# for ax1, row in zip(ax[:,0], ["reltol $10^{-3}$", "reltol $10^{-6}$"]):
#     ax1.annotate(row, xy=(0, 0.5), xytext=(-ax1.yaxis.labelpad - 5, 0),
#         xycoords=ax1.yaxis.label, textcoords='offset points',
#         size='large', ha='right', va='center')

# plt.tight_layout()

# plt.legend(loc="upper right") # order a legend.
plt.show()