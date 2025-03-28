# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 15:50:49 2023
This script is used as part of the study entitled "Assessing the effects of transient weather conditions on 
airborne transmission risk in naturally ventilated hospitals."; 
Alexander J. Edwards, Marco-Felipe King,  Martin Lopez-Garcia, Daniel Peckham, Catherine J. Noakes.".
The user should refer to the README file in the GitHub repository for a description on its use.

@author: scaje
"""
from read_csv_gen_AJE import ReadCSV
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
#simulation - each zone -All doors Closed
##########################################################
##########################################################

co2_data_sim = ReadCSV(r'CO2_analysis\CO2_data_OctOnly_Allclsd.csv')[1][:,1:] # extractin co2 data for zones only - ignoring amb


summary_data_sim1 = np.zeros((3,int(np.shape(co2_data_sim)[1])))
for i in range(int(np.shape(co2_data_sim)[1])):
    summary_data_sim1[0,i] = (((co2_data_sim[:,i]<800).sum())/len(co2_data_sim[:,i]))*100
    summary_data_sim1[1,i]=((((co2_data_sim[:,i]<1200).sum()) - ((co2_data_sim[:,i]<800).sum()))/len(co2_data_sim[:,i]))*100
    summary_data_sim1[2,i]=(((co2_data_sim[:,i]>1200).sum())/len(co2_data_sim[:,i]))*100
    
    
##########################################################
#simulation - each zone - half doors clsd
##########################################################
##########################################################

co2_data_sim = ReadCSV(r'CO2_analysis\CO2_data_OctOnly_Halfclsd.csv')[1][:,1:] # extractin co2 data for zones only - ignoring amb


summary_data_sim2 = np.zeros((3,int(np.shape(co2_data_sim)[1])))
for i in range(int(np.shape(co2_data_sim)[1])):
    summary_data_sim2[0,i] = (((co2_data_sim[:,i]<800).sum())/len(co2_data_sim[:,i]))*100
    summary_data_sim2[1,i]=((((co2_data_sim[:,i]<1200).sum()) - ((co2_data_sim[:,i]<800).sum()))/len(co2_data_sim[:,i]))*100
    summary_data_sim2[2,i]=(((co2_data_sim[:,i]>1200).sum())/len(co2_data_sim[:,i]))*100  
    
    
    
##########################################################
#comparison betweeen experimental and zone 5 (nurse station)
##########################################################
width=0.15
x=[1,2,3]
xlabel=['400-800ppm', '800-1200ppm', '>1200ppm']


plt.figure(dpi=750)#set dots per inch for better quality images
plt.bar(x[0] - 2*width, summary_data_exp[0], 0.3,color='m', label='Measured $CO_2$')#, label = '400-800ppm')
plt.bar(x[1] - 2*width , summary_data_exp[1], 0.3, color = 'm')#, label = '800-1200ppm')
plt.bar(x[2] - 2*width, summary_data_exp[2], 0.3, color = 'm')#, label = '>1200ppm')

plt.bar(x[0] , summary_data_sim2[0,4], 0.3, color = 'b' , label='Simulated $CO_2$ - Patient doors Closed')#, label = '400-800ppm')
plt.bar(x[1] , summary_data_sim2[1,4], 0.3, color = 'b' )#, label = '800-1200ppm')
plt.bar(x[2] , summary_data_sim2[2,4], 0.3, color = 'b')#, label = '>1200ppm')

plt.bar(x[0] + 2*width, summary_data_sim1[0,4], 0.3, color = 'orange' , label='Simulated $CO_2$ - All doors closed')#, label = '400-800ppm')
plt.bar(x[1] + 2*width, summary_data_sim1[1,4], 0.3, color = 'orange' )#, label = '800-1200ppm')
plt.bar(x[2] + 2*width, summary_data_sim1[2,4], 0.3, color = 'orange')#, label = '>1200ppm')

#plt.xticks(np.arange(0, np.max(t_plot), 1), month_label, rotation=45)#arrange in steps of 1 from 0 to max value - using mnth_label as x labels on a slant of 45 degrees
#plt.xlabel("Time of year [Months]")
plt.xticks(np.arange(1,4,1),xlabel)
plt.yticks(np.arange(0,110,10))
plt.ylabel("Percentage %")
#plt.title("$CO_2$ values for Oct - Comparison")
plt.legend()
plt.show()
