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
REC1_N = 20
REC2_N = 50

profile_name = 'synamat'

a = 2.0 * uA
gmax_rec = 0.010 * msiemens
period = 100

trials = range(1)
jitters = [-2] * ms
FLUCs = range(400000, 500000, 100000) * (uA**2 / ms)
freqs = range(40, 50, 10) * Hz
