# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 13:21:38 2022

@author: scaje

This script is used as part of the study entitled "Assessing the effects of transient weather conditions on 
airborne transmission risk in naturally ventilated hospitals."; 
Alexander J. Edwards, Marco-Felipe King,  Martin Lopez-Garcia, Daniel Peckham, Catherine J. Noakes.".
The user should refer to the README file in the GitHub repository for a description on its use.

AJE

"""
from read_csv_co2_AJE import ReadCSV
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm #colour map package



######## FILE PATH
filepath= r'CO2_analysis\CO2_data.csv'
######################################






#define number of days in simulation
d=365

#simulation length in seconds
sim_len = d*24*60*60 #24hrsx60minsx60seconds to get length in seconds

#define time step length in seconds
delta_t=1800 #30 minutes

#Total number of time steps required
total_delta_t = sim_len / delta_t

#Defining time vector
t=np.linspace(0,183,8784)#np.linspace(0,d,int(total_delta_t))#(if all year) #np.linspace(0,183,8783) #if 6months apr-sept

#defining time vector for plotting
t_plot=t/30.4 #for plotting in months




#### assigning label to time plotting function
month_label=['Apr21','May21','Jun21','Jul21','Aug21','Sept21','Oct21']#['Jan21', 'Feb21','Mar21', 'Apr21','May21','Jun21','Jul21','Aug21','Sept21','Oct21','Nov21','Dec21','Jan22'] #['Apr21','May21','Jun21','Jul21','Aug21','Sept21','Oct21']#


#reading .csv
csv_data = ReadCSV(filepath)
headers=csv_data[0]
contaminant_data=csv_data[1][:8784,:]
date_info = csv_data[2]

print(contaminant_data)

#defining colours for plotting
colour = iter(cm.tab20(np.linspace(0, 1, len(contaminant_data[0])))) #defining colour map for new loop
#for more than 10 items use tab20 or tab10 when less than 10

plt.figure(dpi=750)#set dots per inch for better quality images     
##Plotting
for i in range(1,len(contaminant_data[0])):
    c = next(colour)#choosing next random colour for plotting
    plt.plot(t_plot, contaminant_data[:,i],color=c, label='Zone %s' %(i))

plt.plot(t_plot,contaminant_data[:,0], label='Ambient' )
#plt.title("$CO_2$ concentration in each zone")
plt.xlabel("Time [Months]")
plt.xticks(np.arange(0, np.max(t_plot), 1), month_label, rotation=45)#arrange in steps of 1 from 0 to max value - using mnth_label as x labels on a slant of 45 degrees
plt.yticks(np.arange(np.min(np.min(contaminant_data)),np.max(np.max(contaminant_data))+200,200))
plt.ylabel("$CO_2$ [ppm]")
plt.legend(loc='center left',prop={'size': 8}, bbox_to_anchor=(1, 0.5), title='Concentration')
plt.show()

######################################################################
######################################################################
######################################################################
######################################################################
