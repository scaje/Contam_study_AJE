# -*- coding: utf-8 -*-
"""
Created 15/03/2023 AJE
This script is used as part of the study entitled "Assessing the effects of transient weather conditions on 
airborne transmission risk in naturally ventilated hospitals."; 
Alexander J. Edwards, Marco-Felipe King,  Martin Lopez-Garcia, Daniel Peckham, Catherine J. Noakes.".
The user should refer to the README file in the GitHub repository for a description on its use.
"""
from read_csv import ReadCSV
import numpy as np


def extract_flow_contam(filepath,n,t,geometry, filepathMV):
    flows = ReadCSV(filepath)
    MechVent = ReadCSV(filepathMV)
    
    print(flows)
    print(MechVent)
    
    
    # extract_flow defines flow from zone i to j
    extract_flow = np.zeros(n)
    #Diagonal terms
    for i in range(n):
        extract_flow[i] = 0
    

     
    # t is a vector of vectors e.g t[i][0] calls the first entry of the ith vector in t
    #we then divide by 30, to see how many time steps we have taken in the data
    #then multiply by 2, as there are 2 entries for each time step
    # then since the format of the data includes 2 entries for each flow value we take steps in 2 rather than 1
    #the second index then selects the colum which refers to the boundary
    
    #extract columns 
    #extract in zone 1 = - amb to zone 1 -- idx=0
    #extract in zone 2 = - amb to zone 2 -- idx=3
    #extract in zone 3 = - amb to zone 3 -- idx=1
    #extract in zone 4 = - amb to zone 4 -- idx=2
    #zone 5 internal zone - no nat vent
    #extract in zone 6a = - LHS to zone 6a -- idx=9
    #zone 6b internal zone - no nat vent
    #extract in zone 6c =  zone 6c to amb -- idx=12
    #extract in zone 7 = - amb to zone 2 -- idx=17
    #extract in zone 8 = - amb to zone 9 -- idx=18
    #extract in zone 9 = - amb to zone 9 -- idx=19
    #extract in zone 10 = - amb to zone 10 -- idx=20
    
    
    #dealing with natural ventialtion first
    extract_flow[0] = -(flows[int((t[0]/30)*2),0] + flows[int((t[0]/30)*2+1),0]) 

    extract_flow[1] = -(flows[int((t[0]/30)*2),3] + flows[int((t[0]/30)*2+1),3])

    extract_flow[2] = -(flows[int((t[0]/30)*2),1] + flows[int((t[0]/30)*2+1),1])

    extract_flow[3] = -(flows[int((t[0]/30)*2),2] + flows[int((t[0]/30)*2+1),2])


    extract_flow[5] = -(flows[int((t[0]/30)*2),9] + flows[int((t[0]/30)*2+1),9])

    
    extract_flow[7] = flows[int((t[0]/30)*2),12] + flows[int((t[0]/30)*2+1),12]
    
    extract_flow[8] = -(flows[int((t[0]/30)*2),17] + flows[int((t[0]/30)*2+1),17])
    
    extract_flow[9] = -(flows[int((t[0]/30)*2),18] + flows[int((t[0]/30)*2+1),18])
    
    extract_flow[10] = -(flows[int((t[0]/30)*2),19] + flows[int((t[0]/30)*2+1),19])
    
    extract_flow[11] = -(flows[int((t[0]/30)*2),20] + flows[int((t[0]/30)*2+1),20])
    
    #account for any natural ventialtion that is supply not extract. If supply set as zero
    for i in range(n):
        if extract_flow[i]<0:
            extract_flow[i] = 0
            
    #add any additional mechanical ventialtion to each zone
    extract_flow[0] = extract_flow[0] + (MechVent[int((t[0]/30)*2),2] + MechVent[int((t[0]/30)*2+1),2])

    extract_flow[1] = extract_flow[1]+ (MechVent[int((t[0]/30)*2),4] + MechVent[int((t[0]/30)*2+1),4])

    extract_flow[2] = extract_flow[2]+ (MechVent[int((t[0]/30)*2),0] + MechVent[int((t[0]/30)*2+1),0])

    extract_flow[3] = extract_flow[3] + (MechVent[int((t[0]/30)*2),1] + MechVent[int((t[0]/30)*2+1),1])

    extract_flow[4] = + (MechVent[int((t[0]/30)*2),3] + MechVent[int((t[0]/30)*2+1),3])

    extract_flow[5] = extract_flow[5] + (MechVent[int((t[0]/30)*2),5] + MechVent[int((t[0]/30)*2+1),5])

    extract_flow[6] = + (MechVent[int((t[0]/30)*2),6] + MechVent[int((t[0]/30)*2+1),6])
    
    extract_flow[7] = extract_flow[7] + (MechVent[int((t[0]/30)*2),7] + MechVent[int((t[0]/30)*2+1),7])
    
    extract_flow[8] = extract_flow[8] + (MechVent[int((t[0]/30)*2),8] + MechVent[int((t[0]/30)*2+1),8])
    
    extract_flow[9] =  extract_flow[9] + (MechVent[int((t[0]/30)*2),9] + MechVent[int((t[0]/30)*2+1),9])
    
    extract_flow[10] = extract_flow[10] + (MechVent[int((t[0]/30)*2),10] + MechVent[int((t[0]/30)*2+1),10])
    
    extract_flow[11] = extract_flow[11] + (MechVent[int((t[0]/30)*2),11] + MechVent[int((t[0]/30)*2+1),11])

    
    print("Ventilation in Zone i Extract_flow =" + str(extract_flow))
    ###########################################################################
    
    
    return extract_flow