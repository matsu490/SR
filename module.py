# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2017-03-23
#
# Copyright (C) 2017 Taishi Matsumura
#
from os import makedirs as os_makedirs
from os.path import join as os_path_join
from brian2 import SpikeGeneratorGroup, NeuronGroup, Synapses
from brian2.units import *
import numpy as np


def save_data(dic, save_data_dir, mode='npy'):
    os_makedirs(save_data_dir)
    keys = []
    if mode in ('npy', 'numpy'):
        for key, val in dic.items():
            file_path = os_path_join(save_data_dir, key + '.npy')
            np.save(file_path, val)
            keys.append(key)
        np.save(os_path_join(save_data_dir, 'data_list.npy'), keys)
    elif mode in ('txt', 'text', 'csv'):
        for key, val in dic.items():
            file_path = os_path_join(save_data_dir, key + '.csv')
            np.savetxt(file_path, val, fmt='%.6f', delimiter=',')
            keys.append(key)
        np.savetxt(os_path_join(save_data_dir, 'data_list.csv'), keys, fmt='%s')


def digDirectory(path):
    import os
    dirs = path.split('/')
    if dirs[0] == '.':
        check_path = '.'
        for dirc in dirs[1:]:
            check_path += '/' + dirc
            if not os.path.exists(check_path):
                os.mkdir(check_path)
            else:
                pass
    else:
        print('It is not relative path.')
    del os


def getSynamat(N, Synapses_w):
    synamat = np.zeros((N, N))
    for i in np.arange(N):
        for j in np.arange(N):
            if i == j:
                pass
            else:
                synamat[i, j] = Synapses_w[j, i]
    return synamat


class FixedJitterGroup(SpikeGeneratorGroup):
    def __init__(self, N, tmax, freq, jitter):
        indices = np.arange(0, N)
        T = 1.0 / freq
        iniT = T / 4 + jitter
        ''' When freq = 90Hz and jitter = -3msec, iniT becomes a negative value.
        '''
        if iniT < 0:
            iniT = iniT + T
        else:
            pass
        tmptimes = np.arange(iniT, tmax, T)
        times = []
        for itr_n in np.arange(0, len(tmptimes)):
            times.append(tmptimes[itr_n] * np.ones(N))
        indices = np.tile(indices, [1, len(tmptimes)])
        indices = np.hstack(indices)
        times = np.hstack(times) * second

        super(FixedJitterGroup, self).__init__(N, indices, times)


class RelativeJitterGroup(SpikeGeneratorGroup):
    def __init__(self, N, tmax, freq, jitter):
        ''' Give jitter as relative value from peak of oscillation,
            which is described by [-1, 1].
            e.g. jitter = -1, 0 and 1 means that stimulation time coincedents with
            phi = 0, phi = pi/2 and phi = pi of ocillation, respectively.
        '''
        indices = np.arange(0, N)
        T = 1.0 / freq
        iniT = T / 4 + jitter / ms * (T / 4)
        ''' When freq = 90Hz and jitter = -3msec, iniT becomes a negative value.
        '''
        if iniT < 0:
            iniT = iniT + T
        else:
            pass
        tmptimes = np.arange(iniT, tmax, T)
        times = []
        for itr_n in np.arange(0, len(tmptimes)):
            times.append(tmptimes[itr_n] * np.ones(N))
        indices = np.tile(indices, [1, len(tmptimes)])
        indices = np.hstack(indices)
        times = np.hstack(times) * second

        super(RelativeJitterGroup, self).__init__(N, indices, times)


class RandomJitterGroup(SpikeGeneratorGroup):
    def __init__(self, N, tmax, freq):
        T = 1.0 / freq
        iniT = T / 4
        tmptimes = np.arange(iniT, tmax, T)
        times = [itr + 0.001 * np.random.randint(-3, 4) for itr in tmptimes for itr2 in xrange(N)] * second
        indices = np.arange(N)
        indices = np.hstack([indices for itr in xrange(len(tmptimes))])

        super(RandomJitterGroup, self).__init__(N, indices, times)


