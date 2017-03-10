# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 13:56:13 2016

@author: agirard
"""


#################################################################################################################

from AlexRobotics.dynamic  import Hybrid_Manipulator   as HM
import numpy as np


class SingleRevoluteDSDM( HM.HybridOneLinkManipulator ) :
    """  """

    ############################
    def __init__(self):
        
        HM.HybridOneLinkManipulator.__init__(self )
        
        self.ubar = np.array([0,474])
        
        self.x_ub = np.array([ + 1 * np.pi ,  15 ])
        self.x_lb = np.array([ - 2 * np.pi , -15 ])
        self.u_ub = np.array([ + 0.5 ,  500 ])
        self.u_lb = np.array([ - 0.5 ,  0   ])
        
        # High-force Max speed
        self.dq_max_HF = 0.9 # [rad/sec]
        
        self.ext_cst_force = 0
        
        self.setparams()
        
    #############################
    def isavalidinput(self , x , u):
        """ check if u is in the domain """
        
        ans = False # set to True if something is bad
        
        for i in xrange(self.m):
            ans = ans or ( u[i] < self.u_lb[i] )
            ans = ans or ( u[i] > self.u_ub[i] )
            
        # add w_max constraint
        
        # if High-force mode
        if u[1] == self.R[1] :
            
            dq = x[1]
            
            ans = ans or ( dq >  self.dq_max_HF )
            ans = ans or ( dq < -self.dq_max_HF )

            
        return not(ans)
        
        
    #############################
    def setparams(self):
        """ Set model parameters here """
        
        self.l1  = 0.25
        self.lc1 = 0.1
        
        self.m1 = 0.0 # Neglect
        self.I1 = 0.0 # Neglect
        
        # load
        self.M  = 1.0
        
        self.g = 9.81 * 1
        
        self.d1 = 0.05
        
        # Total length
        self.lw = 0.3
        
        self.setActuatorParams()
        
    #############################
    def setActuatorParams(self ):
        """ Set actuators parameters here """
        
        # Actuator damping coef
        self.Da = np.diag( [ 0.00002 ] ) * 0.1
        
        # Actuator inertia coef
        
        I_m = 15 # gcm2
        
        self.Ia = np.diag( [ I_m ] ) * 0.001 * ( 0.01 **2 )
        
        # Gear ratio
        r1   = 23.2 # 5.8 * 4
        r2   = 474  # 123 * 52/18 *4/3
        
        self.R = [ r1 , r2 ]
        
    
    ##############################
    def F_ext(self, q , dq  ):
        """ """        
        return self.ext_cst_force 
        


'''
#################################################################
##################          Main                         ########
#################################################################
'''


if __name__ == "__main__":     
    """ MAIN TEST """
    
    R = SingleRevoluteDSDM()
    
    R.ext_cst_force = 0
    
    R.plotAnimation([3.14,0])