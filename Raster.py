import StimulusTimes
import numpy as np
import pandas as pd
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def main():
    params = {"Lights": int(input('Light? (1/0)'))}

    if params["Lights"] == 1:
        print('Select a trigger file')
        myLights = StimulusTimes.main()/1000

    mySpikes = read_spiketrains()
    myUnits = sort_spiketrains(mySpikes)

    fig, ax = plt.subplots(1,1)
    for i in range(len(mySpikes)):
        ax.plot(mySpikes['Timestamp'][i],
                 myUnits.index(mySpikes['Unit'][i]),
                 marker = '|', color = 'black')

    if params["Lights"] == 1:
        for i in range(len(myLights)):
            ax.add_patch(Rectangle((myLights[i][0],0),
                                   (myLights[i][1]-myLights[i][0]),
                                   len(myUnits),
                                   color = 'blue',
                                   alpha = 0.5))
    ax.set_xlim(0, max(mySpikes['Timestamp']))
    ax.set_ylim(0, len(myUnits))
    ax.set_title(input('Name this graph: '))
    fig.show()


def read_spiketrains():
    print('Select a sorted recording')
    filepath = askopenfilename()
    input = pd.read_csv(filepath)
    input['Unit'] = input['Channel'] + input['Unit']/10

    return input

def sort_spiketrains(spikes):

    unit_list = spikes.groupby('Unit').size()
    unit_list = unit_list.sort_values(ascending = False)
    unit_list = unit_list.index.to_list()
    return unit_list

if __name__ == '__main__':
    main()