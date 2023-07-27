# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 16:19:21 2022

@author: scaje


This script is used as part of the study entitled "Assessing the effects of transient weather conditions on 
airborne transmission risk in naturally ventilated hospitals."; 
Alexander J. Edwards, Marco-Felipe King,  Martin Lopez-Garcia, Daniel Peckham, Catherine J. Noakes.".
The user should refer to the README file in the GitHub repository for a description on its use.
    
AJE
    """
    
import numpy as np





def odes(X, t, n, V_zonal, I_zonal, q_zonal, p_zonal, v_zonal):
    C = X[0:n]
    S = X[n:2*n]
    E = X[2*n:3*n]
    D = X[3*n:]
    
    
    dCdt = q_zonal*I_zonal/v_zonal - np.matmul(V_zonal, C) / v_zonal # concentration
 #   dCdt -= np.matmul(V_zonal, C) / v_zonal
    
    dSdt = -p_zonal * C * S #susceptible
    dEdt = p_zonal * C * S #exposed
    
    dDdt = p_zonal * C #dose received

    dXdt = np.hstack( (dCdt, dSdt, dEdt, dDdt) )
    return dXdt




def steadyodes(Xstar, t, n, V_zonal_inv, I_zonal, q_zonal, p_zonal, v_zonal):
    
    Cstar = np.matmul(V_zonal_inv, I_zonal) * q_zonal
    
    Sstar = Xstar[0:n]
    Estar = Xstar[n:]
    
    dSstardt = -p_zonal * Cstar * Sstar
    dEstardt = p_zonal * Cstar * Sstar
    
    dXstardt = np.hstack((dSstardt, dEstardt))
    return dXstardt