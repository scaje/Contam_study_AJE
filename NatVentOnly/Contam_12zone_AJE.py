# -*- coding: utf-8 -*-
"""
@author: scaje
 This code aims to solve for concentration of pathogen in the air and 
the SE epidemic model for a n zone hopsital ward (layout defined in geometry 
                                                  matrix)

This is based on a CONTAM weather study where we model transient weather effects,
and how they affect the concentration levels. Originally designed for HB23.
The code calls on functions previously defined for the concentration and 
epidemic model. 

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



Ventilation setting for a 12zone ward homogeous case is imported and represents
 the setup for an exact recreation of the J12 subsection for 12zones which were 
 modelled in contam and the boundary flows and extract ventialtion have been extracted.


User must define infected individuals and coresponding zone and any time
periods or zones which the infectors move to below.

Created 25/01/2023 AJE
"""


import matplotlib.pyplot as plt
import random, math
import numpy as np
from scipy.integrate import odeint #for solving odes
import matplotlib.colors as mcolors #colour name package
from matplotlib.pyplot import cm #colour map package
from pywaffle import Waffle #visual package for visuallising icons
import time #for live run time of code
import J12_12z_contam_wth_ventflows as VentMatrix #imports setup for 6 zone ward ventilaton setting from another file where it is already defined
from J12_12z_contam_wth_ventflows import VentilationMatrix #import function which defines ventilation matrix
from J12_12z_contam_wth_ventflows import InvVentilationMatrix #imports function which defines inverse ventilation matrix
from SE_Concentration_Functions import odes #imports predefined SE ode functions for transient concentration
from SE_Concentration_Functions import steadyodes ##imports predefined SE ode functions for steady concentration
from output_contam import output_SE_Ct #This imports the plotting ode for all possible outputs for multizonal transient concentreation SE model
from contam_wth_IzFlows_12zone import boundary_flow_contam #this import the function which changes the boundary flow values based on output from contam simulation
from contam_wth_Extract_12zone import extract_flow_contam #this import the function which changes the extract ventiatlion in each zonebased on output from contam simulation
import pandas as pd

# To run the code, one needs to define the initial parameters below and then 
#define the setup matrices for each specific zone. A time period and timestep needs to be defined
#and then the transient concentrations can be solved and the graphs can be produced. 

#before running the code, itial conditions for the epidemic model also need to be defined.
#These can be found after the ode definition function.


start_time = time.time() #time code started running
############################################################################
#Initial values from other simulations for reference
########################################################
###########################Initial values###################################



#quanta rate = quanta/min . person (as 0.5 quanta per min)
q=0.5 #0.0166667=1qhr, 0.1666667=10qhr, 0.5=30qhr , 5qhr=0.083334
qhr = int(q*60)
#pulmonary rate = volume/min ( as 0.01volume/min)
p=0.01
#Ventilaation rate = volume/ min (taken as 27m^3/min)
#Q = 1620
Q=3 #3m^3 in each zone 
#volume of indoor space V m^3
V=60
#desired number of poeple in each of the zones
K=3


##############################################################################
##############################################################################
############################## ZONAL SETUP ###################################
##############################################################################

######################Run ventilation setting############################ 
n=12


#THE FILEPATH USED FOR THE RESULTS THROUGHOUT (change save directory at end)
filepath = r"C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Contam_models\wind_driven_flow_study\J12_12zone\Increased_leakage\Exported_results\IZFlows.csv"

#different file paths for each contam simulation
#Windows closed - r"C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\St_James_ward_info\CONTAM_Model_Zeyu\Contam_data\Windows_closed.csv"
#windows open - r"C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\St_James_ward_info\CONTAM_Model_Zeyu\Contam_data\Windows_open.csv"
#windows open when infHCW present - r"C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\St_James_ward_info\CONTAM_Model_Zeyu\Contam_data\Windows_open_during_visit.csv"

