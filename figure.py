# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2017-05-06
#
# Copyright (C) 2017 Taishi Matsumura
#
from os import getcwdu as os_getcwdu
from os.path import join as os_path_join
from figure_module import *
from brian2.units import *
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

plt.close('all')


class SynapseMatrix(FigureModel):
    '''
    !!! Restriction !!!
    group = 2
    group_ns = (20, 80)
    '''
    def __init__(self, profile_name, trial, gmax_rec, FLUC, a, freq, jitter, group_ns=(20, 80)):
        super(SynapseMatrix, self).__init__()
        dirs = [
            os_getcwdu(), 'ResultData', profile_name,
            '{}periods'.format(period), 'trial{}'.format(trial),
            'gmax_rec={}'.format(gmax_rec), 'FLUC={}'.format(FLUC),
            'jitter={}'.format(jitter), 'a={}'.format(a),
            'freq={}'.format(freq)]
        data_dir_path = os_path_join(*dirs)
        self.synamat11 = np.load(os_path_join(data_dir_path, 'synamat11.npy'))
        self.synamat12 = np.load(os_path_join(data_dir_path, 'synamat12.npy'))
        self.synamat21 = np.load(os_path_join(data_dir_path, 'synamat21.npy'))
        self.synamat22 = np.load(os_path_join(data_dir_path, 'synamat22.npy'))
        self.group_ns = group_ns
        self.group = len(group_ns)
    
    def reload(self, path):
        self.synamat = np.load(path)

    def get_pre_mean(self):
        return self.synamat.mean(0)

    def get_post_mean(self):
        return self.synamat.mean(1)

    def get_separated_matrix(self):
        # elements in s_synamat is row order
        s_synamat = []
        tmp = np.hsplit(self.synamat11, [20])
        s_synamat.append(np.vsplit(tmp[0], [20])[0])
        s_synamat.append(np.vsplit(tmp[0], [20])[1])
        s_synamat.append(np.vsplit(tmp[1], [20])[0])
        s_synamat.append(np.vsplit(tmp[1], [20])[1])
        return s_synamat

    def get_group_mean(self):
        # !!! need to modify for no all-to-all connection !!!
        s_synamat = self.get_separated_matrix()
        m = []
        for s in s_synamat:
            if s.shape[0] == s.shape[1]:
                m.append(s.sum() / (s.shape[0] ** 2 - s.shape[0]))
            else:
                m.append(s.mean())
        return m

    def plot_synamat(self):
        self.ax11 = self.fig.add_subplot(221)
        self.ax12 = self.fig.add_subplot(222)
        self.ax21 = self.fig.add_subplot(223)
        self.ax22 = self.fig.add_subplot(224)
        im = self.ax11.imshow(self.synamat11, interpolation='none', vmin=0, vmax=1)
        self.ax12.imshow(self.synamat12, interpolation='none', vmin=0, vmax=1)
        self.ax21.imshow(self.synamat21, interpolation='none', vmin=0, vmax=1)
        self.ax22.imshow(self.synamat22, interpolation='none', vmin=0, vmax=1)
        '''
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes('right', size='5%', pad=0.1)
        cb = self.fig.colorbar(im, cax=cax)
        cb.set_label('Weight [a.u.]')
        self.ax.set_xlabel('Pre neuron')
        self.ax.set_ylabel('Post neuron')
        '''

    def plot_sep_mean(self):
        self.ax = self.fig.add_subplot(111)
        bar = self.get_group_mean()
        tick_label = ('G1->G1', 'G1->G2', 'G2->G1', 'G2->G2')
        self.ax.bar(xrange(4), bar, tick_label=tick_label, align='center')
        self.ax.set_ylabel('Weight [a.u.]')

if __name__ == '__main__':
    profile_name = 'synamat'
    period = 100
    trial = 0
    gmax_rec = 0.010 * msiemens
    FLUC = 100000 * (uA ** 2 / ms)
    a = 2.0 * uA
    freq = 40 * Hz
    jitter = -2 * ms

    syn = SynapseMatrix(profile_name, trial, gmax_rec, FLUC, a, freq, jitter)
    syn.plot_synamat()
    syn.save('{}.png'.format(__file__[:-3]))
    syn.show()
