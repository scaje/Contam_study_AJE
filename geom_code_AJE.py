"""
Created on Fri Apr 14 15:45:18 2023

This script is used as part of the study entitled "Assessing the effects of transient weather conditions on 
airborne transmission risk in naturally ventilated hospitals."; 
Alexander J. Edwards, Marco-Felipe King,  Martin Lopez-Garcia, Daniel Peckham, Catherine J. Noakes.".
The user should refer to the README file in the GitHub repository for a description on its use.

CREATED 14/04/2023 AJE
@author: scaje
"""


from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle 
from matplotlib.pyplot import cm #colour map package



def geom_colormap(risk_idx_zonal, risk_idx_ward):

    #imports image which is used for the heat map - in this case the ward geometry
    #even though image is not shown at the end, this sets the axis limits for the patches below
    image=Image.open(r"12Zone_geom_AJE.png")
    
    
    
    
    # Create figure and axes
    fig, ax = plt.subplots(dpi=750)
    
    
    
    # Display the original image
    ax.imshow(image)
    
    
    #sorting colour maps
    #risk_idx_zonal = [0.14423077, 0, 0.61538462, 0.61538462, 0, 0, 0, 0, 0, 0.96153846, 0.5,0.03846154]
    #risk_idx_ward  = 0.3581730769230769
    cmap = cm.Reds(risk_idx_zonal)
    
    # Create a Rectangle patch for each zone, following coordinates inline with original image axis 
    #(if not clear, uncomment original image to see where axis align)
    zone1 = Rectangle((2, 2), 415, 362, linewidth=1.5, edgecolor='k',facecolor=cmap[0])# facecolor=cmap[0])
    zone2 = Rectangle((885, 2), 411, 362 , linewidth=1.5, edgecolor='k', facecolor=cmap[1])
    zone3 = Rectangle((415, 2), 235, 205 , linewidth=1.5, edgecolor='k', facecolor=cmap[2])
    zone4 = Rectangle((650, 2), 235, 205 , linewidth=1.5, edgecolor='k', facecolor=cmap[3])
    zone5 = Rectangle((415, 205), 470, 157 , linewidth=1.5, edgecolor='k', facecolor=cmap[4])
    zone6a = Rectangle((2, 362), 418, 140 , linewidth=1.5, edgecolor='k', facecolor='lightgrey')#cmap[5])
    zone6b = Rectangle((418, 362), 468, 140 , linewidth=1.5, edgecolor='k', facecolor='lightgrey')#cmap[6])
    zone6c = Rectangle((886, 362), 410, 140 , linewidth=1.5, edgecolor='k', facecolor='lightgrey')#cmap[7])
    zone7 = Rectangle((418, 502), 225, 347 , linewidth=1.5, edgecolor='k', facecolor='lightgrey')#cmap[8])
    zone8 = Rectangle((643, 502), 240, 347 , linewidth=1.5, edgecolor='k', facecolor=cmap[9])
    zone9 = Rectangle((883, 502), 190, 347 , linewidth=1.5, edgecolor='k', facecolor=cmap[10])
    zone10 = Rectangle((1073, 502), 223, 347 , linewidth=1.5, edgecolor='k', facecolor=cmap[11])
    
    # Add the patch to the Axes
    ax.add_patch(zone1)
    ax.add_patch(zone2)
    ax.add_patch(zone3)
    ax.add_patch(zone4)
    ax.add_patch(zone5)
    ax.add_patch(zone6a)
    ax.add_patch(zone6b)
    ax.add_patch(zone6c)
    ax.add_patch(zone7)
    ax.add_patch(zone8)
    ax.add_patch(zone9)
    ax.add_patch(zone10)
    
    
    ax.axis('off')#to remove the axis lines and values
    #ax.invert_yaxis() #to invert y axis of image
    
    ####
    #to plot colourbar legend
    Reds=cm.Reds
    m = cm.ScalarMappable(cmap=Reds)
    m.set_array([])
    plt.colorbar(m, label = 'Risk Index')
    ########
    #######################
    #####If want to colour the text box with ward risk index on same colour map use below.....
    ###### colour the risk index for ward box also
    ward_cmap = Reds(risk_idx_ward)
    ######
    
    ##Defining the Key for the image
    #print value of average ward risk index
    plt.text(10, 650, '''Total Ward Risk
Index = %s''' %(round(risk_idx_ward,4)), fontsize = 10, bbox = dict(facecolor = ward_cmap, alpha = 0.5)) #Adding text inside a rectangular box by using the keyword 'bbox'


    
    plt.text(10,750, '    =Infector', fontsize=10, bbox = dict(facecolor = 'w', alpha = 0.5)) #Adding text inside a rectangular box by using the keyword 'bbox'    
    #defining colours
    plt.text(10,850, 'No occupants', fontsize = 10, bbox = dict(facecolor = 'lightgrey', alpha = 0.5)) #Adding text inside a rectangular box by using the keyword 'bbox'


    #adding zone names to each zone
    plt.text(13, 350, 'Zone 1', fontsize = 8, ) #Adding text inside a zone
    plt.text(900, 350, 'Zone 2', fontsize = 8, ) #Adding text inside a zone
    plt.text(425, 190, 'Zone 3', fontsize = 8, ) #Adding text inside a zone
    plt.text(665, 190, 'Zone 4', fontsize = 8, ) #Adding text inside a zone
    plt.text(425, 350, 'Zone 5', fontsize = 8, ) #Adding text inside a zone
    plt.text(13, 485, 'Zone 6', fontsize = 8, ) #Adding text inside a zone
    plt.text(430, 485, 'Zone 7', fontsize = 8, ) #Adding text inside a zone
    plt.text(900, 485, 'Zone 8', fontsize = 8, ) #Adding text inside a zone
    plt.text(425, 835, 'Zone 9', fontsize = 8, ) #Adding text inside a zone
    plt.text(650, 835, 'Zone 10', fontsize = 8, ) #Adding text inside a zone
    plt.text(900, 835, 'Zone 11', fontsize = 8, ) #Adding text inside a zone
    plt.text(1080, 835, 'Zone 12', fontsize = 8, ) #Adding text inside a zone
    
    

    ####
    #ax(dpi=350)
    plt.show()