class StepInputGroup(NeuronGroup):
    def __init__(self, N, dt, tmax, freq, jitter, dur):
        t = np.arange(0, tmax, dt) * second
        step = np.zeros(tmax / dt)
        T = 1.0 / freq
        iniT = T / 4 + jitter
        start_ts = np.arange(iniT, tmax, T) * second
        end_ts = start_ts + dur
        for start_t, end_t in zip(start_ts, end_ts):
            ind = np.logical_and(start_t <= t, t < end_t)
            step[ind] = 1
        steps = TimedArray(step, dt)
        eq = '''
            s = steps(t) : 1
            '''
        super(StepInputGroup, self).__init__(N, eq), steps


class NormalInputSynapses(Synapses):
    def __init__(self, source, target):
        model='''
            tau_stim = 1.0 * ms : second
            g_stim_post = s_stim : 1 (summed)
            ds_stim/dt = -s_stim / tau_stim : 1 (clock-driven)
            '''
        on_pre='''
            s_stim += 1
            '''
        super(NormalInputSynapses, self).__init__(
            source, target, method='rk4', model=model, on_pre=on_pre)
        self.connect('i==j')


class AckerNeuronGroup(NeuronGroup):
    def __init__(self, N, mode='Ih'):
        shared_params = '''
            Vth = 20.0 * mV : volt
            VNa = 55.0 * mV : volt
            VK = -90.0 * mV : volt
            Vh = -20.0 * mV : volt
            gK = 11.0 * msiemens : siemens
            Cm = 1.5 * uF : farad
        '''
        if mode == 'Ih':
            # with Ih, without IK model
            params = '''
                gNa = 52.0 * msiemens : siemens
                V_ha_Ks = 0.0 * mV : volt
                Iapp = -3.5 * uA : amp
                VL = -65.0 * mV : volt
                gNap = 0.5 * msiemens : siemens
                gh = 1.5 * msiemens : siemens
                gL = 0.5 * msiemens : siemens
                gKs = 0.0 * msiemens : siemens
            '''
        elif mode == 'IK':
            # without Ih, with IK model
            params = '''
                gNa = 52.0 * msiemens : siemens
                V_ha_Ks = -35.0 * mV : volt
                Iapp = -1.791 * uA : amp
                VL = -54.0 * mV : volt
                gNap = 0.21 * msiemens : siemens
                gh = 0.0 * msiemens : siemens
                gL = 0.1 * msiemens : siemens
                gKs = 2.0 * msiemens : siemens
            '''
        elif mode == 'IhIK':
            # with Ih and IK, without INa model
            params = '''
                gNa = 0.0 * msiemens : siemens
                V_ha_Ks = 0.0 * mV : volt
                Iapp = 0 * uA : amp
                VL = -65.0 * mV : volt
                gNap = 0.5 * msiemens : siemens
                gh = 1.5 * msiemens : siemens
                gL = 0.5 * msiemens : siemens
                gKs = 0.0 * msiemens : siemens
            '''
        eqs = '''
            Iwave = a * sin(2 * pi * freq * t) : amp

            Inz = (2.0 * FLUC * DT) ** 0.5 * randn() : amp (constant over dt)

            g_stim : 1
            Amp = 20.0 * uA : amp
            Istim = Amp * g_stim : amp

            g_rec : 1
            Vrec = 0.0 * mV : volt
            Irec = -gmax_rec * g_rec * (V - Vrec) : amp

            wtot : 1
            dV/dt = (Iapp + Iwave + Inz + Istim + Irec
                -(gNa * m ** 3 * h + gNap * mNap) * (V - VNa)
                -(gK * n ** 4 + gKs * mKs) * (V - VK)
                -gh * (0.65 * mhf + 0.35 * mhs) * (V - Vh)
                -gL * (V - VL)) / Cm : volt

            dm/dt = alpha_m * (1.0 - m) - beta_m * m : 1
            alpha_m = -0.1 * (V / mV + 23.0) / (exp(-0.1 * (V / mV + 23.0)) - 1.0) / ms : Hz
            beta_m = 4.0 * exp(-(V / mV + 48.0) / 18.0) / ms : Hz

            dh/dt = alpha_h * (1.0 - h) - beta_h * h : 1
            alpha_h = 0.07 * exp(-(V / mV + 37.0) / 20.0) / ms : Hz
            beta_h = 1.0 / (exp(-0.1 * (V / mV + 7.0)) + 1.0) / ms : Hz

            dn/dt = alpha_n * (1.0 - n) - beta_n * n : 1
            alpha_n = -0.01 * (V / mV + 27.0) / (exp(-0.1 * (V / mV + 27.0)) - 1.0) / ms : Hz
            beta_n = 0.125 * exp(-(V / mV + 37.0) / 80.0) / ms : Hz

            dmNap/dt = alpha_mNap * (1.0 - mNap) - beta_mNap * mNap : 1
            alpha_mNap = 1.0 / (0.15 * (1.0 + exp(-(V / mV + 38.0) / 6.5))) / ms : Hz
            beta_mNap = exp(-(V / mV + 38.0) / 6.5) / (0.15 * (1.0 + exp(-(V / mV + 38.0) / 6.5))) / ms : Hz

            dmKs/dt = (mKs_inf - mKs) / tau_mKs : 1
            mKs_inf = 1.0 / (1.0 + exp(-(V / mV - V_ha_Ks / mV) / 6.5)) : 1
            tau_mKs = 90.0 * ms : second

            dmhf/dt = (mhf_inf - mhf) / tau_mhf : 1
            mhf_inf = 1.0 / (1.0 + exp((V / mV + 79.2) / 9.78)) : 1
            tau_mhf = 0.51 / (exp((V / mV - 1.7) / 10.0) + exp(-(V / mV + 340.0) / 52.0) + 1.0) * ms : second

            dmhs/dt = (mhs_inf - mhs) / tau_mhs : 1
            mhs_inf = 1.0 / (1.0 + exp((V / mV + 71.3) / 7.9)) : 1
            tau_mhs = 5.6 / (exp((V / mV - 1.7) / 14.0) + exp(-(V / mV + 260.0) / 43.0) + 1.0) * ms : second
            '''
        # neuron_eqs = '\n'.join(shared_params + params + eqs)
        neuron_eqs = shared_params + params + eqs
        super(AckerNeuronGroup, self).__init__(
            N, neuron_eqs, threshold='V>Vth', refractory='V>Vth', method='rk4')
        self.V = -65.0 * mV
        self.m = 0.0
        self.h = 0.0
        self.mNap = 0.0
        self.n = 0.0
        self.mKs = 0.0
        self.mhf = 0.0
        self.mhs = 0.0


