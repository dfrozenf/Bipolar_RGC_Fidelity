from Raster import read_spiketrains
import numpy as np
import math
import StimulusTimes
import matplotlib.pyplot as plt

print('Upload trigger file: ')
myLights = StimulusTimes.main()
myLights = np.array(myLights).reshape((len(myLights),4))
print('Upload sorted spikes: ')
mySpikes = read_spiketrains()

wash_ID = ['Control', 'MFA', 'DNQX']
wash_times = [2109.9, 14664.8 - 2117.6]
wash_times.insert(0, 0)
wash_times.insert(len(wash_times) + 1, max(mySpikes['Timestamp']))

unit_list = [35.3, 46.1, 46.2, 46.3, 47.1, 47.2, 55.2, 56.3, 57.1, 57.2, 65.1,
             66.1, 66.2, 67.1, 67.2, 67.3, 74.1, 74.2, 75.1, 76.1, 83.1, 83.2,
             83.3, 84.2]

control = mySpikes[mySpikes['Timestamp'] < wash_times[1]]
mfa = mySpikes[mySpikes['Timestamp'] > wash_times[1]]
mfa = mfa[mfa['Timestamp'] < wash_times[2]]

##Fig 1##
bin_width = 0.01
min_tau = 0
max_tau = 0.5
xx = [i for i in np.arange(min_tau, max_tau, bin_width)]
for i in unit_list:
    p = [0 for _ in xx]
    control_ = control[control['Units'] == i]
    spikes = []
    for j in range(len(myLights)):
        spiketrain = [i-myLights[j,0] for i in control_['Timestamp'] if myLights[j, 0] < i < myLights[j, 0] + 3.1]
        spiketrain = [i for i in spiketrain if min_tau <= i <= max_tau]
        for k in spiketrain:
            spikes.append(k)

    plt.hist(x=spikes, bins=np.arange(min_tau, max_tau, bin_width), alpha=0.5)
plt.show()
