# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2017-03-23
#
# Copyright (C) 2017 Taishi Matsumura
#
from module import *
from params import *
from brian2 import *
defaultclock.dt = DT
prefs.codegen.target = 'cython'
close('all')

REC1_N = 50
REC2_N = 50


class Main(object):
    def __init__(self):
        pass

    def run(self):
        tmax = period * 1.0 / freq
        data_dir_path = '{0}Data/gmax_rec={1}mS/FLUC={2}/jitter={3}ms/a={4}uA/freq={5}Hz/'.format(profile_root, gmax_rec, FLUC, jitter, a, freq)
        rec1 = AckerNeuronGroup(REC1_N, mode='Ih')
        rec2 = AckerNeuronGroup(REC2_N, mode='Ih')
        syna11 = AddSTDPRecurrentSynapse(rec1, rec1, 'i!=j')
        syna12 = AddSTDPRecurrentSynapse(rec1, rec2, True)
        syna21 = AddSTDPRecurrentSynapse(rec2, rec1, True)
        syna22 = AddSTDPRecurrentSynapse(rec2, rec2, 'i!=j')
        stim = RelativeJitterGroup(10, tmax, freq, jitter)
        stim_rec1 = NormalInputSynapses(stim, rec1)

        spkmon_rec1 = SpikeMonitor(rec1)
        spkmon_rec2 = SpikeMonitor(rec2)
        ratemon_rec1 = PopulationRateMonitor(rec1)
        ratemon_rec2 = PopulationRateMonitor(rec2)
        synamon_rec11 = StateMonitor(syna11, 'w', record=[0, 1])
        synamon_rec12 = StateMonitor(syna12, 'w', record=[0, 1])
        synamon_rec21 = StateMonitor(syna21, 'w', record=[0, 1])
        synamon_rec22 = StateMonitor(syna22, 'w', record=[0, 1])
        wtotmon_rec1 = StateMonitor(rec1, 'wtot', record=True)
        wtotmon_rec2 = StateMonitor(rec2, 'wtot', record=True)

        run(tmax, report='text')

        meanw_rec1 = (wtotmon_rec1.wtot.sum(0)) / (REC1_N**2 - REC1_N)
        meanw_rec2 = (wtotmon_rec2.wtot.sum(0)) / (REC2_N**2 - REC2_N)

        variables = {
            'meanw_rec1': meanw_rec1,
            'meanw_rec2': meanw_rec2,
            'ws11': syna11.w,
            'ws12': syna12.w,
            'ws21': syna21.w,
            'ws22': syna22.w,
            'synamat11': getSynamat(REC1_N, syna11.w),
            'synamat22': getSynamat(REC2_N, syna22.w),
            'syna_rec11': synamon_rec11.w,
            'syna_rec12': synamon_rec12.w,
            'syna_rec21': synamon_rec21.w,
            'syna_rec22': synamon_rec22.w,
            'raster_rec1_t': spkmon_rec1.t[:],
            'raster_rec2_t': spkmon_rec2.t[:],
            'raster_rec1_i': spkmon_rec1.i[:],
            'raster_rec2_i': spkmon_rec2.i[:]}
        saveData(variables, data_dir_path, mode='npy')

if __name__ == '__main__':
    main = Main()
    main.run()
