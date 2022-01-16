import numpy as np
from tkinter.filedialog import askopenfilename

def read_lightbins(filepath):
    with open(filepath, 'r') as f:
        input = f.readlines()
    input = input[4:]
    input = [i.rstrip().split('\t') for i in input]
    input = np.array(input).reshape((len(input),3))
    time = input[:,1]
    time = [float(i) for i in time]
    return time

def calc_lightbins(TTL):
    lighton = []
    lightoff = []
    i = 1
    while i < len(TTL):
        if TTL[i]-TTL[i-1] >= 4:
            lighton.append(TTL[i-1])
            lightoff.append(TTL[i])
        i += 1
    lights = np.array([lighton, lightoff]).reshape((2, len(lighton))).transpose()

    return lights

def main():
    filepath = askopenfilename()
    myTTL = read_lightbins(filepath)
    myLights = calc_lightbins(myTTL)

    return myLights

if __name__ == '__main__':
    myLights = main()
