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
METHOD = 'rk4'
STDP = 'add'

MODE = 'Ih'

profile_root = './test1/'

a = 2.0 * uA
gmax_rec = 0.010 * msiemens

period = 10
jitter = -2 * ms
FLUC = 100000 * (uA**2 / ms)
freq = 50 * Hz

if STDP == 'add':
    TAU_REC = 5.0 * ms
    TAU_LTP = 17.0 * ms
    TAU_LTD = 34.0 * ms
    A_LTP_ = 1.0
    A_LTD_ = -0.6
    ETA = 0.05
    SIGMA = 0.6
elif STDP == 'mlt':
    TAU_REC = 5.0 * ms
    TAU_LTP = 17.0 * ms
    TAU_LTD = 34.0 * ms
    A_LTP_ = 1.0
    A_LTD_ = -1.65
    ETA = 0.05
    SIGMA = 0.6
    W0 = 0.25
elif STDP == 'log':
    TAU_REC = 5.0 * ms
    TAU_LTP = 17.0 * ms
    TAU_LTD = 34.0 * ms
    A_LTP_ = 1.0
    A_LTD_ = -0.5
    ETA = 0.05
    SIGMA = 0.6
    ALPHA = 5
    BETA = 50
    W0 = 0.25
