import matplotlib.pyplot as plt
import numpy as np


# You probably won't need this if you're embedding things in a tkinter plot...


class graphf():
    def __init__(self, min=2400000000, max=2500000000, n=100):
        plt.ion()
        plt.style.use('dark_background')
        self.x = np.linspace(min, max, n)
        self.y = [1 for i in range(n)]
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.line1, = self.ax.plot(self.x, self.y, 'r-')

    def update(self, y_buffer):
        self.line1.set_ydata(y_buffer)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


if __name__ == '__main__':
    g = graphf()
    for i in range(100):
        g.update([i*0.5 for i in range(20)])
