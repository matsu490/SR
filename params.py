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
REC1_N = 50
REC2_N = 50

profile_name = 'test'

a = 2.0 * uA
gmax_rec = 0.010 * msiemens
period = 5

jitters = [-2] * ms
FLUCs = range(0, 400000, 100000) * (uA**2 / ms)
freqs = range(10, 50, 10) * Hz
