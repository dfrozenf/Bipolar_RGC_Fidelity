import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

p = pd.read_csv('E:/Fidelity/22_3_22_rd1_cck_cre_ai32/Figs/timewise_firing_prob.csv', header = [0], skiprows = [0])
t = [round(float(i), 3)*1000 for i in p.columns]
p = p.to_numpy()

plt.xlabel("Time (ms)")
plt.ylabel("Spiking probability")
plt.title("All Units")
for i in range(len(p)):
    plt.plot(t[150:175], p[i][150:175], c = 'black', alpha = 0.1)
plt.show()

plt.xlabel("Time (ms)")
plt.ylabel("Spiking probability")
plt.title("Average")
plt.plot(t[150:175], np.mean(p, axis = 0)[150:175])
plt.show()
