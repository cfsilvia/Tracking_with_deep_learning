# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 08:46:29 2024

@author: Administrator
"""
#Define constants
NUMBER_OF_FRAMES = 100


import numpy as np
#Use Agg backend for canvas
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import cv2

class CreatePlot:
    def  __init__(self,frame, data_to_plot, counter_frame,up_line, down_line,data_to_plot_left = [],title = []):
        self.frame = frame
        self.data_to_plot = data_to_plot
        self.counter_frame = counter_frame
        self.upper = up_line
        self.lower = down_line
        if any(data_to_plot_left):
           self.data_to_plot_left = data_to_plot_left
        else:
            self.data_to_plot_left = []
        if any(title):
            self.title = title
        else:
            self.title = []
        
        
    '''
    Select data to plot-select the frames
    output: cut data and cut frames
    '''
    def SelectDataToPlot(self):
        if self.counter_frame < NUMBER_OF_FRAMES:
            #find the data to plot
            self.Selected_frame = np.arange(0,self.counter_frame + NUMBER_OF_FRAMES,1)
        elif self.counter_frame + NUMBER_OF_FRAMES > len(self.data_to_plot): # if go over the number of data
            self.Selected_frame = np.arange(self.counter_frame - NUMBER_OF_FRAMES,len(self.data_to_plot)-1,1)
        else:
            self.Selected_frame = np.arange(self.counter_frame - NUMBER_OF_FRAMES ,self.counter_frame + NUMBER_OF_FRAMES,1)
      
        self.Selected_data = self.data_to_plot.iloc[self.Selected_frame]
        if any(self.data_to_plot_left):
           self.Selected_data_left = self.data_to_plot_left.iloc[self.Selected_frame]
    '''
    Fill subplot with frame and data
    '''    
    def FillSubplot(self):
        ax1,ax2,fig = CreatePlot.CreateSubplots()
        #set the axis
        plt.axes(ax1);
        ax1.get_xaxis().set_visible(False);
        ax1.get_yaxis().set_visible(False);
        
        # showing image
        plt.imshow(self.frame);
        fig.canvas.draw()
        fig.canvas.flush_events()
        #%%Plot data
        plt.axes(ax2);
        plt.plot(self.Selected_frame[~np.isnan(self.Selected_data)], self.Selected_data[~np.isnan(self.Selected_data)], color= 'red',linewidth=2);
        if any(self.data_to_plot_left):
           plt.plot(self.Selected_frame[~np.isnan(self.Selected_data)], self.Selected_data_left[~np.isnan(self.Selected_data)], color= 'blue',linewidth=2);
        
        plt.axvline(x= self.counter_frame,color = 'black',linestyle='dashed', linewidth=2)
        plt.axhline(y = self.upper, color = 'b', linestyle ='dashed', linewidth = 2)
        plt.axhline(y = self.lower, color = 'b', linestyle ='dashed', linewidth = 2)
        
        plt.ylim((self.lower)*1.5,(self.upper)*1.5)
        #%% add title
        plt.title(self.title,fontsize=18, color='blue', fontweight='bold')
        #%%
        fig.canvas.draw()
        fig.canvas.flush_events()
        img = np.array(fig.canvas.renderer._renderer)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        return img,fig
        
        
#%% Static methods
       
    '''
    Create subplots on a given figure
    return figure and axis
    '''
    @staticmethod
    def CreateSubplots():
            fig = plt.figure()
            fig.set_figheight(20)
            fig.set_figwidth(20)
            ax1 = plt.subplot2grid(shape=(3, 1), loc=(0, 0), colspan=1,rowspan = 2)
            ax2 = plt.subplot2grid(shape=(3, 1), loc=(2, 0), colspan=1)
            return ax1,ax2,fig
