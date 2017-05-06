# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2017-03-06
#
# Copyright (C) 2017 Taishi Matsumura
#
from os import getcwdu as os_getcwdu
from os.path import join as os_path_join
from figure_module import *
from brian2.units import *
import numpy as np

plt.close('all')


class StatesFigure(FigureModel):
    def __init__(self):
        super(StatesFigure, self).__init__()

    def plot(self, profile_name, period, trial, gmax_rec, FLUC, a, freq, jitter):
        dirs = [
            os_getcwdu(), 'ResultData', profile_name,
            '{}periods'.format(period), 'trial{}'.format(trial),
            'gmax_rec={}'.format(gmax_rec), 'FLUC={}'.format(FLUC),
            'jitter={}'.format(jitter), 'a={}'.format(a),
            'freq={}'.format(freq)]
        data_dir_path = os_path_join(*dirs)
        t = np.load(os_path_join(data_dir_path, 't.npy'))
        V = np.load(os_path_join(data_dir_path, 'V.npy'))
        Istim = np.load(os_path_join(data_dir_path, 'Istim.npy'))
        Inz = np.load(os_path_join(data_dir_path, 'Inz.npy'))
        Irec = np.load(os_path_join(data_dir_path, 'Irec.npy'))
        self.ax1 = self.fig.add_subplot(411)
        self.ax2 = self.fig.add_subplot(412)
        self.ax3 = self.fig.add_subplot(413)
        self.ax4 = self.fig.add_subplot(414)
        self.ax1.plot(t, V.T, ms=2)
        self.ax2.plot(t, Istim.T, ms=2)
        self.ax3.plot(t, Irec.T, ms=2)
        self.ax4.plot(t, Inz.T, ms=2)
        self.ax3.set_xlabel('Time [msec]')
        # self.ax.set_ylabel('Neuron')
        self.fig.tight_layout()

if __name__ == '__main__':
    profile_name = 'synamat'
    period = 500
    trial = 0
    gmax_rec = 0.010 * msiemens
    FLUC = 1000 * (uA ** 2 / ms)
    a = 2.0 * uA
    freq = 40 * Hz
    jitter = -2 * ms

    fig = StatesFigure()
    fig.plot(profile_name, period, trial, gmax_rec, FLUC, a, freq, jitter)
    fig.save('{}.png'.format(__file__[:-3]))
    fig.show()
