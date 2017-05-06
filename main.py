# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2017-03-23
#
# Copyright (C) 2017 Taishi Matsumura
#
from shutil import copy as shutil_copy
from os import getcwdu as os_getcwdu
from os.path import join as os_path_join
import multiprocessing as mp
import argparse
from module import *
from params import *
from brian2 import *
defaultclock.dt = DT
prefs.codegen.target = 'cython'
close('all')


class Main(object):
    def __init__(self, *loop_params):
        self.loop_params = loop_params
        self.params_tuples = self.return_params_tuple()
        self.args = self.first()

    def return_params_tuple(self):
        trials, jitters, FLUCs, freqs = self.loop_params
        return [(i, j, k, l) for i in trials for j in jitters for k in FLUCs for l in freqs]

    def first(self):
        parser = argparse.ArgumentParser(description='Network simulation')
        parser.add_argument('--multi', '-m', type=int, default=0,
            help='Number of process that run at the same time: max={}'.format(mp.cpu_count()))
        args = parser.parse_args()
        print('')
        print('# process: {}'.format(args.multi))
        print('')
        return args

    def run(self):
        self.print_start_message()
        if self.args.multi >= 2:
            self.multi_core_processing()
        else:
            self.single_core_processing()
        self.print_end_message()

    def single_core_processing(self):
        for params_tuple in self.params_tuples:
            simulation_loop(*params_tuple)

    def multi_core_processing(self):
        pool = mp.Pool(self.args.multi)
        pool.map(wrapper, self.params_tuples)

    def print_start_message(self):
        if self.args.multi >= 2:
            print('multi_core_processing() is running now')
            print('')
        else:
            print('single_core_processing() is running now')
            print('')

    def print_end_message(self):
        print('All simulation finished.')

def simulation_loop(trial, jitter, FLUC, freq):
    tmax = period * 1.0 / freq
    rec1 = AckerNeuronGroup(REC1_N, mode=MODE)
    rec2 = AckerNeuronGroup(REC2_N, mode=MODE)
    if STDP == 'add':
        # syna12 means synapses from group 1 to group 2
        syna11 = AddSTDPRecurrentSynapse(rec1, rec1, 'i!=j')
        syna12 = AddSTDPRecurrentSynapse(rec1, rec2, True)
        syna21 = AddSTDPRecurrentSynapse(rec2, rec1, True)
        syna22 = AddSTDPRecurrentSynapse(rec2, rec2, 'i!=j')
    elif STDP == 'mlt':
        syna11 = MultiSTDPRecurrentSynapse(rec1, rec1, 'i!=j')
        syna12 = MultiSTDPRecurrentSynapse(rec1, rec2, True)
        syna21 = MultiSTDPRecurrentSynapse(rec2, rec1, True)
        syna22 = MultiSTDPRecurrentSynapse(rec2, rec2, 'i!=j')
    elif stdp == 'log':
        syna11 = LogSTDPRecurrentSynapse(rec1, rec1, 'i!=j')
        syna12 = LogSTDPRecurrentSynapse(rec1, rec2, True)
        syna21 = LogSTDPRecurrentSynapse(rec2, rec1, True)
        syna22 = LogSTDPRecurrentSynapse(rec2, rec2, 'i!=j')
    stim = RelativeJitterGroup(STIM_N, tmax, freq, jitter)
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
    synamat11 = np.zeros((REC1_N, REC1_N))
    synamat12 = np.zeros((REC2_N, REC1_N))
    synamat21 = np.zeros((REC1_N, REC2_N))
    synamat22 = np.zeros((REC2_N, REC2_N))
    synamat11[syna11.j[:], syna11.i[:]] = syna11.w[:]
    synamat12[syna12.j[:], syna12.i[:]] = syna12.w[:]
    synamat21[syna21.j[:], syna21.i[:]] = syna21.w[:]
    synamat22[syna22.j[:], syna22.i[:]] = syna22.w[:]

    variables = {
        'meanw_rec1': meanw_rec1,
        'meanw_rec2': meanw_rec2,
        'ws11': syna11.w,
        'ws12': syna12.w,
        'ws21': syna21.w,
        'ws22': syna22.w,
        'synamat11': synamat11,
        'synamat12': synamat12,
        'synamat21': synamat21,
        'synamat22': synamat22,
        'syna_rec11': synamon_rec11.w,
        'syna_rec12': synamon_rec12.w,
        'syna_rec21': synamon_rec21.w,
        'syna_rec22': synamon_rec22.w,
        'raster_rec1_t': spkmon_rec1.t[:],
        'raster_rec2_t': spkmon_rec2.t[:],
        'raster_rec1_i': spkmon_rec1.i[:],
        'raster_rec2_i': spkmon_rec2.i[:]}
    params = {
        'DT': DT,
        'MODE': MODE,
        'STDP': STDP,
        'REC1_N': REC1_N,
        'REC2_N': REC2_N,
        'a': a,
        'gmax_rec': gmax_rec,
        'period': period,
        'trial': trial,
        'jitter': jitter,
        'FLUC': FLUC,
        'freq': freq}
    dirs = [
        os_getcwdu(), 'ResultData', profile_name,
        '{}periods'.format(period), 'trial{}'.format(trial),
        'gmax_rec={}'.format(gmax_rec), 'FLUC={}'.format(FLUC),
        'jitter={}'.format(jitter), 'a={}'.format(a),
        'freq={}'.format(freq)]
    data_dir_path = os_path_join(*dirs)
    makedirs(data_dir_path)
    save_data(variables, data_dir_path, mode='npy')
    pickle(params, data_dir_path, 'params.pkl')
    shutil_copy('./params.py', data_dir_path)

def wrapper(params_tuple):
    return simulation_loop(*params_tuple)

if __name__ == '__main__':
    # When you wanna use multiprocessing module,
    # you'd better write this line to avoid freezing.
    mp.freeze_support()

    main = Main(trials, jitters, FLUCs, freqs)
    main.run()