class AddSTDPRecurrentSynapse(Synapses):
    def __init__(
            self, source, target, connect,
            tau_rec = 5.0 * ms,
            tau_LTP = 17.0 * ms,
            tau_LTD = 34.0 * ms,
            A_LTP = 1.0,
            A_LTD = -0.6,
            eta = 0.05,
            sigma = 0.6,
            w_ini = 0.2
        ):
        self._initEquations()
        super(AddSTDPRecurrentSynapse, self).__init__(
            source, target, method='rk4',
            model=self.model_eqs,
            on_pre=self.pre_eqs,
            on_post=self.post_eqs)
        self.connect(connect)
        self.tau_rec = tau_rec
        self.tau_LTP = tau_LTP
        self.tau_LTD = tau_LTD
        self.A_LTP = A_LTP
        self.A_LTD = A_LTD
        self.eta = eta
        self.sigma = sigma
        self.w = w_ini
        self.pre.order = 1
        self.post.order = -1

    def _initEquations(self):
        self.model_eqs = '''
            tau_rec : second
            tau_LTP : second
            tau_LTD : second
            A_LTP : 1
            A_LTD : 1
            eta : 1
            sigma : 1
            w : 1
            wtot_post = w : 1 (summed)
            g_rec_post = w * s_rec : 1 (summed)
            ds_rec/dt = -s_rec / tau_rec : 1 (clock-driven)
            dLTP/dt = -LTP / tau_LTP : 1 (event-driven)
            dLTD/dt = -LTD / tau_LTD : 1 (event-driven)
            '''
        self.pre_eqs = '''
            dw_LTD = eta * (1.0 + sigma * randn()) * LTD
            w = clip(w + dw_LTD, 0.0, 1.0)
            s_rec += 1
            LTP += A_LTP
            '''
        self.post_eqs = '''
            dw_LTP = eta * (1.0 + sigma * randn()) * LTP
            w = clip(w + dw_LTP, 0.0, 1.0)
            LTD += A_LTD
            '''


