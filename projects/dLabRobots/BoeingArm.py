# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 10:10:34 2016

@author: agirard
"""

from AlexRobotics.dynamic  import Hybrid_Manipulator   as HM

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d



class BoeingArm( HM.HybridThreeLinkManipulator ) :
    """ 3DOF Manipulator Class """
    
    
    ############################
    def __init__(self, n = 6 , m = 4 ):
        
        HM.HybridThreeLinkManipulator.__init__(self, n , m )
        
        # Create interpol function
        self.compute_q0_fwd_kinematic()
        
        # Ploting param
        self.n_pts   = 8 # number of pts to plot on the manipulator 
        self.dim_pts = 3 # number of dimension for each pts 
        self.axis_to_plot = [0,2]  # axis to plot for 2D plot
        
        
    #############################
    def setparams(self):
        """ Set model parameters here """
        
        # First link kinematic
        b0  = 0.5  # 2x2 tubing length
        b1  = 0.2  # pivot distance from 2x2 tubing base
        b2  = 0.1  # pivot height from 2x2 tubing mid-line
        b3  = 0.25  # rod length
        b4  = 0.1  # pivot height from ballscrew line
        b5  = 0.4  # total length of ballscrew
        b6  = np.sqrt( b1 **2 + b2 **2 )  # distance between pivots on main tube
        b7  = np.arctan( b2 / b1 )         # angle difference between 
        self.b = np.array([ b0 , b1 , b2 , b3 , b4 , b5 , b6 , b7])
        
        
        self.lw = 1
        
        
        # Dynamics
        
        # actuator viscous damping coef
        self.d1 = 1
        self.d2 = 1
        self.d3 = 1
        
        
    ############################
    def q0_inv_kinematic(self, theta_0 = 0 ):
        """ 
        Inverse kinematic of first DOF 
        -----------------------------
        theta_0 : angle of 2x2 tube w/ vertical [rad]
        q0      : linear displacement of ballscew nut from zero-position
        
        """
        # see alex logbook for figure and variable def:
        
        theta_3 = self.b[7] - theta_0   # angle offset
        
        s3 = np.sin( theta_3 )
        c3 = np.cos( theta_3 )
        
        l3 = self.b[6]
        l2 = self.b[3]
        h1 = self.b[4]
        
        l1 = l3 * s3 + np.sqrt( l2 **2 - ( l3 * c3 - h1) **2 )
        
        q0 = self.b[5] - l1
        
        return q0
        
        
    ############################
    def compute_q0_fwd_kinematic( self , plot = False  ):
        """ 
        Create and interpol function for fwd kinematic 
        -----------------------------------------------
        Data validated using solidworks sketch tools
        
        """
        
        # Create data
        
        angles = np.arange( -np.pi * 0.3 , np.pi * 0.8 , 0.01)
        linear = np.zeros( angles.size )
        
        # Inv kinematic
        for i in range( angles.size ):
            linear[i] = self.q0_inv_kinematic( angles[i] )
            
        self.theta0_fwd_kinematic = interp1d( linear , angles )
        # theta_0 = self.q0_fwd_kinematic( q0 )
        
        if plot:
            # For validation
            
            linear_approx = np.arange( 0 , 0.41 , 0.01)
            angles_approx = np.zeros( linear_approx.size )
            
            for i in range( linear_approx.size ):
                angles_approx[i] = self.theta0_fwd_kinematic( linear_approx[i] )
            
            fig , plot = plt.subplots( 1 , sharex=True , figsize=(4, 3), dpi=300, frameon=True)
            fig.canvas.set_window_title('First Link kinematic')
            plt.plot( linear, angles * 180 / np.pi , 'b-')
            plt.plot( linear_approx, angles_approx * 180 / np.pi , 'r-')
            plot.set_xlabel( 'Linear displacement [meter]' , fontsize=5)
            plot.set_ylabel( 'Angle 0 [deg]' , fontsize=5)
            plot.grid(True)
            fig.tight_layout()
        
        
    ##############################
    def trig(self, q = np.zeros(3) ):
        """ Compute cos and sin """
        
        theta_0 = self.theta0_fwd_kinematic( q[0] )
        s0 = np.sin( theta_0 )
        c0 = np.cos( theta_0 )
        
        theta_3 = self.b[7] - theta_0
        s3 = np.sin( theta_3 )
        c3 = np.cos( theta_3 )
        
        theta_2 = np.arcsin( (self.b[6] * c3 - self.b[4] ) / self.b[3] )
        s2 = np.sin( theta_2 )
        c2 = np.cos( theta_2 )
        
        
        base  = [ theta_0 , s0 , c0 , theta_2 , s2 , c2 , theta_3, s3 , c3 ]
        link1 = []
        link2 = []
        
        
        return [base,link1,link2]
        
        
    ##############################
    def fwd_kinematic(self, q = np.zeros(3) ):
        """ Compute [x;y;z] positions of points of interest given angles q """
        
        ### First DOF ### 
        [base,link1,link2] = self.trig( q )
        
        p0 = [ -self.b[5] , 0 , 0 ]
        p1 = [ 0, 0, 0 ]                      # Base of 2x2 beam
        p2 = [ q[0] - self.b[5] , 0 , 0 ]
        p3 = [ q[0] - self.b[5] , 0 , self.b[4] ]
        
        [ theta_0 , s0 , c0 , theta_2 , s2 , c2 , theta_3, s3 , c3 ] = base
        
        p4 = [ q[0] - self.b[5] + self.b[3] * c2 , 0 , self.b[4] + self.b[3] * s2 ]
        p5 = [ self.b[1] * s0 , 0 , self.b[1] * c0 ]
        p6 = [ 0 , 0 , 0 ]
        p7 = [ self.b[0] * s0 , 0 , self.b[0] * c0 ]
        
        ### Seconde DOF ###
        #TODO
        
        
        return np.array([p0,p1,p2,p3,p4,p5,p6,p7])
        
                    
    ##############################
    def jacobian_endeffector(self, q = np.zeros(3)):
        """ Compute jacobian of end-effector """
                
        J = np.zeros((3,3))
        #TODO
        
        return J
        
        
    ##############################
    def jacobian_q0_theta0(self, q = np.zeros(3)):
        """ 
        Compute jacobian of link0 angular velocity (theta_0)  vs. linear actuator velocity (q[0])
        
        units = [meter/rad]
        
        validated by looking at the gradient of the integral function
        
        """
        
        [base,link1,link2] = self.trig( q )
        
        [ theta_0 , s0 , c0 , theta_2 , s2 , c2 , theta_3, s3 , c3 ] = base
                
        l3 = self.b[6]
        l2 = self.b[3]
        h1 = self.b[4]
        
        alpha = l3*c3 - h1
        beta  = l2 ** 2 - alpha **2
        
        j     = l3 * c3 + alpha * l3 * s3 / np.sqrt( beta )
        
        return j
        
        
        
        
    ##############################
    def H(self, q = np.zeros(3)):
        """ Inertia matrix """  
        
        H = np.eye(3)
        
        # TODO        
        
        return H
        
        
    ##############################
    def C(self, q = np.zeros(3) ,  dq = np.zeros(3) ):
        """ Corriolis Matrix """ 
                        
        C = np.zeros((3,3))
        #TODO
        
        return C
        
        
    ##############################
    def D(self, q = np.zeros(3) ,  dq = np.zeros(3) ):
        """ Damping Matrix """  
               
        D = np.zeros((3,3))
        
        D[0,0] = self.d1
        D[1,1] = self.d2
        D[2,2] = self.d3
        
        return D
        
        
    ##############################
    def G(self, q = np.zeros(2) ):
        """Gravity forces """  
        
        #TODO
        
        G = np.zeros(3)
        
        return G
        
        
    ##############################
    def e_potential(self, q = np.zeros(2) ):
        """ Compute potential energy of manipulator """  
               
        e_p = 0
        
        # TODO
        
        return e_p
        
        
        
        

        





'''
#################################################################
##################          Main                         ########
#################################################################
'''


if __name__ == "__main__":     
    """ MAIN TEST """
    
    R = BoeingArm()
    
    x0 = np.array([0,0,0,0.3,0,0])
    
    R.plot3DAnimation( x0 )
