from Raster import read_spiketrains
import StimulusTimes
from pylab import *
import matplotlib.ticker as mtick


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

light0 = [i for i in myLights if wash_times[0] < i[0] < wash_times[1]]
light0 = np.array(light0).reshape((len(light0), 4))
light1 = [i for i in myLights if wash_times[1] < i[0] < wash_times[2]]
light1 = np.array(light1).reshape((len(light1), 4))
light2 = [i for i in myLights if wash_times[2] < i[0] < wash_times[3]]
light2 = np.array(light2).reshape((len(light2), 4))

avg_light0 = light0[:,3].mean()
avg_light1 = light1[:,3].mean()
avg_light2 = light2[:,3].mean()

flight0 = [0 for _ in xx]
for i in range(len(xx)):
    if 0 < xx[i] < avg_light0:
        flight0[i] = 1

flight1 = [0 for _ in xx]
for i in range(len(xx)):
    if 0 < xx[i] < avg_light1:
        flight1[i] = 1

flight2 = [0 for _ in xx]
for i in range(len(xx)):
    if 0 < xx[i] < avg_light2:
        flight2[i] = 1

unit_list = list(sort(list(set(mySpikes['Units']))))

control = mySpikes[mySpikes['Timestamp'] < wash_times[1]]
mfa = mySpikes[mySpikes['Timestamp'] > wash_times[1]]
mfa = mfa[mfa['Timestamp'] < wash_times[2]]
dnqx = mySpikes[mySpikes['Timestamp'] > wash_times[2]]

for i in unit_list:
    control_ = control[control['Units'] == i]
    mfa_ = mfa[mfa['Units'] == i]
    dnqx_ = dnqx[dnqx['Units'] == i]

    fig, ax = plt.subplots(3, 3, sharex='all', sharey = 'row', gridspec_kw={'height_ratios': [1, 10, 10]})
    fig.suptitle('Unit {}'.format(i))
    ax[0, 0].set_xlim(min_tau, max_tau)
    ax[0, 0].plot(xx, flight0)
    ax[0, 0].axis('off')
    ax[0, 1].plot(xx, flight1)
    ax[0, 1].axis('off')
    ax[0, 2].plot(xx, flight2)
    ax[0, 2].axis('off')
    ax[1, 0].tick_params(axis='x', which='both', bottom=False, top=False)
    ax[1, 1].tick_params(axis='x', which='both', bottom=False, top=False)
    ax[1, 1].tick_params(axis='y', which='both', bottom=False, top=False)
    ax[1, 2].tick_params(axis='x', which='both', bottom=False, top=False)
    ax[1, 2].tick_params(axis='y', which='both', bottom=False, top=False)
    ax[0, 0].set_title(wash_ID[0])
    ax[0, 1].set_title(wash_ID[1])
    ax[0, 2].set_title(wash_ID[2])
    ax[1, 0].set_ylabel('Trial')
    ax[2, 0].set_ylabel('Instantaneous Frequency \n (Hz)')
    ax[1, 0].set_ylim(0, 100)
    ax[2, 0].set_yscale('log')
    ax[2, 1].set_xlabel('Time (s)')

    control_h = []
    mfa_h = []
    dnqx_h = []
    control_f = {}
    mfa_f = {}
    dnqx_f = {}


    for j in range(len(myLights)):
        xxx = np.linspace(min_tau, max_tau, 1000)
        yy = []

        light_on = myLights[j,1]
        light_off = myLights[j,2]
        if myLights[j,1] < wash_times[1]:
            wash = 'Control'
        elif wash_times[1] < myLights[j,1] < wash_times[2]:
            wash = 'MFA'
        elif myLights[j,1] > wash_times[2]:
            wash = 'DNQX'

        if wash == 'Control':
            spiketrain = [light_off-i for i in control_['Timestamp'] if (myLights[j,0] < i < myLights[j,0]+3) ]
            for k in spiketrain:
                control_h.append(k)
                ax[1,0].scatter(x=k, y=j, marker="o", color = 'black', s = 0.1)
            for t in xxx:
                spike1 = list(sorted([i for i in spiketrain if i < t]))
                spike2 = list(sorted([i for i in spiketrain if i >= t]))
                if spike1 and spike2:
                    ISI = spike2[0] - spike1[-1]
                    yy.append(1 / ISI)
                    #ax[2, 2].plot(t, 1 / ISI)
                else:
                    yy.append(NaN)
            xxx = np.array(xx)
            yy = np.array(yy)
            mask = np.isfinite(yy.astype(np.double))
            xxx = xxx[mask]
            yy = yy[mask]
            ax[2,0].plot(xxx, yy, alpha = 0.1, color='black')
        elif wash == 'MFA':
            spiketrain = [light_off-i for i in mfa_['Timestamp'] if (myLights[j,0] < i < myLights[j,0]+3)]
            for k in spiketrain:
                mfa_h.append(k)
                ax[1, 1].scatter(x=k, y=j-100, marker="o", color = 'black', s = 0.1)
            for t in xxx:
                spike1 = list(sorted([i for i in spiketrain if i < t]))
                spike2 = list(sorted([i for i in spiketrain if i >= t]))
                if spike1 and spike2:
                    ISI = spike2[0] - spike1[-1]
                    yy.append(1 / ISI)
                    #ax[2, 2].plot(t, 1 / ISI)
                else:
                    yy.append(NaN)
            xxx = np.array(xx)
            yy = np.array(yy)
            mask = np.isfinite(yy.astype(np.double))
            xxx = xxx[mask]
            yy = yy[mask]
            ax[2, 1].plot(xxx, yy, alpha = 0.1, color = 'black')

        elif wash == 'DNQX':
            spiketrain = [light_off-i for i in dnqx_['Timestamp'] if (myLights[j,0] < i < myLights[j,0]+3)]
            for k in spiketrain:
                dnqx_h.append(k)
                ax[1,2].scatter(x=k, y=j-200, marker="o", color = 'black', s = 0.1)
            for t in xxx:
                spike1 = list(sorted([i for i in spiketrain if i < t]))
                spike2 = list(sorted([i for i in spiketrain if i >= t]))
                if spike1 and spike2:
                    ISI = spike2[0]-spike1[-1]
                    yy.append(1/ISI)
                    #ax[2, 2].plot(t, 1/ISI)
                else:
                    yy.append(NaN)
            xxx = np.array(xx)
            yy = np.array(yy)
            mask = np.isfinite(yy.astype(np.double))
            xxx = xx[mask]
            yy = yy[mask]
            ax[2, 2].plot(xxx, yy, alpha = 0.1, color = 'black')
    #for t in control_f.keys():
    #    ax[2,0].scatter(t, sum(control_f[t])/len(control_f), color = 'black', s = 0.1)

    #for t in mfa_f.keys():
    #    ax[2, 1].scatter(t, sum(mfa_f[t]) / len(mfa_f), color='black', s=0.1)

    #for t in dnqx_f.keys():
        #ax[2, 2].scatter(t, sum(dnqx_f[t]) / len(dnqx_f), color='black', s=0.1)

    plt.savefig('E:/Fidelity/22_3_22_rd1_cck_cre_ai32/Figs/aligned_Unit_{}'.format(i).replace('.','_')+'.png')
    plt.show()
    plt.close(fig)