# -*- coding: utf-8 -*-
"""

@author: scaje

This code sets out the setup for a 10 zone hospital ward with homogeneous mixing with 
the geometry taken as a subset of J12 st James's adult respiratory ward with 
the zones defined as
Zone 1 = Bay 1 - Volume= 98.35m^3  
Zone 2 = Bay 2  -  Volume= 98.35m^3
Zone 3 = Single Room 1  -  Volume=   28.57m^3
Zone 4 = Single Room 2  -  Volume= 28.57m^3  
Zone 5 = Nurse Room 1  -  Volume= 36.35m^3  
Zone 6 = Corridor 1  -  Volume= 31.74m^3   
Zone 7 = Corridor 2  -  Volume= 31.73m^3
Zone 8 = Corridor 3  -  Volume= 31.74m^3
Zone 9 = Sluice 1 ( a contamintaion room) Volume= 47.24m^3   
Zone 10 = Nurse Room 2 (staff room) Volume= 50.46m^3  
Zone 11 = Clinic room 1 Volume= 43.42m^3   
Zone 12 = Doctors office 1 Volume= 46.94m^3  

total ward volume=573.41

This code is designed to be imported into working code to save on working lines
and improve code efficiency and clarity. 

This file is set up to deal with imported boundary flows from the results of a contam simulation.
This fuction is called with the ventilation matrix function.

Please find a pdf illustrating the zonal and ventialtion setup in the same folder
as this funtcion. 


Created 15/03/2023 AJE

"""

from read_csv import ReadCSV
import numpy as np
import scipy as sp
from contam_wth_IzFlows_12zone import boundary_flow_contam #imports boundary flow function which uses cintam results to define them 
from contam_wth_Extract_MV_12z import extract_flow_contam #this import the function which changes the extract ventiatlion in each zonebased on output from contam simulation


##############################################################################
##############################################################################
############################## ZONAL SETUP ###################################
##############################################################################
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
#Zonal volumes little v
v_zonal = np.zeros(n)
#for when volume is the same in each room
#for i in range(n):
#    v_zonal[i] = V
#If volumes are different
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

#   .
#   .
#   .
#v_zonal[n]= 
print("volume v_zonal = " + str(v_zonal))
##########################################################################

#number of people in each zone is not the same due to scenario

K_zonal = np.zeros(n)
#for i in range(n):
#    K_zonal[i]=10
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


# ZONE 5 - Nurse station includes 6 susceptibles and 1 infector
#zones 1-4 are fixed bays with patients in beds
##############################################################################
###########################################################################
#EXTRACT VENTILATION IS NOW IMPORTED
# =============================================================================
# #zonal ventialtion rate
# Q_zonal = np.zeros(n)
# #for when ventilation rate is same in each zone
# #for i in range(n):
# #    Q_zonal[i] = 3 # ventilation rate is the same in each zone 
# 
# #if ventilation rates are different
# #NOTE: Q_zonal[i] cannot equal zero for all i, this will cause singular matrix
# #for ventilation rates <1 the inverse matrix solver is unstable so need to find alternative route
# 
# Q_zonal[0]=4.91 #for 3ach= 4.91 #for1.5ach = 2.45 for 0.5ach = 0.81 #for 6ACH=9.82
# Q_zonal[1]=4.91 #for 3ach=4.91 #for1.5ach = 2.45 for 0.5ach = 0.81 #for 6ACH=9.82
# Q_zonal[2]=1.42 #for 3ach=1.42 #for1.5ach = 0.71 for 0.5ach = 0.23 #for 6ACH=2.84
# Q_zonal[3]=1.42 #for 3ach=1.42 #for1.5ach = 0.71 for 0.5ach = 0.23 #for 6ACH=2.84
# Q_zonal[4]=1.81 #for 3ach=1.81 #for1.5ach = 0.9 for 0.5ach = 0.3 #for 6ACH=3.62
# Q_zonal[5]=1.59 #for 3ach=1.59 #for1.5ach = 0.795 for 0.5ach =0.265  #for 6ACH=3.18
# Q_zonal[6]=1.59 #for 3ach=1.59 #for1.5ach = 0.795 for 0.5ach =0.265  #for 6ACH=3.18
# Q_zonal[7]=1.59#for 3ach=1.59 #for1.5ach = 0.795 for 0.5ach =0.265  #for 6ACH=3.18
# Q_zonal[8]=2.36 #for 3ach=2.36 #for1.5ach = 1.18 for 0.5ach = 0.4 #for 6ACH=4.72
# Q_zonal[9]=2.52 #for 3ach=2.52 #for1.5ach = 1.26 for 0.5ach = 0.42 #for 6ACH=5.04
# Q_zonal[10]=2.17 #for 3ach=2.17 #for1.5ach = 1.08 for 0.5ach = 0.36 #for 6ACH=4.34
# Q_zonal[11]=2.32 #for 3ach=2.32 #for1.5ach = 1.16 for 0.5ach = 0.39 #for 6ACH=4.64
# 
# #add more for more zones, currently for 3 zones
# print("ventialtion Q_zonal =" + str(Q_zonal))
# =============================================================================
###########################################################################

#BOUNDARY FLOW IS IMPORTED

#boundary_flow = 

#print("flow from zone i to zone k BOUNDARY_FLOW =" + str(boundary_flow))








###########################################################################
def VentilationMatrix(n, t, geometry, filepath, filepathMV):
    
    
    #define boundary flow matrix from boundary flow contam func
    boundary_flow = boundary_flow_contam(filepath, n, t, geometry)
    
    #DEFINE EXTRACT VENTIALTION VECTOR FROM CONTAM FLOWS FUNC
    extract_flow = extract_flow_contam(filepath, n, t, geometry,filepathMV)
    
    
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