# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2017-04-25
#
# Copyright (C) 2017 Taishi Matsumura
#
from os import getcwdu as os_getcwdu
from os.path import join as os_path_join
from figure_module import *
from brian2.units import *
import numpy as np

plt.close('all')


class RasterFigure(FigureModel):
    def __init__(self):
        self.fig = plt.figure(figsize=(18, 4), dpi=80)

    def plot(self, profile_name, period, trial, gmax_rec, FLUC, a, freq, jitter):
        dirs = [
            os_getcwdu(), 'ResultData', profile_name,
            '{}periods'.format(period), 'trial{}'.format(trial),
            'gmax_rec={}'.format(gmax_rec), 'FLUC={}'.format(FLUC),
            'jitter={}'.format(jitter), 'a={}'.format(a),
            'freq={}'.format(freq)]
        data_dir_path = os_path_join(*dirs)
        raster_t = np.load(os_path_join(data_dir_path, 'raster_rec1_t.npy'))
        raster_i = np.load(os_path_join(data_dir_path, 'raster_rec1_i.npy'))
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(raster_t, raster_i, 'k|', ms=10)
        self.ax.set_xlabel('Time [msec]')
        self.ax.set_ylabel('Neuron')
        self.fig.tight_layout()

if __name__ == '__main__':
    profile_name = 'synamat'
    period = 100
    trial = 0
    gmax_rec = 0.010 * msiemens
    FLUC = 100000 * (uA ** 2 / ms)
    a = 2.0 * uA
    freq = 40 * Hz
    jitter = -2 * ms

    fig = RasterFigure()
    fig.plot(profile_name, period, trial, gmax_rec, FLUC, a, freq, jitter)
    fig.save('{}.png'.format(__file__[:-3]))
    fig.show()
