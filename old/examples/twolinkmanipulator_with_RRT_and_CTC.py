# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 15:27:04 2016

@author: alex
"""

from AlexRobotics.planning import RandomTree     as RPRT
from AlexRobotics.dynamic  import Manipulator    as M
from AlexRobotics.control  import ComputedTorque as CTC

import numpy as np
import matplotlib.pyplot as plt

""" Define system """

R  =  M.TwoLinkManipulator()

x_start = np.array([3,0,0,0])
x_goal  = np.array([0,0,0,0])

RRT = RPRT.RRT( R , x_start )

T = 12 # torque

RRT.U = np.array([[T,0],[0,0],[-T,0],[0,T],[0,-T],[T,T],[-T,-T],[-T,T],[T,-T]])

RRT.dt                    = 0.1
RRT.goal_radius           = 0.8
RRT.max_nodes             = 12000
RRT.max_solution_time     = 8

#RRT.compute_steps(1000,True)
RRT.find_path_to_goal( x_goal )

# Assign controller
CTC_controller     = CTC.ComputedTorqueController( R )
CTC_controller.load_trajectory( RRT.solution )
R.ctl              = CTC_controller.ctl

CTC_controller.w0           = 1.0
CTC_controller.zeta         = 0.7
CTC_controller.traj_ref_pts = 'closest'
#CTC_controller.traj_ref_pts = 'interpol'

#R.ctl = RRT.trajectory_controller
#RRT.traj_ctl_kp   = 25
#RRT.traj_ctl_kd   = 10

""" Simulation and plotting """

# Plot
tf = RRT.time_to_goal + 5
n  = int( np.round( tf / 0.05 ) ) + 1
R.plotAnimation( x_start , tf  , n , solver = 'euler' )
R.Sim.plot_CL('x') 
R.Sim.plot_CL('u')
#R.phase_plane_trajectory([0,0],x_start,tf,True,True,True,True)
RRT.plot_2D_Tree()

# Hold figures alive
#plt.show()