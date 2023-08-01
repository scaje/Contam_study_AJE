"""
This script is used as part of the study entitled "Assessing the effects of transient weather conditions on 
airborne transmission risk in naturally ventilated hospitals."; 
Alexander J. Edwards, Marco-Felipe King,  Martin Lopez-Garcia, Daniel Peckham, Catherine J. Noakes.".
The user should refer to the README file in the GitHub repository for a description on its use.
"""

import csv #csv package is imported
import numpy as np #import numpy

def ReadCSV(x):
    
    #open csv file
    file = open(x)
    
    #check what type of file has been opened
    type(file)
    
    #use the in-built csv reader to read in the file
    csvreader = csv.reader(file)
    
    #create an empty list for the header
    header = []
    
    #import the header names from the file which has been read
    header = next(csvreader)
    
    
    header.pop(0) #gets rid of first entry
    header.pop(0) # gets rid of 2nd entry
    
    #check the output for 'header' list
    header 
    
    #dates
    date = []
   # for date in csvreader:
       # date.append(date[0]) #appends the dates to date column
    
    
    #Extract the rows in the file
    
    rows = [] #empty list called rows
    
    for row in csvreader:
            date.append(row[0])#extracts the date information
            row.pop(0) #gets rid of first entry
            row.pop(0) #gets rid of 2nd entry
            rows.append(row) #append each row to the list
    
    #check output of rows
    rows.pop(-1) #removes the last time step
    date.pop(-1) #removes the last time step
    rows
    
    #extract numbers from list into an array
    rows = np.array(rows)
    rows = rows.astype(np.float) #changes an array of strngs to an array of floats
    
    #close the file - once it is closed, no further operations can be performed on the original csv file
    #and everything is stored in 'csvreader'
    file.close()
    
    
    return header, rows, date


