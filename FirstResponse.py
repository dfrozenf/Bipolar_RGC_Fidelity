from Raster import read_spiketrains
import StimulusTimes
import numpy as np
from scipy.signal import correlate
import matplotlib.pyplot as plt



def main():
    myLights = StimulusTimes.main() / 1000

    mySpikes = read_spiketrains()

    while myLights[-1][0] > max(mySpikes['Timestamp']):
        myLights = myLights[:-1, :]

    latencies = {}
    responses = {}
    for j in set(mySpikes['Unit']):
        latencies[j] = []
        responses[j] = []

    for i in latencies.keys():
        spiketrain = mySpikes[mySpikes['Unit']==i]['Timestamp'].to_numpy()
        for j in range(len(myLights)):
            light_on = myLights[j][0]
            response = np.argmax(spiketrain > light_on)
            if response != 0:
                latency = spiketrain[response] - light_on
                latencies[i].append(latency)
                responses[i].append(response)

    for i in latencies.keys():
        cc = correlate(myLights[:,0], responses[i])
        for j in range(len(responses[i])):
            plt.plot(j, cc[j])
        plt.title('Cross-correlation for Unit {}'.format(i))
        plt.show()

    return responses, myLights

if __name__ == '__main__':
    main()
