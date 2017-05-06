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
        raster_t1 = np.load(os_path_join(data_dir_path, 'raster_rec1_t.npy'))
        raster_i1 = np.load(os_path_join(data_dir_path, 'raster_rec1_i.npy'))
        raster_t2 = np.load(os_path_join(data_dir_path, 'raster_rec2_t.npy'))
        raster_i2 = np.load(os_path_join(data_dir_path, 'raster_rec2_i.npy'))
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)
        self.ax1.plot(raster_t1, raster_i1, 'k|', ms=10)
        self.ax2.plot(raster_t2, raster_i2, 'k|', ms=10)
        self.ax2.set_xlabel('Time [msec]')
        # self.ax1.set_ylabel('Neuron')
        self.fig.tight_layout()

if __name__ == '__main__':
    profile_name = 'test'
    period = 500
    trial = 0
    gmax_rec = 0.010 * msiemens
    FLUC = 0 * (uA ** 2 / ms)
    a = 2.0 * uA
    freq = 50 * Hz
    jitter = -2 * ms

    fig = RasterFigure()
    fig.plot(profile_name, period, trial, gmax_rec, FLUC, a, freq, jitter)
    fig.save('{}.png'.format(__file__[:-3]))
    fig.show()