#filepath for the flipped study investigating a 180 degree spin (remember to change the save directory at end)
#filepath = r"C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Contam_models\wind_driven_flow_study\J12_12zone\Orientation\Exported_results\IZFlows.csv"

###############################################################

#Pulmonary rate in each zone
p_zonal = np.zeros(n)
#for when  is the same in each room
for i in range(n):
    p_zonal[i] = p
#If volumes are different
#p_zonal[0]=
#p_zonal[1]=
#p_zonal[2]=
#   .
#   .
#   .
#p_zonal[n]=
print("Pulmonary rate p_zonal = " + str(p_zonal))
############################################################################

#Zonal quanta
q_zonal = np.zeros(n)
#for when  is the same in each room
for i in range(n):
    q_zonal[i] = q
#If volumes are different
#q_zonal[0]=
#q_zonal[1]=
#q_zonal[2]=
#   .
#   .
#   .
#q_zonal[n]=
print("quanta q_zonal = " + str(q_zonal))
############################################################################


 
#Zonal infections
#Zonal volumes little v
I_zonal = np.zeros(n)
#for when is the same in each room
#for i in range(n):
#    I_zonal[i] = I0
#If volumes are different
I_zonal[0]=0
I_zonal[1]=0
I_zonal[2]=0
I_zonal[3]=0
I_zonal[4]=1
I_zonal[5]=0

#   .
#   .
#   .
#I_zonal[n]= 
print("infections I_zonal = " + str(I_zonal))
##########################################################################

#############################################################################
#############################################################################
######################### DEFINE  Transient ODES #############################
#############################################################################


#################################################################



###########################################################################
################ Time and infector setup #############################
##############################################################################


#weather file timesteps in 1hr intervals, so sufficient to update IZ flows every 2hr is reasonable assumption
#183 days, gives  4392 hours, gives 263520 minutes...
#... time steps are 1 minute so total time steps in 263520
#For time periods of length 2hrs = 120 mins, this gives 2196 total time periods and so ...
#... the code will run 2196 times for full solution

#weather time steping in minutes
wth_delta_t=60 #1hr time stepping for weather file
update_t_len= 2*wth_delta_t #length of time for each period of solving before flow updates 
#total sim length Apr-Oct 214 days
sim_len_days = 183 #183 days for  Apr -End of Sept (oct) # 214 days for Apr-End of Oct 
sim_len_hrs = sim_len_days*24
sim_len_mins = sim_len_hrs*60

t = [] #initialise t
#define first time period
t_0 = np.linspace(0, update_t_len , update_t_len) #weather time step defined in minutes, we want steps in minutes also so keep same
t.append(t_0)#include first time period into t
for i in range((int(sim_len_hrs/2)) -1):#sim_len_hrs gives number of hours in sim, we divide by two as updating every 2 hrs not 1 so half as many steps
    t_i = np.linspace(t[i][-1], t[i][-1] + update_t_len, update_t_len)
    
    t.append(t_i) 
    

#infection vectors to correspon with scenario
I_zonal_t1 = I_zonal # for infector present in nurse station - Zone 5

###########################################################################
############################################################################
##############################################################################
#################################################################

#Loops below calculate the solution for transient infector over any specified time periods

###########################################
##############  Transient #################
###########################################

#looping solutions over different time periods for transient model
C0 = np.zeros(n) #inital concentration
E0 = np.zeros(n) #inital exposed
S0 = VentMatrix.K_zonal - I_zonal_t1 - E0 #inital suceptibles
D0 = np.zeros(n) #inital dose received
Ct = np.empty((0,n))
St = np.empty((0,n))
Et = np.empty((0,n))
Dt = np.empty((0,n))
#combining intial conditions
X0 = np.hstack( (C0, S0, E0, D0) )
print(X0)

