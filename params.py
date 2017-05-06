# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2017-03-23
#
# Copyright (C) 2017 Taishi Matsumura
#
from brian2.units import *

DT = 0.01 * ms
MODE = 'Ih'
STDP = 'add'
STIM_N = 20
REC1_N = 100
REC2_N = 100

profile_name = 'test'

a = 2.0 * uA
gmax_rec = 0.010 * msiemens
period = 500

trials = range(1)
jitters = [-2] * ms
FLUCs = range(100000, 200000, 100000) * (uA**2 / ms)
FLUCs = [0, 100000, 400000] * (uA**2 / ms)
freqs = range(40, 60, 10) * Hz
