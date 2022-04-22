import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)
import matplotlib.ticker as ticker

p = pd.read_csv('C:/Users/User/Desktop/timewise_firing_prob.csv', header = [0], skiprows = [0])
t = [round(i, 3) for i in np.arange(-1.5, 1.5, 0.01)]
p = p.to_numpy()

fig, ax1 = plt.subplots()
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Spiking probability")
ax1.set_title("22_3_22 rd1 cck-cre ai32 P(spike|t)")
for i in range(len(p)):
    ax1.plot(t, p[i], c = 'black', alpha = 0.1, label = 'Individual Units')
ax1.plot(t, np.mean(p, axis = 0), c = 'black', alpha = 1, label = 'Average')
ax1.margins(x=0, y=0)
ax1.set_ylim(0, 1)

handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc=1)
#plt.show()

ax2 = plt.axes([0,0,1,1])
ip = InsetPosition(ax1, [0.1, 0.6, 0.35, 0.35])
ax2.set_axes_locator(ip)
mark_inset(ax1, ax2, loc1 = 3, loc2 = 1, fc='none', ec='blue', clip_on = True)

for i in range(len(p)):
    ax2.plot(t, p[i], c = 'black', alpha = 0.1, label = 'Individual Units')
ax2.plot(t, np.mean(p, axis = 0), c = 'black', alpha = 1, label = 'Average')
ax2.margins(x=0, y=0)
ax2.set_ylim(0, 0.8)
ax2.set_xlim(0, 0.075)
#ax2.set_xticklabels(ax2.get_xticks(), backgroundcolor='w')
ticks = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*1000))
ax2.xaxis.set_major_formatter(ticks)
ax2.set_xlabel('Time (ms)')
plt.show()