from Raster import read_spiketrains
import math
import StimulusTimes
from pylab import *
from matplotlib.patches import Rectangle
import matplotlib.patches as patches
import matplotlib.path as path

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

    min_tau = -1.5
    max_tau = 1.5
    xx = np.linspace(min_tau, max_tau, 1000)

    unit_list = [35.3, 46.1, 46.2, 46.3, 47.1, 47.2, 55.2, 56.3, 57.1, 57.2, 65.1,
                 66.1, 66.2, 67.1, 67.2, 67.3, 74.1, 74.2, 75.1, 76.1, 83.1, 83.2,
                 83.3, 84.2]

    control = mySpikes[mySpikes['Timestamp'] < wash_times[1]]
    mfa = mySpikes[mySpikes['Timestamp'] > wash_times[1]]
    mfa = mfa[mfa['Timestamp'] < wash_times[2]]

    success_c, fail_c, success_m, fail_m = [], [], [], []
    fig, ax = plt.subplots(1, 2, sharey='all', sharex='all')
    nTr_c, nTr_m = 0, 0
    success_c_p, success_c_n, fail_c_p, fail_c_n, success_m_p, success_m_n, fail_m_p, fail_m_n = [], [], [], [], [], [], [], []
    for i in unit_list:

        control_ = control[control['Units'] == i]
        mfa_ = mfa[mfa['Units'] == i]


        for j in range(len(myLights)):

            light_on = myLights[j,1]
            light_off = myLights[j,2]
            if myLights[j,1] < wash_times[1]:
                wash = 'Control'
            elif wash_times[1] < myLights[j,1] < wash_times[2]:
                wash = 'MFA'
            elif myLights[j,1] > wash_times[2]:
                wash = 'DNQX'

            if wash == 'Control':
                nTr_c += 1
                spiketrain = sorted([light_on - i for i in control_['Timestamp'] if (myLights[j, 0] < i < myLights[j, 0] + 3)])
                ISIp = [i for i in spiketrain if i < 0]
                ISIn = [i for i in spiketrain if i >= 0]
                if len(ISIp) > 0 and len(ISIn) > 0:
                    p = ISIp[-1]

                    n = ISIn[0]
                    if 0.02 < n < 0.05:
                        ax[0].scatter(n, -p, color = 'red', s = 0.1)
                        success_c.append(n)
                        success_c_n.append(n)
                        success_c_p.append(p)

                    else:
                        ax[0].scatter(n, -p, color='black', s=0.1)
                        fail_c.append(n)
                        fail_c_n.append(n)
                        fail_c_p.append(p)

            elif wash == 'MFA':
                nTr_m += 1
                spiketrain = sorted(
                    [light_on - i for i in mfa_['Timestamp'] if (myLights[j, 0] < i < myLights[j, 0] + 3)])
                ISIp = sorted([i for i in spiketrain if i < 0])
                ISIn = sorted([i for i in spiketrain if i >= 0])
                if len(ISIp) > 0 and len(ISIn) > 0:
                    p = sorted(ISIp)[-1]

                    n = sorted(ISIn)[0]
                    if 0.02 < n < 0.05:
                        ax[1].scatter(n*1000, -p*1000, color='red', s=0.1)
                        success_m.append(n)
                        success_m_n.append(n)
                        success_m_p.append(p)

                    else:
                        ax[1].scatter(n*1000, -p*1000, color='black', s=0.1)
                        fail_m.append(n)
                        fail_m_n.append(n)
                        fail_m_p.append(p)

            elif wash == 'DNQX':
                pass

    fig.suptitle('ISI vs. ISI')
    #fig.suptitle('Latency of first post-stimulus spike (s)', y = 0.1)
    ax[0].set_title('Control')
    ax[1].set_title('MFA')
    ax[0].set_ylabel('Interval from last pre-stimulus spike to stimulus (ms)')
    ax[0].set_xscale('log')
    ax[0].set_yscale('log')
    plt.savefig('C:/Users/User/Desktop/ISIvsISI.png', dpi=300)
    plt.show()
    print('Control Trials: {}'.format(nTr_c))
    print('MFA Trials: {}'.format(nTr_m))
    print(' success_c_p: {} \nsuccess_c_n: {} \nfail_c_p: {} \nfail_c_n: {} \nsuccess_m_p: {} \nsuccess_m_n: {} \nfail_m_p: {} \nfail_m_n: {} '.format(success_c_p, success_c_n, fail_c_p, fail_c_n, success_m_p, success_m_n, fail_m_p, fail_m_n))
if __name__ == '__main__':
    main()