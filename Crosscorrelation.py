from Raster import read_spiketrains
import numpy as np
from numpy import correlate
import math
import StimulusTimes
from pylab import *
import seaborn as sns

def create_signal(spiketrain):
    signal = [0 for _ in range(int((max(spiketrain)+1)*1000))]
    for i in spiketrain:
        index = int(i*1000)
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

corr_beforestim = np.zeros(len(unit_list)**2).reshape((len(unit_list), len(unit_list)))
corr_afterstim = np.zeros(len(unit_list)**2).reshape((len(unit_list), len(unit_list)))

for i in range(len(unit_list)-1):
    control1 = control[control['Units'] == unit_list[i]]
    for j in range(i+1,len(unit_list)):
        control2 = control[control['Units'] == unit_list[j]]
        control_2_before = []
        control_1_before = []
        for k in range(len(myLights)):
            spike1 = [i for i in control1['Timestamp'] if myLights[k,1] - 0.15 < i < myLights[k,1]]
            spike2 = [i for i in control2['Timestamp'] if myLights[k,1] - 0.15 < i < myLights[k,1]]
            control_1_before.append(spike1)
            control_2_before.append(spike2)
        control_1_before = [item for sublist in control_1_before for item in sublist]
        control_1_before = [i for i in control_1_before]
        control_2_before = [item for sublist in control_2_before for item in sublist]
        control_2_before = [i for i in control_2_before]
        c = correlate(a=create_signal(control_1_before),v=create_signal(control_2_before),mode='valid')
        c_ = max(c)/(min([len(control_1_before)+len(control_2_before)]))
        print("Correlated pre-stim signals from units {} and {}: \n Correlation of {} at lag = {} ms".\
              format(unit_list[i], unit_list[j], c_, np.argmax(c)))
        corr_beforestim[j, i] = c_

mask = np.zeros_like(corr_beforestim)
mask[np.triu_indices_from(mask)] = True

plt.title('Correlation Before Stim (-150 ms to 0 ms)')
g = sns.heatmap(corr_beforestim, mask=mask, vmax=.3, square=True)
g.set_facecolor('xkcd:white')
plt.show()

for i in range(len(unit_list)-1):
    control1 = control[control['Units'] == unit_list[i]]
    for j in range(i+1,len(unit_list)):
        control2 = control[control['Units'] == unit_list[j]]
        control_2_after = []
        control_1_after = []
        for k in range(len(myLights)):
            spike1 = [i for i in control1['Timestamp'] if myLights[k,1] < i < myLights[k,0]+3]
            spike2 = [i for i in control2['Timestamp'] if myLights[k,1] + 0.02 < i < myLights[k,1]+ 0.06]
            control_1_after.append(spike1)
            control_2_after.append(spike2)
        control_1_after = [item for sublist in control_1_after for item in sublist]
        control_1_after = [i for i in control_1_after]
        control_2_after = [item for sublist in control_2_after for item in sublist]
        control_2_after = [i for i in control_2_after]
        c = correlate(a=create_signal(control_1_after),v=create_signal(control_2_after),mode='valid')
        c_ = max(c)/(min([len(control_1_after)+len(control_2_after)]))
        print("Correlated post-stim signals from units {} and {}: \n Correlation of {} at lag = {} ms".\
              format(unit_list[i], unit_list[j], c_, np.argmax(c)))
        corr_afterstim[j, i] = c_

plt.title('Correlation After Stim ( +20 ms to + 50 ms)')
g = sns.heatmap(corr_afterstim, mask=mask, vmax=.3, square=True)
g.set_facecolor('xkcd:white')
plt.show()

plt.title("Delta Correlation")
g = sns.heatmap(corr_afterstim - corr_beforestim, mask=mask, vmax=.3, square=True)
g.set_facecolor('xkcd:white')
plt.show()

#mask = np.zeros_like(corr_beforestim)
#with sns.axes_style("white"):
#    ax = sns.heatmap(corr_beforestim, mask=mask, vmax=.3, square=True)
#    plt.show()