import matplotlib.pyplot as plt
import numpy as np


# You probably won't need this if you're embedding things in a tkinter plot...


class graphf():
    def __init__(self, min=2400000000, max=2500000000, n=100, ymin=-100, ymax=0):
        plt.ion()
        plt.style.use('dark_background')
        self.x = np.linspace(min, max, n)
        self.y = [1 for i in range(n)]
        self.ymin = ymin
        self.ymax = ymax
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.line1, = self.ax.plot(self.x, self.y, 'r-')

    def update(self, y_buffer):

        self.update_borne(y_buffer)
        self.line1.set_ydata(y_buffer)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def update_axis(self):
        self.ax.set_ylim([self.ymin, self.ymax])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def update_borne(self, y_buffer):
        min = y_buffer[0]
        max = y_buffer[0]
        for i in range(len(y_buffer)):
            if y_buffer[i] > max:
                max = y_buffer[i]
            if y_buffer[i] < min:
                min = y_buffer[i]
        if min < self.ymin:
            self.ymin = min
        if max > self.ymax:
            self.ymax = max
        self.update_axis()


if __name__ == '__main__':
    g = graphf(0, 10, 10)
    a = [5.0, 7.0, 5.0, 4.0, 7.0, 50.0, 9.0, 10.0, 9.0, 8.0]

    g.update(a)
