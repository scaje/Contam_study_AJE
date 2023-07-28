# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 15:00:04 2023

@author: scaje

This script is used as part of the study entitled "Assessing the effects of transient weather conditions on 
airborne transmission risk in naturally ventilated hospitals."; 
Alexander J. Edwards, Marco-Felipe King,  Martin Lopez-Garcia, Daniel Peckham, Catherine J. Noakes.".
The user should refer to the README file in the GitHub repository for a description on its use.




Created 15/03/2023 AJE
"""



import numpy as np
from scipy.integrate import odeint #for solving odes
import time #for live run time of code
import ventflows_MV_AJE as VentMatrix #imports setup for 6 zone ward ventilaton setting from another file where it is already defined
from ventflows_MV_AJE import VentilationMatrix #import function which defines ventilation matrix
from ventflows_MV_AJE import InvVentilationMatrix #imports function which defines inverse ventilation matrix
from SE_Conc_eqns_AJE import odes #imports predefined SE ode functions for transient concentration
from SE_Conc_eqns_AJE import steadyodes ##imports predefined SE ode functions for steady concentration
from output_contam import output_SE_Ct #This imports the plotting ode for all possible outputs for multizonal transient concentreation SE model
from IzFlows_AJE import boundary_flow_contam #this import the function which changes the boundary flow values based on output from contam simulation
from Extract_MV_AJE import extract_flow_contam #this import the function which changes the extract ventiatlion in each zonebased on output from contam simulation
import matplotlib.pyplot as plt
import math
from geom_code_AJE import geom_colormap #function for colouring zones in accordiing to risk factor


start_time = time.time() #time code started running


###########################################################################
########################################################
###########################Initial values###################################

#number of zones
n=12

#people in each zone
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
    

#Pulmonary rate in each zone
p_zonal = np.zeros(n)
#for when  is the same in each room
for i in range(n):
    p_zonal[i] = 0.01

#quanta rate = quanta/min . person (as 0.5 quanta per min)
q=0.5 
qhr = int(q*60) #qunta rate per hour
#pulmonary rate = volume/min ( as 0.01volume/min)
p=0.01


##############################################################################
##############################################################################
############################## ZONAL SETUP ###################################
##############################################################################

######################Run ventilation setting############################ 



#THE FILEPATH USED FOR THE RESULTS THROUGHOUT (Uncomment where neccessary)
#For 'mechanical ventialtion only' case
#filepath = r"Contam_sim\IZFlow_MV_winclsd3ACH.csv"

#for 'natural ventilation and mechanical ventialtion' case
#filepath = r"Contam_sim\IZFlows_MV_winop3ACH.csv"

#3ach mech vent
filepathMV =  r"Contam_sim\MechVentFlows3ACH.csv"

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

#infected person
I_zonal = np.zeros(n)
I_zonal[4] = 1#define zone with infector
 

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
        V_zonal = VentilationMatrix(n, t[i], VentMatrix.geometry, filepath,filepathMV) #define filepaths at beginning of script
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
##############PLOTTING #######################

#re-define the number of people in each zone
#instead of total population, K_zonal is now the number of sucspetible. 
#This needs to be adjusted depending on the zone of the infector. 
#e.g. currently the infector is in zone 5, where there are no suscepibtles
#people in each zone
K_zonal = np.zeros(n)
K_zonal[0]=4
K_zonal[1]=4
K_zonal[2]=1
K_zonal[3]=1
K_zonal[4]=0
K_zonal[5]=0
K_zonal[6]=0
K_zonal[7]=0
K_zonal[8]=0
K_zonal[9]=3
K_zonal[10]=2
K_zonal[11]=1

###################### NEW ANALYSIS #######################################
##########################################################################
#function for rounding up
def round_up(n, decimals):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

#resetting vector to originals 
week_total_exp_all = Et_week_end




#storing in weeks and zones again rather than in one vector (for zonal or weekly analysis)
week_total_exp_zonal = np.empty((num_weeks,n))
for i in range(num_weeks):
    for j in range(n):
        week_total_exp_zonal[i,j] = week_total_exp_all[int(j+i*12)]


#rounding up values which are very close to integer (within 0.01) 
for i in range(num_weeks):
    for j in range(n):
        week_total_exp_zonal[i,j] = int(round_up(week_total_exp_zonal[i,j], 2))



################################## PLOTTING ##############################
######Probability histogram of exposures in a particular zone #############
#bar plot with probabilities
#setup bars and frequencies for histogram
bins_zonal=[[] for i in range(n)]
for i in range(n):
    bins_zonal[i] = np.linspace(0,int(K_zonal[i]), int(K_zonal[i]+1))

freq_zonal = [[] for i in range(n)]

#find probabilities for each exposure in each zone
for i in range(n):
    binwidth = 1
    freq_zonal[i] ,bins_zonal[i] = np.histogram(week_total_exp_zonal[:,i], bins=int(K_zonal[i]+1), range=(0, int(K_zonal[i]+1)), density=True)


    
#Probabilities for histogram across whole ward over time
#finding probabilities for each exposure across the ward 
week_total_exp_ward = np.sum(week_total_exp_zonal,axis=1)
freq_ward, bins_ward = np.histogram(week_total_exp_ward, bins = int(np.sum(K_zonal)+1), range = (0,int(np.sum(K_zonal)+1)), density=True)
x_ward =np.linspace(0, int(np.sum(K_zonal)), int(np.sum(K_zonal)+1))


################################################################################
################################################################################
#################### CALCULATING A RISK INDEX ##################################
###############################################################################

######## FOR EACH ZONE #####
risk_idx_zonal = np.empty((n)) #intialising a vector for risk index for each zone
E_x_zonal = np.empty((n)) #initialising empty vector for expected value


for i in range(n):
    E_xi=0 # initialsie epxetced value
    for j in range(len(freq_zonal[i])):
        
        E_xi = E_xi + (freq_zonal[i][j] * bins_zonal[i][j])# caluclated the expected value for each exposure in each zone

    
    E_x_zonal[i] = E_xi #store vector for epxected values 
    if K_zonal[i]==0:
        risk_idx_zonal[i] = 0
    else:
        risk_idx_zonal[i] = E_x_zonal[i] / int(K_zonal[i]) #caluclated probability risk index by dividing by total susceptible
    
print('Expected exposure value in each zone = %s'%(E_x_zonal))
print('Risk Index Factor in Each Zone = %s' %(risk_idx_zonal))


######## FOR THE WHOLE WARD #####
#initialise
risk_idx_ward = 0 #intialising a vector for risk index for each zone
E_x_ward = 0 #initialising empty vector for expected value

#calculate
for i in range(len(freq_ward)):
    E_x_ward = E_x_ward + (freq_ward[i]*bins_ward[i])
    risk_idx_ward = E_x_ward / int(np.sum(K_zonal))
    
print('Expected exposure value for the ward = %s'%(E_x_ward))
print('Risk Index Factor  for the ward = %s' %(risk_idx_ward))



########### Plotting for war dhistogram with risk index ########

#Probabilities for histogram across whole ward over time 
week_total_exp_ward = np.sum(week_total_exp_zonal,axis=1)
freq_ward, bins_ward = np.histogram(week_total_exp_ward, bins = int(np.sum(K_zonal)+1), range = (0,int(np.sum(K_zonal)+1)), density=True)
x_ward =np.linspace(0, int(np.sum(K_zonal)), int(np.sum(K_zonal)+1))
plt.figure(dpi=750)#set dots per inch for better quality images
plt.bar(x_ward, freq_ward)
plt.xlabel('Exposures [people]')
plt.xticks(x_ward)
plt.yticks(np.arange(0,1.1,0.1))
plt.ylabel('Probability')
#plt.title('Probability of Weekly Exposures over a 6-month period across the ward')
plt.text(3, 0.8, 'Risk Index = %s' %(round(risk_idx_ward,4)), fontsize = 22, bbox = dict(facecolor = 'red', alpha = 0.5)) #Adding text inside a rectangular box by using the keyword 'bbox'
plt.show()



############################################################################
######################### COLOUR MAP ON GEOMERTY #########################

#call function from other script with geomerty coded - include risk index for each zone, and for the ward as arguments

geom_colormap(risk_idx_zonal, risk_idx_ward) #calls the function which is already defined


print("--- Run Time = %s seconds ---" % (time.time() - start_time))

