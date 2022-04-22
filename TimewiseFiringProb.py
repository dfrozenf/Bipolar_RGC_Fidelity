from Raster import read_spiketrains
import StimulusTimes
from pylab import *
import csv

def main():

    print('Upload trigger file: ')
    myLights = StimulusTimes.main()
    myLights = np.array(myLights).reshape((len(myLights),4))
    print('Upload sorted spikes: ')
    mySpikes = read_spiketrains()

    wash_ID = ['Control', 'MFA', 'DNQX']
    wash_times = [2109.9, 14664.8 - 2117.6]
    wash_times.insert(0, 0)
    wash_times.insert(len(wash_times) + 1, max(mySpikes['Timestamp']))

    tau = 0.01
    min_tau = -1.5
    max_tau = 1.5
    xx = [i for i in np.arange(min_tau, max_tau, tau)]

    light0 = [i for i in myLights if wash_times[0] < i[0] < wash_times[1]]
    light0 = np.array(light0).reshape((len(light0), 4))
    light1 = [i for i in myLights if wash_times[1] < i[0] < wash_times[2]]
    light1 = np.array(light1).reshape((len(light1), 4))
    light2 = [i for i in myLights if wash_times[2] < i[0] < wash_times[3]]
    light2 = np.array(light2).reshape((len(light2), 4))

    unit_list = [35.3, 46.1, 46.2, 46.3, 47.1, 47.2, 55.2, 56.3, 57.1, 57.2, 65.1,
                 66.1, 66.2, 67.1, 67.2, 67.3, 74.1, 74.2, 75.1, 76.1, 83.1, 83.2,
                 83.3, 84.2]

    control = mySpikes[mySpikes['Timestamp'] < wash_times[1]]
    mfa = mySpikes[mySpikes['Timestamp'] > wash_times[1]]
    mfa = mfa[mfa['Timestamp'] < wash_times[2]]
    dnqx = mySpikes[mySpikes['Timestamp'] > wash_times[2]]

    with open('E:/Fidelity/22_3_22_rd1_cck_cre_ai32/Figs/timewise_firing_prob.csv', 'a') as f:
        np.savetxt(f, np.array(xx)[None], delimiter=',', newline='\n')

    for i in unit_list:
        control_ = control[control['Units'] == i]
        mfa_ = mfa[mfa['Units'] == i]
        dnqx_ = dnqx[dnqx['Units'] == i]

        p_control = []
        p_mfa = []
        p_dnqx = []

        for j in range(len(myLights)):

            light_on = myLights[j, 1]
            light_off = myLights[j, 2]

            if myLights[j,1] < wash_times[1]:
                wash = 'Control'
            elif wash_times[1] < myLights[j,1] < wash_times[2]:
                wash = 'MFA'
            elif myLights[j,1] > wash_times[2]:
                wash = 'DNQX'


            if wash == 'Control':
                spiketrain = [light_off - i for i in control_['Timestamp'] if (myLights[j, 0] < i < myLights[j, 0] + 3)]
                p_control.append([])
                for k in xx:
                    ind = len(p_control)
                    spiketrain_ = [i for i in spiketrain if k < i <= k+tau]
                    if len(spiketrain_) > 0:
                        p_control[ind-1].append(1)
                    elif len(spiketrain_) == 0:
                        p_control[ind-1].append(0)


            elif wash == 'MFA':
                spiketrain = [light_off - i for i in mfa_['Timestamp'] if (myLights[j, 0] < i < myLights[j, 0] + 3)]
                p_mfa.append([])
                for k in xx:
                    ind = len(p_mfa)
                    spiketrain_ = [i for i in spiketrain if k < i <= k + tau]
                    if len(spiketrain_) > 0:
                        p_mfa[ind-1].append(1)
                    elif len(spiketrain_) == 0:
                        p_mfa[ind-1].append(0)


            elif wash == 'DNQX':
                spiketrain = [light_off - i for i in dnqx_['Timestamp'] if (myLights[j, 0] < i < myLights[j, 0] + 3)]
                p_dnqx.append([])
                for k in xx:
                    ind = len(p_dnqx)
                    spiketrain_ = [i for i in spiketrain if k < i <= k+tau]
                    if len(spiketrain_) > 0:
                        p_dnqx[ind-1].append(1)
                    elif len(spiketrain_) == 0:
                        p_dnqx[ind-1].append(0)
        p_control = np.array(p_control).reshape((len(p_control), len(xx)))
        p_dnqx = np.array(p_mfa).reshape((len(p_mfa), len(xx)))
        p_mfa = np.array(p_dnqx).reshape((len(p_dnqx), len(xx)))

        p_control = np.mean(p_control, axis = 0)
        with open('E:/Fidelity/22_3_22_rd1_cck_cre_ai32/Figs/timewise_firing_prob.csv', 'a') as f:
            np.savetxt(f, p_control[None], delimiter=',',newline='\n')

#    with open('E:/Fidelity/22_3_22_rd1_cck_cre_ai32/Figs/unit_list.csv', 'w') as f:
#        np.savetxt(f, unit_list, delimiter = ',', newline='\n')

if __name__ == '__main__':
    p = main()