# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 16:19:21 2022

@author: scaje

 This code defines 2 ODE functions for the concentration of pathogen:
1) A transient concentration of pathogen model, within an 
    Suscpetible-Exposed SE model. 
    
    This includes an ODE for:
        - Transient Concentration
        - Suscpetible
        - Exposed
        - Cummulative Dose Received 
        
        
2) A steady state concentration of pathogen model, within an SE model.
        This includes an equation for steady state concentration with an 
        ODE for:
        - Suscpetible
        - Exposed

        
Note both functions use the inclusion of various free parameters:
    n - is the number of zones
    I_zonal - a vector of infected individuals in each zone
    v_zonal - a vector of the volume of each zone (m^3)
    p_zonal - a vector of the pulmonary rate of each zone (m^3/min)
    q_zonal - a vector of quanta production rate per zone (quanta/min)
    t - is the time period of model
    
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