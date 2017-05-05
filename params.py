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

profile_name = 'test2'

a = 2.0 * uA
gmax_rec = 0.010 * msiemens

period = 5
jitter = -2 * ms
FLUC = 100000 * (uA**2 / ms)
freq = 50 * Hz
