# -*- coding: utf-8 -*-
"""

@author: scaje


This script is used as part of the study entitled "Assessing the effects of transient weather conditions on 
airborne transmission risk in naturally ventilated hospitals."; 
Alexander J. Edwards, Marco-Felipe King,  Martin Lopez-Garcia, Daniel Peckham, Catherine J. Noakes.".
The user should refer to the README file in the GitHub repository for a description on its use.

Created 25/01/2023 AJE

"""

import numpy as np
import scipy as sp
from IzFlows_AJE import boundary_flow_contam #imports boundary flow function which uses cintam results to define them 
from Extract_AJE import extract_flow_contam #this import the function which changes the extract ventiatlion in each zonebased on output from contam simulation



##############################################################################
############################## ZONAL SETUP ###################################
##############################################################################

#number of zones n
n=12

##############################################################################
############################## geometry matrix SETUP #########################
##############################################################################
""" the aim of this nxn matrix, geometry(nxn), is to characterise the geometry
 and so if zone i is connected to zone j then entry geometry[i,j]=1,
 if zone i is not connected to zone j then geometry[1,j]=0."""
 
#defined in such away that input should be [i,j] where i<j
geometry=np.zeros((n,n))
geometry[0,5]=1
geometry[1,7]=1
geometry[2,4]=1
geometry[3,4]=1
geometry[4,6]=1
geometry[5,6]=1
geometry[6,7]=1
geometry[6,8]=1
geometry[6,9]=1
geometry[7,10]=1
geometry[7,11]=1




for i in range(n):
    for j in range(n):    
        geometry[j,i] = geometry[i,j]

print("geometry matric geometry" +str(geometry))

##############################################################################
#Zonal volumes
v_zonal = np.zeros(n)

v_zonal[0]=98.35
v_zonal[1]=98.35
v_zonal[2]=28.57
v_zonal[3]=28.57
v_zonal[4]=36.35
v_zonal[5]=31.74
v_zonal[6]=31.74
v_zonal[7]=31.74
v_zonal[8]=47.24
v_zonal[9]=50.46
v_zonal[10]=43.42
v_zonal[11]=46.94


##########################################################################

#number of people in each zone is not the same due to scenario

K_zonal = np.zeros(n)

K_zonal[0]=4
K_zonal[1]=4
K_zonal[2]=1
K_zonal[3]=1
K_zonal[4]=1
K_zonal[5]=0
K_zonal[6]=0
K_zonal[7]=0
K_zonal[8]=0
K_zonal[9]=3
K_zonal[10]=2
K_zonal[11]=1


###########################################################################
def VentilationMatrix(n, t, geometry, filepath):
    
    
    #define boundary flow matrix from boundary flow contam func
    boundary_flow = boundary_flow_contam(filepath, n, t, geometry)
    
    #DEFINE EXTRACT VENTIALTION VECTOR FROM CONTAM FLOWS FUNC
    extract_flow = extract_flow_contam(filepath, n, t, geometry)
    
    
    #VENTILATION MATRIX
    V_zonal = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i==j:
                V_zonal[i,i] = extract_flow[i]
            
                for k in range(n):
                    if geometry[i,k] > 0:
                        
                        V_zonal[i,i] = V_zonal[i,i] + boundary_flow[i,k]
                    else:
                        V_zonal[i,i] = V_zonal[i,i]
                    
                    
            else:
                if geometry[i,j]>0:
                        
                    V_zonal[i,j] = - boundary_flow[j,i]
                else:
                    V_zonal[i,j] = 0
                
    print("Ventilation Matrix V = " + str(V_zonal))   
    print("BOUNDARY FLOW" +str(boundary_flow))
    
    
    return V_zonal




def InvVentilationMatrix(V_zonal):
    
    
    #calculate inverse of ventiation matrix for steady state calculation
    V_zonal_inv = sp.linalg.inv(V_zonal)
    print("Inverse Ventilation Matrix V = " + str(V_zonal_inv))
    
    return V_zonal_inv
###########################################################################