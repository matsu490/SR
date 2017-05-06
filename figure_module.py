# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2017-02-09
#
# Copyright (C) 2017 Taishi Matsumura
#
import matplotlib.pyplot as plt
size = 18
p = {'font.size': size,
    'axes.labelsize': size,
    'legend.fontsize': size,
    'xtick.labelsize': size,
    'ytick.labelsize': size,
    'font.family': 'serif',
    'font.sans-serif': 'Times New Roamn',
    'text.usetex': False}
plt.rcParams.update(p)


class FigureModel(object):
    def __init__(self):
        self.fig = plt.figure(figsize=(10, 8), dpi=80)

    def show(self):
        plt.show()

    def close(self):
        plt.close(self.fig)

    def save(self, name):
        self.fig.savefig(name, transparent=True)


class ParamsLabels(FigureModel):
    def __init__(self):
        super(ParamsLabels, self).__init__()
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.set_xticklabels([])
        self.ax1.set_yticklabels([])
        self.ax1.patch.set_facecolor('none')
        self.ax1.spines['right'].set_color('none')
        self.ax1.spines['top'].set_color('none')
        self.ax1.spines['bottom'].set_color('none')
        self.ax1.spines['left'].set_color('none')
        self.ax1.tick_params(axis='x', which='both', top='off', bottom='off', labelbottom='off')
        self.ax1.tick_params(axis='y', which='both', left='off', right='off', labelbottom='off')

    def plot(self, params):
        self.ax1.set_ylim(-1, 10 + len(params))
        for y, (key, val) in enumerate(params.items()):
            self.ax1.text(0, y, '{0} = {1}'.format(key, val))
        # Following a line is needed to be put after drqwing.
        self.ax1.invert_yaxis()
