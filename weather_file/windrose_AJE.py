# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 15:12:54 2023

@author: scaje
"""
from read_csv_gen import ReadCSV
from windrose import WindroseAxes
import numpy as np
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt
filepath = r"weather_file\GBR_ENG_Leeds.Wea.GEN.csv"

data = ReadCSV(filepath)
ws = data[1][:,2]
wd = data[1][:,3]


#A quick way to create new windrose axes...
def new_axes():
    fig = plt.figure(figsize=(6, 6), dpi=750, facecolor='w', edgecolor='w')
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect)
    fig.add_axes(ax)
    return ax

ax = new_axes()
ax.bar(wd,ws,normed=True, opening=0.8, edgecolor='white')

# also change the labels
ax.set_yticklabels(('5.2%','10.4%', '15.6%', '20.8%', '26.0%'))
ax.legend(loc='center left', bbox_to_anchor=(0.95, 0.1), title ='Speed [$ms^{-1}$]', fontsize=10)
