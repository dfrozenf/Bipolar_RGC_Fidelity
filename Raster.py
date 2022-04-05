import StimulusTimes
import numpy as np
import pandas as pd
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def main():

    myLights = StimulusTimes.main()

    mySpikes = read_spiketrains()
    myUnits = sort_spiketrains(mySpikes)

    fig, ax = plt.subplots(1,1)
    for i in range(len(mySpikes)):
        ax.plot(mySpikes['Timestamp'][i],
                 mySpikes['Units'][i],
                 marker = 'o', color = 'black')


    for i in range(len(myLights)):
        ax.add_patch(Rectangle((myLights[i][1],0),
                               (myLights[i][2]-myLights[1][0]),
                               max(mySpikes['Units']),
                               color = 'blue',
                               alpha = 0.5))
    ax.set_xlim(0, max(mySpikes['Timestamp']))
    ax.set_ylim(0, max(mySpikes['Units']))
    ax.set_title(input('Name this graph: '))
    #ax.vlines([2044.7, 3538.0], ymin=0, ymax=88, color = 'red')
    fig.show()

def read_spiketrains():
    print('Select a sorted recording')
    filepath = askopenfilename()
    input = pd.read_csv(filepath)
    input['Channel Name'] = [i[-2:] for i in input['Channel Name']]
    input['Channel Name'] = input['Channel Name'].apply(lambda x: float(x))
    input['Unit'].apply(lambda x: float(x))
    input['Units'] = input['Channel Name'] + input['Unit']/10

    return input

def sort_spiketrains(spikes):

    unit_list = spikes.groupby('Unit').size()
    unit_list = unit_list.sort_values(ascending = False)
    unit_list = unit_list.index.to_list()
    return unit_list

if __name__ == '__main__':
    main()