class MultiSTDPRecurrentSynapse(Synapses):
    def __init__(
            self, source, target, connect,
            tau_rec = 5.0 * ms,
            tau_LTP = 17.0 * ms,
            tau_LTD = 34.0 * ms,
            A_LTP = 1.0,
            A_LTD = -1.65,
            eta = 0.05,
            sigma = 0.6,
            w0 = 0.25,
            w_ini = 0.2
        ):
        self._initEquations()
        super(MultiSTDPRecurrentSynapse, self).__init__(
            source, target, method='rk4',
            model=self.model_eqs,
            on_pre=self.pre_eqs,
            on_post=self.post_eqs)
        self.connect(connect)
        self.tau_rec = tau_rec
        self.tau_LTP = tau_LTP
        self.tau_LTD = tau_LTD
        self.A_LTP = A_LTP
        self.A_LTD = A_LTD
        self.eta = eta
        self.sigma = sigma
        self.w0 = w0
        self.w = w_ini
        self.pre.order = 1
        self.post.order = -1

    def _initEquations(self):
        self.model_eqs = '''
            tau_rec : second
            tau_LTP : second
            tau_LTD : second
            A_LTP : 1
            A_LTD : 1
            eta : 1
            sigma : 1
            w0 : 1
            w : 1
            wtot_post = w : 1 (summed)
            g_rec_post = w * s_rec : 1 (summed)
            ds_rec/dt = -s_rec / tau_rec : 1 (clock-driven)
            dLTP/dt = -LTP / tau_LTP : 1 (event-driven)
            dLTD/dt = -LTD / tau_LTD : 1 (event-driven)
        '''
        self.pre_eqs = '''
            dw_LTD = eta * (1.0 + sigma * randn()) * LTD
            w = clip(w + dw_LTD, 0.0, inf)
            s_rec += 1
            LTP += A_LTP
        '''
        self.post_eqs = '''
            dw_LTP = eta * (1.0 + sigma * randn()) * LTP
            w = clip(w + dw_LTP, 0.0, inf)
            LTD += A_LTD * w / w0
        '''


class LogSTDPRecurrentSynapse(Synapses):
    def __init__(
            self, source, target, connect,
            tau_rec = 5.0 * ms,
            tau_LTP = 17.0 * ms,
            tau_LTD = 34.0 * ms,
            A_LTP = 1.0,
            A_LTD = -0.5,
            eta = 0.05,
            sigma = 0.6,
            alpha = 5,
            beta = 50,
            w0 = 0.25,
            w_ini = 0.2
        ):
        self._initEquations()
        super(LogSTDPRecurrentSynapse, self).__init__(
            source, target, method='rk4',
            model=self.model_eqs,
            on_pre=self.pre_eqs,
            on_post=self.post_eqs)
        self.connect(connect)
        self.tau_rec = tau_rec
        self.tau_LTP = tau_LTP
        self.tau_LTD = tau_LTD
        self.A_LTP = A_LTP
        self.A_LTD = A_LTD
        self.eta = eta
        self.sigma = sigma
        self.alpha = alpha
        self.beta = beta
        self.w0 = w0
        self.w = w_ini
        self.pre.order = 1
        self.post.order = -1

    def _initEquations(self):
        self.model_eqs = '''
            tau_rec : second
            tau_LTP : second
            tau_LTD : second
            A_LTP : 1
            A_LTD : 1
            eta : 1
            sigma : 1
            alpha : 1
            beta : 1
            w0 : 1
            w : 1
            wtot_post = w : 1 (summed)
            g_rec_post = w * s_rec : 1 (summed)
            ds_rec/dt = -s_rec / tau_rec : 1 (clock-driven)
            dLTP/dt = -LTP / tau_LTP : 1 (event-driven)
            dLTD/dt = -LTD / tau_LTD : 1 (event-driven)
        '''
        self.pre_eqs = '''
            dw_LTD = eta * (1.0 + sigma * randn()) * LTD
            w = clip(w + dw_LTD, 0.0, inf)
            s_rec += 1
            LTP += A_LTP * exp(-w / (w0 * beta))
        '''
        self.post_eqs = '''
            dw_LTP = eta * (1.0 + sigma * randn()) * LTP
            w = clip(w + dw_LTP, 0.0, inf)
            LTD += A_LTD * (w / w0) * (w <= w0) + A_LTD * (1.0 + log(1.0 + alpha * (w / w0 - 1.0)) / alpha) * (w > w0)
        '''
