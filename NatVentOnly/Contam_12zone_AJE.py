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
from scipy.integrate import odeint #for solving odes
import time #for live run time of code
import ventflows_AJE as VentMatrix #imports setup for 6 zone ward ventilaton setting from another file where it is already defined
from ventflows_AJE import VentilationMatrix #import function which defines ventilation matrix
from ventflows_AJE import InvVentilationMatrix #imports function which defines inverse ventilation matrix
from SE_Conc_eqns_AJE import odes #imports predefined SE ode functions for transient concentration
from SE_Conc_eqns_AJE import steadyodes ##imports predefined SE ode functions for steady concentration
from output_contam import output_SE_Ct #This imports the plotting ode for all possible outputs for multizonal transient concentreation SE model
from IzFlows_AJE import boundary_flow_contam #this import the function which changes the boundary flow values based on output from contam simulation
from Extract_AJE import extract_flow_contam #this import the function which changes the extract ventiatlion in each zonebased on output from contam simulation




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



##############################################################################
##############################################################################
############################## ZONAL SETUP ###################################
##############################################################################

######################Run ventilation setting############################ 
n=12


#THE FILEPATH USED FOR THE RESULTS THROUGHOUT 
filepath = r"Contam_sim/IZFlows.csv"


###############################################################

#Pulmonary rate in each zone
p_zonal = np.zeros(n)
#for when  is the same in each room
for i in range(n):
    p_zonal[i] = p

############################################################################

#Zonal quanta
q_zonal = np.zeros(n)
#for when  is the same in each room
for i in range(n):
    q_zonal[i] = q

############################################################################


 

#Zonal volumes 
I_zonal = np.zeros(n)

I_zonal[4]=1

##########################################################################

#############################################################################
#############################################################################
######################### DEFINE  Transient ODES #############################
#############################################################################


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
sim_len_days = 183 #183 days for  Apr -End of Sept 
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
    

    V_zonal = VentilationMatrix(n, t[i], VentMatrix.geometry, filepath) #filepath defined at the start of the script
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
