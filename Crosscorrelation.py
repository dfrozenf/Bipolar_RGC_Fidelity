from Raster import read_spiketrains
import numpy as np
from numpy import correlate
import math
import StimulusTimes
from pylab import *
import seaborn as sns

def create_signal(spiketrain, bins):
    signal = [0 for _ in range(int((max(spiketrain)+1)*bins))]
    for i in spiketrain:
        index = int(i*bins)
        signal[index] = 1
    return signal

print('Upload trigger file: ')
myLights = StimulusTimes.main()
myLights = np.array(myLights).reshape((len(myLights),4))
print('Upload sorted spikes: ')
mySpikes = read_spiketrains()

wash_ID = ['Control', 'MFA', 'DNQX']
wash_times = [2109.9, 14664.8 - 2117.6]
wash_times.insert(0, 0)
wash_times.insert(len(wash_times) + 1, max(mySpikes['Timestamp']))

min_tau = -1.5
max_tau = 1.5
xx = np.linspace(min_tau, max_tau, 1000)

unit_list = [35.3, 46.1, 46.2, 46.3, 47.1, 47.2, 55.2, 56.3, 57.1, 57.2, 65.1,
             66.1, 66.2, 67.1, 67.2, 67.3, 74.1, 74.2, 75.1, 76.1, 83.1, 83.2,
             83.3, 84.2]

control = mySpikes[mySpikes['Timestamp'] < wash_times[1]]
mfa = mySpikes[mySpikes['Timestamp'] > wash_times[1]]
mfa = mfa[mfa['Timestamp'] < wash_times[2]]

def npcorr(unit_list, spiketrain, lights, tau1, tau2, title, nbins):
    counter = 0
    corr_ = np.zeros(len(unit_list)**2).reshape((len(unit_list), len(unit_list)))
    n_computations = (len(unit_list)**2/2)
    for i in range(len(unit_list)-1):
        spike1 = spiketrain[spiketrain['Units'] == unit_list[i]]
        for j in range(i+1,len(unit_list)):
            spike2 = spiketrain[spiketrain['Units'] == unit_list[j]]
            spike_2_before = []
            spike_1_before = []
            for k in range(len(myLights)):
                spike1_ = [i for i in spike1['Timestamp'] if lights[k,1] + tau1 < i < lights[k,1]+ tau2]
                spike2_ = [i for i in spike2['Timestamp'] if lights[k,1] + tau1 < i < lights[k,1] + tau2]
                spike_1_before.append(spike1_)
                spike_2_before.append(spike2_)
            spike_1_before = [item for sublist in spike_1_before for item in sublist]
            spike_1_before = [i for i in spike_1_before]
            spike_2_before = [item for sublist in spike_2_before for item in sublist]
            spike_2_before = [i for i in spike_2_before]
            counter += 1
            c = correlate(a=create_signal(spike_1_before, nbins),v=create_signal(spike_2_before, nbins),mode='valid')
            c_ = max(c)/(min([len(spike_1_before), len(spike_2_before)]))
            print("Correlated pre-stim signals from units {} and {} ({}/{})".
                  format(unit_list[i], unit_list[j], counter, int(n_computations)))
            corr_[j, i] = c_

    mask = np.zeros_like(corr_)
    mask[np.triu_indices_from(mask)] = True

    plt.title(title)
    g = sns.heatmap(corr_, mask=mask, vmax=.3, square=True)
    g.set_facecolor('xkcd:white')
    plt.show()
    return corr_



