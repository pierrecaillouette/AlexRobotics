# -*- coding: utf-8 -*-
"""
Created on 19/11/2019

@author: Pierre
"""
###############################################################################
import numpy as np
###############################################################################
from pyro.dynamic import pendulum
from pyro.control import nonlinear
###############################################################################

sys = pendulum.SinglePendulum()
ctl = nonlinear.AdaptativeController(sys)

sys.m1 = 1

ctl.A[0] = 0
ctl.A[1] = 0

ctl.Kd = 1
ctl.lam = 1
ctl.T[0,0] = 10
ctl.T[1,1] = 10
# Set Point
q_target = np.array([3.14])
ctl.rbar = q_target

# New cl-dynamic
cl_sys = ctl + sys
#cl_sys = sys

# Simultation
x_start  = np.array([0,1])
tf = 10
n  = tf * 1000 + 1
cl_sys.plot_trajectory( x_start , tf , n, 'euler')
cl_sys.sim.phase_plane_trajectory(0,1)
cl_sys.animate_simulation()