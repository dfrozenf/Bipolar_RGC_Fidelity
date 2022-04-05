import numpy as np
from tkinter.filedialog import askopenfilename


def read_lightbins(filepath):
    with open(filepath, 'r') as f:
        input = f.readlines()
    input = input[4:]
    input = [i.rstrip().split('\t') for i in input]
    input = np.array(input).reshape((len(input),5))
    nTr_Time = input[:,1]
    time = input[:,2]
    nTr_Time = [float(i) for i in nTr_Time]
    time = [float(i) for i in time]
    return [nTr_Time,time]

def calc_lightbins(TTL):
    lights = []
    trial_times = list(sorted(list(set(TTL[0]))))
    for t in trial_times:
        indices = [i for i, x in enumerate(TTL[0]) if x == t]
        timeon = TTL[1][min(indices)]
        timeoff = TTL[1][max(indices)]
        light = [t, timeon, timeoff, timeoff-timeon]
        light = [float(i)/1000 for i in light]
        lights.append(light)
    return lights

def main():
    filepath = askopenfilename()
    myTTL = read_lightbins(filepath)
    myLights = calc_lightbins(myTTL)

    return myLights

if __name__ == '__main__':
    myLights = main()
