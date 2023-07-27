# -*- coding: utf-8 -*-
"""
Created 25/01/2023 AJE
"""
from read_csv import ReadCSV
import numpy as np

#r"C:\Users\scaje\OneDrive - University of Leeds\UNIV. OF LEEDS\PhD PROJECT\Ward Transmission\Contam_models\wind_driven_flow_study\J12_12zone\Increased_leakage\Exported_results\IZFlows.csv"

def boundary_flow_contam(filepath,n,t,geometry):
    flows = ReadCSV(filepath)
    print(flows)
    
    
    # boundary_flow defines flow from zone i to j
    boundary_flow = np.zeros((n,n))
    #Diagonal terms
    for i in range(n):
        boundary_flow[i,i] = 0
    
    #other entries in boundary flow matrix
    #For homogenous mixing
    #for i in range(n-1):#n-1 since considering i+1 in indices below 
     #       boundary_flow[i,i+1]=9
     #       boundary_flow[i+1,i]=9
     
    #Homogenous Mixing
     
    # t is a vector of vectors e.g t[i][0] calls the first entry of the ith vector in t
    #we then divide by 30, to see how many time steps we have taken in the data
    #then multiply by 2, as there are 2 entries for each time step
    # then since the format of the data includes 2 entries for each flow value we take steps in 2 rather than 1
    #the second index then selects the colum which refers to the boundary

    boundary_flow[0,5] = flows[int((t[0]/30)*2),6] + flows[int((t[0]/30)*2+1),6]
    #boundary_flow[5,0] = - flows[int((t[0])*2+1),6]
    boundary_flow[1,7] = flows[int((t[0]/30)*2),8] + flows[int((t[0]/30)*2+1),8]
    #boundary_flow[5,1] = -flows[int((t[0])*2+1),8]
    boundary_flow[2,4] = flows[int((t[0]/30)*2),4] + flows[int((t[0]/30)*2+1),4]
    #boundary_flow[4,2] = -flows[int((t[0])*2+1),4]
    boundary_flow[3,4] = flows[int((t[0]/30)*2),5] + flows[int((t[0]/30)*2+1),5]
    #boundary_flow[4,3] = -flows[int((t[0])*2+1),5]
    boundary_flow[4,6] = flows[int((t[0]/30)*2),7] + flows[int((t[0]/30)*2+1),7]
    #boundary_flow[5,4] = -flows[int((t[0])*2+1),7]
    boundary_flow[5,6] = flows[int((t[0]/30)*2),10] + flows[int((t[0]/30)*2+1),10]
    boundary_flow[6,7] = flows[int((t[0]/30)*2),11] + flows[int((t[0]/30)*2+1),11]    
    boundary_flow[6,8] = -(flows[int((t[0]/30)*2+1),13] +flows[int((t[0]/30)*2),13])
    #boundary_flow[6,5] = flows[int((t[0])*2),13]
    boundary_flow[6,9] = -(flows[int((t[0]/30)*2+1),14] + flows[int((t[0]/30)*2),14])
    #boundary_flow[7,5] = flows[int((t[0])*2),14]
    boundary_flow[7,10] = -(flows[int((t[0]/30)*2+1),15] +flows[int((t[0]/30)*2),15])
   # boundary_flow[8,5] = flows[int((t[0])*2),15]
    boundary_flow[7,11] = -(flows[int((t[0]/30)*2+1),16] +flows[int((t[0]/30)*2),16])
    #boundary_flow[9,5] = flows[int((t[0])*2),16]
    
    for i in range(n):
        for j in range(n):
            if geometry[i,j] > 0:
                if boundary_flow[i,j] < 0:
                    boundary_flow[j,i] = - boundary_flow[i,j]
                    boundary_flow[i,j] = 0
                
    
    #add more for more zones, currently for 3 zones
    
    print("flow from zone i to zone k boundary_flow =" + str(boundary_flow))
    ###########################################################################
    
    
    return boundary_flow