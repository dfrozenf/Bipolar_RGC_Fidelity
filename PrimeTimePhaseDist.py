from Raster import read_spiketrains
import math
import StimulusTimes
from pylab import *
from matplotlib.patches import Rectangle
import matplotlib.patches as patches
import matplotlib.path as path
from scipy.optimize import curve_fit
from basic_units import radians

def main():
    print('Upload trigger file: ')
    myLights = StimulusTimes.main()
    myLights = np.array(myLights).reshape((len(myLights),4))
    print('Upload sorted spikes: ')
    mySpikes = read_spiketrains()

    unit_list = [35.3, 46.1, 46.2, 46.3, 47.1, 47.2, 55.2, 56.3, 57.1, 57.2, 65.1,
                 66.1, 66.2, 67.1, 67.2, 67.3, 74.1, 74.2, 75.1, 76.1, 83.1, 83.2,
                 83.3, 84.2]

    wash_ID = ['Control', 'MFA', 'DNQX']
    wash_times = [2109.9, 14664.8 - 2117.6]
    wash_times.insert(0, 0)
    wash_times.insert(len(wash_times) + 1, max(mySpikes['Timestamp']))

    success_window = [0.02, 0.06]

    control = mySpikes[mySpikes['Timestamp'] <= wash_times[1]]

    xx = np.linspace(0, 2*np.pi, 60)

    success = []
    fail = []

    for i in unit_list:
        control_ = control[control['Units'] == i]
        for j in range(len(myLights)):
            spiketrain = [i - myLights[j, 1] for i in control_['Timestamp'] if myLights[j,0] < i < myLights[j,0] + 3.3]
            post = list(sorted([i for i in spiketrain if i > 0]))
            pre = list(sorted([i for i in spiketrain if i <= 0]))
            if len(pre) > 4 and post:
                fig, ax = plt.subplots(1, 2)
                t,s = create_signal(pre)
                ax[0].plot(t, s)
                a = np.fft.fft(s)
                print(a)
                ax[1].plot([i for _ in range(len(a))], a)
                plt.show()

def create_signal(spiketrain, spiketime = 0.005):
    t = [round(i,4) for i in np.arange(-1.5, 0, spiketime)]
    s = [0 for i in np.arange(-1.5, 0, spiketime)]
    for i in spiketrain:
        bin = np.digitize(i, t)
        s[bin] = 1
    return t,s

if __name__ == '__main__':
    main()