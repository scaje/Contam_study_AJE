# -*- coding: utf-8 -*-
"""
This script is used as part of the study entitled "Assessing the effects of transient weather conditions on 
airborne transmission risk in naturally ventilated hospitals."; 
Alexander J. Edwards, Marco-Felipe King,  Martin Lopez-Garcia, Daniel Peckham, Catherine J. Noakes.".
The user should refer to the README file in the GitHub repository for a description on its use.


Created on Wed Mar 29 14:43:47 2023

@author: scaje


CREATED 29/03/23 AJE 
"""


import numpy as np
from Extract_AJE import extract_flow_contam #this import the function which changes the extract ventiatlion in each zonebased on output from contam simulation
import ventflows_AJE as VentMatrix #imports setup for 6 zone ward ventilaton setting from another file where it is already defined
import time #for live run time of code
import matplotlib.pyplot as plt#
import statistics as stat
import seaborn as sns #for density plot
from geom_code_natvent_AJE import geom_colormap_natvent #function for colouring zones in accordiing to risk factor


start_time = time.time() #time code started running
############################################################################

#THE FILEPATH USED FOR THE VENTIALTION RESULTS THROUGHOUT (change save directory at end)
filepath = r"Contam_sim\IZFlows.csv"


#number of zones
n=12

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
    
##########################################################################
##########################################################################

#Extracting nat vent rates



#following loop does it for each 2hr time step for each zone, and appends value

nat_vent_zonal = np.empty((len(t),n)) #vector for storing the natural ventialtion values for each zone 
nat_vent_ward = np.empty((len(t))) #vector for storing nat vent values for whole waard


for i in range(len(t)):
    extract_flow = extract_flow_contam(filepath, n, t[i], VentMatrix.geometry)#caluclated nat vent for each zone at each time period
    
    #rates are imported at m3/min - in order to get ACH we need to divide by corresponding volume, and mulitply by 60
    for j in range(n):
        nat_vent_zonal[i,j] = (extract_flow[j]/VentMatrix.v_zonal[j])*60
    nat_vent_ward[i] = (np.sum(extract_flow)/np.sum(VentMatrix.v_zonal))*60
    
    print("COUNT i =" +str(i))
    #End
    
    
############################################################################



################## PLOTTING ###################
########################
###### Nat vent #######
avg = stat.mean(nat_vent_ward)

###### MECH Vent#######
natvent_3ACH = nat_vent_ward + 3
avg_3ACH = stat.mean(natvent_3ACH)


############################################################################
############################### NAT VENT & Natvent and mechvent on the same plot.  all doors closed
######################################################################################

plt.figure(dpi=750)#set dots per inch for better quality images
sns.distplot(nat_vent_ward, hist=False, kde=True, 
             bins=int(max(nat_vent_ward)+1), color = 'cornflowerblue', 
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 2}, label='NV only')# Plot formatting
      

plt.vlines(avg,0,1.4,'r', label = 'Mean - NV Only')# plots mean line
plt.vlines(avg_3ACH,0,1.4,'darkorange', label = 'Mean - NV + 3 ACH MV')# plots mean line
plt.vlines(6,0,1.4,'g', label = 'HTM03-01 Guidance')



sns.distplot(natvent_3ACH, hist=False, kde=True, 
             bins=int(max(natvent_3ACH)+1), color = 'darkorchid', 
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 2}, label='NV + 3 ACH MV')#, label='Natural Ventilaion + 3 ACH')



plt.legend(loc='center left',prop={'size': 8}, bbox_to_anchor=(0.78, 0.5))#plt.legend(loc='upper right',prop={'size': 9})#, bbox_to_anchor=(1, 0.5), title='')
plt.xlabel('Ventilation Rate [ACH]')
#plt.title('Natural Ventilation + 3 ACH')
plt.xticks(np.arange(0,8,1))#x_ward_axis+3) #  for all_door_clsd (0,8,1)
plt.xlim(0,8) #for all_door_clsd (0,8)
#for all door clsd plt.yticks(np.arange(0,1.6,0.2)) 
plt.ylim(0,1.4) #for all door clsd (0, 0.14)
plt.ylabel('Density')
plt.show()



############################################################################
######################### COLOUR MAP ON GEOMERTY #########################

#call function from other script with geomerty coded - include risk index for each zone, and for the ward as arguments
nat_vent_zonal_avg=np.empty(n)
for i in range(n):
    nat_vent_zonal_avg[i] = stat.mean(nat_vent_zonal[:,i]) #np.sum(nat_vent_zonal[:,i])/len(nat_vent_zonal[:,i])

nat_vent_ward_avg = stat.mean(nat_vent_ward) #stat.mean(nat_vent_zonal_avg)


geom_colormap_natvent(nat_vent_zonal_avg, nat_vent_ward_avg) #calls the function which is already defined
########################################################################



print("--- Run Time = %s seconds ---" % (time.time() - start_time))
