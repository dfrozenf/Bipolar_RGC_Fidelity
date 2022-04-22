from Raster import read_spiketrains
import math
import StimulusTimes
from pylab import *
from matplotlib.patches import Rectangle
import matplotlib.patches as patches
import matplotlib.path as path
from scipy.optimize import curve_fit

print('Upload trigger file: ')
myLights = StimulusTimes.main()
myLights = np.array(myLights).reshape((len(myLights), 4))
print('Upload sorted spikes: ')
mySpikes = read_spiketrains()
print('Select raw data')
filepath = askopenfilename()
input = pd.read_csv(filepath, header=None)



unit_list = [35.3, 46.1, 46.2, 46.3, 47.1, 47.2, 55.2, 56.3, 57.1, 57.2, 65.1,
             66.1, 66.2, 67.1, 67.2, 67.3, 74.1, 74.2, 75.1, 76.1, 83.1, 83.2,
             83.3, 84.2]

wash_ID = ['Control', 'MFA', 'DNQX']
wash_times = [2109.9, 14664.8 - 2117.6]
wash_times.insert(0, 0)
wash_times.insert(len(wash_times) + 1, max(mySpikes['Timestamp']))

success_window = [0.02, 0.06]

control = mySpikes[mySpikes['Timestamp'] <= wash_times[1]]
