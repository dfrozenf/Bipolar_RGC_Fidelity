from Raster import read_spiketrains
import math
import StimulusTimes
from pylab import *
from matplotlib.patches import Rectangle
import matplotlib.patches as patches
import matplotlib.path as path
from scipy.optimize import curve_fit

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

    xx = np.linspace(-1.5, 0, 100)

    success = {}
    fail = {}

    for i in unit_list:
        success_, fail_ = [], []
        control_ = control[control['Units'] == i]
        for j in range(len(myLights)):
            spiketrain = [i - myLights[j, 1] for i in control_['Timestamp'] if myLights[j,0] < i < myLights[j,0] + 3.3]
            post = list(sorted([i for i in spiketrain if i > 0]))
            pre = list(sorted([i for i in spiketrain if i <= 0]))
            if post and pre:
                if success_window[0] <= post[0] < success_window[1]:
                    success_.append(pre[-1])
                else:
                    fail_.append(pre[-1])

        try:
            fig, ax = plt.subplots(1, 2, sharex='col', sharey='row')
            ax[0].set_ylim(0, 40)
            fig.suptitle('Distribution of prime time: Unit {}'.format(i))
            (n, bins, patches) = ax[0].hist(success_)
            bins = [(bins[i]+bins[i+1])/2 for i in range(len(bins)-1)]
            ax[0].set_title('Distribution of prime times \nin successful trials')
            ax[0].set_xlabel('Prime Time (s)')
            ax[0].set_ylabel('Counts')
            fit = curve_fit(exp_fit, bins, n)[0]
            ax[0].plot(xx, [exp_fit(i, fit[0], fit[1], fit[2]) for i in xx], c='red')
            success[i] = {'Mode': n.argmax(), 'A': fit[0], 'b': fit[1], 'c': fit[2], 'n': sum(n)}

            (n, bins, patches) = ax[1].hist(fail_)
            ax[1].set_title('Distribution of prime times \nin failed trials')
            ax[1].set_xlabel('Prime Time (s)')
            bins = [(bins[i]+bins[i+1])/2 for i in range(len(bins)-1)]
            fit = curve_fit(exp_fit, bins, n)[0]
            ax[1].plot(xx, [exp_fit(i, fit[0], fit[1], fit[2]) for i in xx], c='red')
            plt.show()
            fail[i] = {'Mode': n.argmax(), 'A': fit[0], 'b': fit[1], 'c': fit[2], 'n': sum(n)}
        except RuntimeError:
            pass

    return success, fail





def exp_fit(x, a, b, c):
    y = a * np.exp(b*x) + c
    return y

if __name__ == '__main__':
    success, fail = main()