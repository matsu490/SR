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

period = 15
jitter = -2 * ms
FLUC = 100000 * (uA**2 / ms)
freq = 50 * Hz
