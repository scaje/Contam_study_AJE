# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 15:00:04 2023

@author: scaje

This script includes the analysis completed on the CONTAM WTH study
Here, we aim to run the multi-zonal model with imported vent flows and boundary flows
and the run for a weekly period - resetting the exposure to an initial condition of 10.

This then stores the final number of exposures per week, per zone in a vector which are collected
and will be used to produce a distribution of the solutions.
This also includes a mechanical ventialtion applied to each zone within the contam model which is imported here also




Created 15/03/2023 AJE
"""


import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint #for solving odes
import matplotlib.colors as mcolors #colour name package
from matplotlib.pyplot import cm #colour map package
#from pywaffle import Waffle #visual package for visuallising icons
import time #for live run time of code
#import pandas as pd
from read_csv_gen import ReadCSV
from gradient_func import deriv #import function for calculating the gradient
#import datetime #python datetime module
#from windrose import WindroseAxes
import random, math
import J12_12z_contam_wth_ventflows_MV as VentMatrix #imports setup for 6 zone ward ventilaton setting from another file where it is already defined
from J12_12z_contam_wth_ventflows_MV import VentilationMatrix #import function which defines ventilation matrix
from J12_12z_contam_wth_ventflows_MV import InvVentilationMatrix #imports function which defines inverse ventilation matrix
from SE_Concentration_Functions import odes #imports predefined SE ode functions for transient concentration
from SE_Concentration_Functions import steadyodes ##imports predefined SE ode functions for steady concentration
from output_contam import output_SE_Ct #This imports the plotting ode for all possible outputs for multizonal transient concentreation SE model
from contam_wth_IzFlows_12zone import boundary_flow_contam #this import the function which changes the boundary flow values based on output from contam simulation
from contam_wth_Extract_MV_12z import extract_flow_contam #this import the function which changes the extract ventiatlion in each zonebased on output from contam simulation
import pandas as pd


start_time = time.time() #time code started running


#########################################################################################################################################################

####################### filepaths ####################################

#########################################################################################################################################################

############# Results from multi-zone code########
#the multi-zone code here currently runs for a period of 183 days, time stepping every minute giving...
#...263520 time setps in total.
#This also runs for 183 days April - End of Sept
#concentration
#filepath_conc = r'C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Code\Zonal_models\Zonal_Models_New_versions\Scenarios\CONTAM_wth\python_results\Conc_pyresults.csv'
#Ct = ReadCSV(filepath_conc)[1] #take the second argument (note that the first argument gives headers, second gives the data, the last gives dates/indicies)


#exposures
#filepath_exp = r'C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Code\Zonal_models\Zonal_Models_New_versions\Scenarios\CONTAM_wth\python_results\Expos_pyresults.csv'
#Et = ReadCSV(filepath_exp)[1]

###########################################################################
#############################################################################
############################################################################
#Initial values from other simulations for reference
########################################################
###########################Initial values###################################

#number of zones
#n= int(np.shape(Ct)[1])
n=12

#people in each zone
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
    

#Pulmonary rate in each zone
p_zonal = np.zeros(n)
#for when  is the same in each room
for i in range(n):
    p_zonal[i] = 0.01

#quanta rate = quanta/min . person (as 0.5 quanta per min)
q=0.5 #0.0166667=1qhr, 0.1666667=10qhr, 0.5=30qhr
qhr = int(q*60)
#pulmonary rate = volume/min ( as 0.01volume/min)
p=0.01


##############################################################################
##############################################################################
############################## ZONAL SETUP ###################################
##############################################################################

######################Run ventilation setting############################ 



#THE FILEPATH USED FOR THE RESULTS THROUGHOUT (change save directory at end)
#3ACH windows open
#=filepath = r"C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Contam_models\wind_driven_flow_study\J12_12zone\MechVent\Exported_results\IZFlows_winop3ACH.csv"
#3ach windows closed
#filepath = r"C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Contam_models\wind_driven_flow_study\J12_12zone\MechVent\Exported_results\IZFlow_winclsd3ACH.csv"
#6ach windows closed
filepath = r"C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Contam_models\wind_driven_flow_study\J12_12zone\MechVent\Exported_results\IZFlow_winclsd6ACH.csv"

#3ach mech vent
#filepathMV =  r"C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Contam_models\wind_driven_flow_study\J12_12zone\MechVent\Exported_results\MechVentFlows3ACH.csv"
#6ach mech vent
filepathMV =  r"C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Contam_models\wind_driven_flow_study\J12_12zone\MechVent\Exported_results\MechVentFlows6ACH.csv"

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

#infected person
I_zonal = np.zeros(n)
I_zonal[4] = 1
 

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


###Calculate a weekly t for simulation
num_weeks = int(sim_len_days/7) #total number of weeks in simualtions
week_delta_t = 7*24*60 # Total minute time steps in a week
week_2hours = 7*24/2


t = [] #initialise t
#define first time period
t_0 = np.linspace(0, update_t_len , update_t_len) #weather time step defined in minutes, we want steps in minutes also so keep same
t.append(t_0)#include first time period into t
for i in range((int(sim_len_hrs/2)) -1):#sim_len_hrs gives number of hours in sim, we divide by two as updating every 2 hrs not 1 so half as many steps
    t_i = np.linspace(t[i][-1], t[i][-1] + update_t_len, update_t_len)
    
    t.append(t_i) 
    



#defining t for calculation
t_week = np.linspace(0,week_delta_t, week_delta_t) # made up of minute time steps for 1 week



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
S0 = K_zonal - I_zonal_t1 - E0 #inital suceptibles
D0 = np.zeros(n) #inital dose received
Ct = np.empty((0,n))
St = np.empty((0,n))
Et = np.empty((0,n))
Dt = np.empty((0,n))
#combining intial conditions
X0 = np.hstack( (C0, S0, E0, D0) )
print(X0)

#arrays for end values
St_weekly = [[] for i in range(num_weeks)] #this sets up to stores a vector of the weekly solutions in vector forms 
Et_weekly = [[] for i in range(num_weeks)] #this sets up to stores a vector of the weekly solutions in vector forms 
St_week_end=() #defining vector to store end values
Et_week_end=() #defining vector to store end values


for j in range(num_weeks):

    for i in range(int(week_2hours*(j)), int(week_2hours*(j+1))):
        V_zonal = VentilationMatrix(n, t[i], VentMatrix.geometry, filepath,filepathMV)
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
        
        print("COUNT i (Solution period) =" +str(i))
        print("COUNT j (Week No.) =" +str(j+1))
        #End
        
        
        
    #storing results
    St_weekly[j] = St[week_delta_t*j:week_delta_t*(j+1),:]
    Et_weekly[j] = Et[week_delta_t*j:week_delta_t*(j+1),:]
        
    #storing end results results in a vector
    St_weekly_last = St_weekly[j][-1,:]
    Et_weekly_last = Et_weekly[j][-1,:]
        
    St_week_end = np.append(St_week_end, St_weekly_last)
    Et_week_end = np.append(Et_week_end, Et_weekly_last)
    
    #redefine the epidemic model initial conditions 
    
    
    E0 = np.zeros(n) #inital exposed
    S0 = K_zonal - I_zonal - E0 #inital suceptibles   

    X0 = np.hstack( (C0[-1,:], S0, E0, D0[-1,:]) )
    print(X0)
    
    
    
    print("COUNT j (Week No.) =" +str(j+1))
    #End


    
    


###########################################################################
###########################################################################




############################################################################
#saving results to excel spreadsheet
############################################################################
#convert to data frame
df1=pd.DataFrame(Et, columns=['Zone 1','Zone 2','Zone 3','Zone 4','Zone 5','Zone 6','Zone 7','Zone 8','Zone 9','Zone 10','Zone 11','Zone 12'])
#df2=pd.DataFrame(Et_weekly)#, columns=['Zone 1','Zone 2','Zone 3','Zone 4','Zone 5','Zone 6','Zone 7','Zone 8','Zone 9','Zone 10','Zone 11','Zone 12'])
df3=pd.DataFrame(Et_week_end)#, columns=['Zone 1','Zone 2','Zone 3','Zone 4','Zone 5','Zone 6','Zone 7','Zone 8','Zone 9','Zone 10','Zone 11','Zone 12'])

#export
df1.to_csv(r'C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Code\Zonal_models\Zonal_Models_New_versions\Scenarios\CONTAM_wth\python_results\%sqhr\MechVent\winclsd6ACH\Weekly_Exposure_analysis\Exp_sol_all.csv' %(qhr))#, sheet_name = 'Concentration')
#df2.to_csv(r'C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Code\Zonal_models\Zonal_Models_New_versions\Scenarios\CONTAM_wth\python_results\Weekly_Exposure_analysis\Exp_sol_weekly.csv')#, sheet_name = 'Exposures')
df3.to_csv(r'C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Code\Zonal_models\Zonal_Models_New_versions\Scenarios\CONTAM_wth\python_results\%sqhr\MechVent\winclsd6ACH\Weekly_Exposure_analysis\Week_total_exp_all.csv'%(qhr))#, sheet_name = 'Exposures')

for i in range(num_weeks):
    df4=pd.DataFrame(Et_weekly[i], columns=['Zone 1','Zone 2','Zone 3','Zone 4','Zone 5','Zone 6','Zone 7','Zone 8','Zone 9','Zone 10','Zone 11','Zone 12'])
    df4.to_csv(r'C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Code\Zonal_models\Zonal_Models_New_versions\Scenarios\CONTAM_wth\python_results\%sqhr\MechVent\winclsd6ACH\Weekly_Exposure_analysis\Exp_sol_week_%s.csv' %(qhr,i+1))#





print("--- Run Time = %s seconds ---" % (time.time() - start_time))


#########################################################################################################################################################

######################### Plotting #########################################

#########################################################################################################################################################



    


############################################################################
############################################################################