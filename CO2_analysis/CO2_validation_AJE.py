# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 15:50:49 2023
This script offers a comparison between experimental CO2 values and CONTAM simulation CO2 values for the month of October. 
The simulation CO2 values come from the increased_leakage study. 

@author: scaje
"""
from read_csv_gen import ReadCSV
import numpy as np
import matplotlib.pyplot as plt


##########################################################
#EXPERIMENTAL
##########################################################
co2_data_exp = ReadCSV(r'CO2_analysis\measured_co2_data.csv')[1]


#we will split into 3 groups 
#400-800ppm, 800-1200ppm, >1200ppm
summary_data_exp=np.zeros(3)
summary_data_exp[0] = (((co2_data_exp<800).sum())/len(co2_data_exp))*100
summary_data_exp[1]=((((co2_data_exp<1200).sum()) - ((co2_data_exp<800).sum()))/len(co2_data_exp))*100
summary_data_exp[2]=(((co2_data_exp>1200).sum())/len(co2_data_exp))*100



##########################################################
#simulation - all zones 
##########################################################

co2_data_sim = ReadCSV(r'CO2_analysis\CO2_data_OctOnly.csv')[1][:,1:] # extractin co2 data for zones only - ignoring amb


co2_data_sim_new = []

#loop to combine all co2 values from each zone and time step into one vector
for i in range(np.shape(co2_data_sim)[0]):
    for j in range(np.shape(co2_data_sim)[1]):
        co2_data_sim_new = np.append(co2_data_sim_new, co2_data_sim[i,j])
        


##########################################################
#simulation - each zone
##########################################################


summary_data_sim = np.zeros((3,int(np.shape(co2_data_sim)[1])))
for i in range(int(np.shape(co2_data_sim)[1])):
    summary_data_sim[0,i] = (((co2_data_sim[:,i]<800).sum())/len(co2_data_sim[:,i]))*100
    summary_data_sim[1,i]=((((co2_data_sim[:,i]<1200).sum()) - ((co2_data_sim[:,i]<800).sum()))/len(co2_data_sim[:,i]))*100
    summary_data_sim[2,i]=(((co2_data_sim[:,i]>1200).sum())/len(co2_data_sim[:,i]))*100

    
    
    
##########################################################
#comparison betweeen experimental and zone 5 (nurse station)
##########################################################
width=0.15
x=[1,2,3]
xlabel=['400-800ppm', '800-1200ppm', '>1200ppm']


plt.figure(dpi=750)#set dots per inch for better quality images
plt.bar(x[0] - width, summary_data_exp[0], 0.3,color='r', label='Experimental')#, label = '400-800ppm')
plt.bar(x[1] - width , summary_data_exp[1], 0.3, color = 'r')#, label = '800-1200ppm')
plt.bar(x[2] - width, summary_data_exp[2], 0.3, color = 'r')#, label = '>1200ppm')

plt.bar(x[0] + width, summary_data_sim[0,4], 0.3, color = 'b' , label='Simulation - Zone 5')#, label = '400-800ppm')
plt.bar(x[1] + width, summary_data_sim[1,4], 0.3, color = 'b' )#, label = '800-1200ppm')
plt.bar(x[2] + width, summary_data_sim[2,4], 0.3, color = 'b')#, label = '>1200ppm')



#plt.xticks(np.arange(0, np.max(t_plot), 1), month_label, rotation=45)#arrange in steps of 1 from 0 to max value - using mnth_label as x labels on a slant of 45 degrees
#plt.xlabel("Time of year [Months]")
plt.xticks(np.arange(1,4,1),xlabel)
plt.yticks(np.arange(0,110,10))
plt.ylabel("Percentage %")
plt.title("$CO_2$ values for Oct - Comparison")
plt.legend()
plt.show()

