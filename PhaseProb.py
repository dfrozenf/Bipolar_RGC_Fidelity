from Raster import read_spiketrains
import math
import StimulusTimes
from pylab import *
from matplotlib.patches import Rectangle
import matplotlib.patches as patches
import matplotlib.path as path
from basic_units import radians

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

    success_window = [0.02, 0.06]
    xx = np.linspace(0, 2*np.pi, 60)
    yy = {}
    for t in xx:
        yy[t] = [0, 0]

    unit_list = [35.3, 46.1, 46.2, 46.3, 47.1, 47.2, 55.2, 56.3, 57.1, 57.2, 65.1,
                 66.1, 66.2, 67.1, 67.2, 67.3, 74.1, 74.2, 75.1, 76.1, 83.1, 83.2,
                 83.3, 84.2]

    control = mySpikes[mySpikes['Timestamp'] <= wash_times[1]]

    for i in unit_list:

        control_ = control[control['Units'] == i]

        for j in range(len(myLights)):

            trialstart = myLights[j, 0]
            lighton = myLights[j, 1]

            spiketrain = sorted([lighton - i for i in control_['Timestamp'] if trialstart <= i <= trialstart + 3 ])

            spike1 = sorted([i for i in spiketrain if i < 0])

            spike2 = sorted([i for i in spiketrain if i >= 0])

            if len(spike1) > 4 and spike2:
                period = [spike1[i + 1] - spike1[i] for i in range(len(spike1) - 1)]
                period = (period[-1] + period[-2] + period[-3]) / 3
                phase = -spike1[-1] * 2 * np.pi / period
                bin = np.digitize(phase, xx)-1
                bin = xx[bin]
                if success_window[0] <= spike2[0] < success_window[1]:
                    yy[bin] = [yy[bin][0] + 1, yy[bin][1]]
                else:
                    yy[bin] = [yy[bin][0], yy[bin][1]  + 1 ]
    xx = [i * radians for i in np.linspace(0, 2*np.pi, 60)]
    for t in yy.keys():
        if yy[t] != [0, 0]:
            plt.scatter(t*radians, yy[t][0], color = 'blue', label = 'Success', xunits = radians)
            plt.scatter(t*radians, yy[t][1], color = 'black', label = 'Fail', xunits = radians)
            #ax.add_patch(Rectangle(xy = (t, 0), width = 0.01, height = yy[t][0], color='blue', label='Success'))
            #ax.add_patch(Rectangle(xy = (t+0.01, 0), width = 0.01, height = yy[t][1], color = 'black', label = 'Failure'))
            #plt.scatter(t, yy[t][0]/sum(yy[t]), s=sum(yy[t])/10, c='black')
    plt.xlabel('Phase Estimate')
    plt.ylabel('Count')
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.title('P(ChR2 Response | Prime Time)')
    plt.show()

    for t in yy.keys():
        if yy[t] != [0, 0]:
            plt.scatter(t*radians, yy[t][0]/sum(yy[t]), color='blue', label='Success', xunits=radians)
            plt.scatter(t*radians, yy[t][1]/sum(yy[t]), color='black', label='Fail', xunits=radians)
            # plt.scatter(t, yy[t][0]/sum(yy[t]), s=sum(yy[t])/10, c='black')
    plt.xlabel('Phase Estimate')
    plt.ylabel('Probability')
    #handles, labels = plt.gca().get_legend_handles_labels()
    #by_label = dict(zip(labels, handles))
    #plt.legend(by_label.values(), by_label.keys())
    #plt.suptitle('P(Light Response | Timing of Preceding Spike)')
    plt.show()

if __name__ == '__main__':
    main()