for i in range(len(t)):
    

    V_zonal = VentilationMatrix(n, t[i], VentMatrix.geometry, filepath)
    print("V_zonal = " + str(V_zonal)) #print bounday flow to check its updating each step

    
    #solving
    x = odeint(odes, X0, t[i], args=(n, V_zonal, I_zonal_t1, q_zonal, p_zonal, VentMatrix.v_zonal)) #args=()
    
    #re-defining initial conditions
    C0 = x[:, 0:n]
    S0 = x[:, n:2*n]
    E0 = x[:, 2*n:3*n]
    D0 = x[:,3*n:]
    
    X0 = np.hstack( (C0[-1,:], S0[-1,:], E0[-1,:], D0[-1,:]) )
    print(X0)
    
    
    #storing results in a vector
    Ct = np.vstack((Ct, C0))
    St = np.vstack((St,S0))
    Et = np.vstack((Et,E0))
    Dt = np.vstack((Dt,D0))
    
    print("COUNT i =" +str(i))
    #End



###########################################################################
###########################################################################
####################### population values###################################

#Total population
N = K*n #K people in each zone
#transinet version
St_pop = np.sum(St, axis=1) #axis=1 does rows, axis=0 does columns
Et_pop = np.sum(Et, axis=1)
S0_pop = np.sum(S0)
E0_pop = np.sum(E0)
I0_pop = np.sum(I_zonal)




############################################################################
############################################################################
######################### Plotting #########################################
############################################################################
############################################################################

#define t for plotting 
#plotting in hours 
#t_hours = t/60

t_plot=np.empty((0,0))
for i in range(len(t)):#note range runs for number of time periods defined
    t_plot = np.append(t_plot,t[i]/(60*24*30.5)) #to make all times plottable in months not minutes (avg days in month=30.5)
    
#Define Colours array for plotting 
#cm is imported colour maps from matplotlib.pyplot library
#tab20 is selected color map palette
# n is number of different colours needed
#This has to be applied before each use
#colour = iter(cm.tab20(np.linspace(0, 1, n)))


############################################################################
############################################################################

#uses a predefined function to plot all of the required outputs for this model
output_SE_Ct(n, t_plot, Ct, Dt, St, Et, St_pop, Et_pop, I0_pop, start_time, sim_len_days)

print("V_zonal = " + str(V_zonal))
#print("V_zonal_inv = " + str(V_zonal_inv))


boundary_flow_test = boundary_flow_contam( filepath, n, t[3], VentMatrix.geometry)
print("boundary flow test" + str(boundary_flow_test))

extract_flow_test = extract_flow_contam( filepath, n, t[3], VentMatrix.geometry)
print("extract flow test" + str(extract_flow_test))


############################################################################
#saving results to excel spreadsheet
############################################################################
#convert to data frame
# =============================================================================
# df1=pd.DataFrame(Ct, columns=['Zone 1','Zone 2','Zone 3','Zone 4','Zone 5','Zone 6','Zone 7','Zone 8','Zone 9','Zone 10','Zone 11','Zone 12'])
# df2=pd.DataFrame(Et, columns=['Zone 1','Zone 2','Zone 3','Zone 4','Zone 5','Zone 6','Zone 7','Zone 8','Zone 9','Zone 10','Zone 11','Zone 12'])
# 
# #export
# df1.to_csv(r'C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Code\Zonal_models\Zonal_Models_New_versions\Scenarios\CONTAM_wth\python_results\%sqhr\Conc_pyresults.csv' %(qhr))#Flip180\%sqhr\Conc_pyresults.csv' %(qhr))#, sheet_name = 'Concentration')
# df2.to_csv(r'C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Code\Zonal_models\Zonal_Models_New_versions\Scenarios\CONTAM_wth\python_results\%sqhr\Expos_pyresults.csv' %(qhr) )#Flip180\%sqhr\Expos_pyresults.csv' %(qhr) )#, sheet_name = 'Exposures')
# 
# =============================================================================
