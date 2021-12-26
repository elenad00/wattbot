from matplotlib import pyplot as plt
import numpy as np

def plot(data):
    print("[-] Plotting Data")
    try:
        for i in range(len(data)):
            y = np.array(data[i])
            x = np.array([0, len(data[i])])
            plt.subplot(3,2,i+1)
            plt.plot(x, y)
        plt.show()
    except Exception:
        print("[!] Not enough data to plot")
