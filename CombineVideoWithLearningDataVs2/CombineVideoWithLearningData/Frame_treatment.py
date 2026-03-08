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
import pandas as pd

class CreatePlot:
    def  __init__(self,frame, data_to_plot: pd.DataFrame, counter_frame: int,up_line: float, down_line: float,data_to_plot_left = None,titles = None):
        
       
        self.frame = frame
        self.data_to_plot = data_to_plot
        self.counter_frame = counter_frame
        self.upper = up_line
        self.lower = down_line
        self.data_to_plot_left = data_to_plot_left
        self.titles = titles or []

        # create summary table of max and min values for each column
        self.summary = pd.DataFrame([(self.data_to_plot.iloc[324:1200]).max(), (self.data_to_plot.iloc[324:1200]).min()], index=['max', 'min'])

        #

        if not isinstance(self.data_to_plot, pd.DataFrame):
            raise TypeError("data_to_plot must be a pandas DataFrame.")
        
        
           
        
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

        if self.data_to_plot_left is not None:
            self.Selected_data_left = self.data_to_plot_left.iloc[self.Selected_frame]
        else:
            self.Selected_data_left = None
    '''
    Fill subplot with frame and data
    '''    
    def FillSubplot(self):
        n_plots = self.data_to_plot.shape[1]
        ax_img, ax_list, fig  = CreatePlot.CreateSubplots(n_plots = n_plots)

         # --- Image axis ---
        ax_img.axis("off")
        ax_img.imshow(self.frame)

        fig.canvas.draw()
        fig.canvas.flush_events()


        #add user order
        user_order = ["BM_snout_y", "BM_head_y", "BM_behind_y"]
        # keep only those that exist, and keep the exact order
        cols = [c for c in user_order if c in list(self.Selected_data.columns)]
        #user colors
        colors = ['black', 'brown', 'green']

         # --- Time-series axes (one per column) ---
       # cols = list(self.Selected_data.columns)

        for i, col in enumerate(cols):
            ax = ax_list[i]
            y = pd.to_numeric(self.Selected_data[col], errors="coerce") #no consider nan values
            mask = ~np.isnan(y.to_numpy()) #true if is not nan
            ax.plot(self.Selected_frame[mask], y.to_numpy()[mask], color = colors[i], linewidth=2)

            if self.Selected_data_left is not None:
                yL = pd.to_numeric(self.Selected_data_left[col], errors="coerce")
                maskL = ~np.isnan(yL.to_numpy())
                ax.plot(self.Selected_frame[maskL], yL.to_numpy()[maskL], linewidth=2)

            ax.axvline(x=self.counter_frame, linestyle="dashed", linewidth=2)
            # if col == 'BM_snout_y':
            #   ax.axhline(y=self.upper, linestyle="dashed", linewidth=2)
            #   ax.axhline(y=self.lower, linestyle="dashed", linewidth=2)
            #   # Choose y-limits (same rule you used; adjust if needed)
            #   ax.set_ylim(self.lower * 1.5, self.upper * 1.5)
            
           
            ax.set_ylim(self.summary.loc['min', col] * 1.5, self.summary.loc['max', col] * 1.5)
           

            # Title per subplot if provided
            
            ax.set_title(col, fontsize=14, fontweight="bold")

             # Hide x labels except bottom plot (optional)
            if i < len(cols) - 1:
                ax.tick_params(labelbottom=False)
            
        fig.tight_layout()
        #%%
        fig.canvas.draw()
        fig.canvas.flush_events()
        img = np.array(fig.canvas.renderer._renderer)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        return img,fig







        # #####################
        # #set the axis
        # plt.axes(ax1);
        # ax1.get_xaxis().set_visible(False);
        # ax1.get_yaxis().set_visible(False);
        
        # # showing image
        # plt.imshow(self.frame);
        # fig.canvas.draw()
        # fig.canvas.flush_events()
        # #%%Plot data
        # plt.axes(ax2);
        # plt.plot(self.Selected_frame[~np.isnan(self.Selected_data)], self.Selected_data[~np.isnan(self.Selected_data)], color= 'red',linewidth=2);
        # if any(self.data_to_plot_left):
        #    plt.plot(self.Selected_frame[~np.isnan(self.Selected_data)], self.Selected_data_left[~np.isnan(self.Selected_data)], color= 'blue',linewidth=2);
        
        # plt.axvline(x= self.counter_frame,color = 'black',linestyle='dashed', linewidth=2)
        # plt.axhline(y = self.upper, color = 'b', linestyle ='dashed', linewidth = 2)
        # plt.axhline(y = self.lower, color = 'b', linestyle ='dashed', linewidth = 2)
        
        # plt.ylim((self.lower)*1.5,(self.upper)*1.5)
        # #%% add title
        # plt.title(self.title,fontsize=18, color='blue', fontweight='bold')
        # #%%
        # fig.canvas.draw()
        # fig.canvas.flush_events()
        # img = np.array(fig.canvas.renderer._renderer)
        # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        # return img,fig
        
        
#%% Static methods
       
    '''
    Create subplots on a given figure
    return figure and axis
    '''
    @staticmethod
    def CreateSubplots(n_plots):
            # total rows: image + n_plots
        fig = plt.figure(figsize=(20, 20))
        gs = fig.add_gridspec(nrows=1 + n_plots, ncols=1, height_ratios=[2] + [1] * n_plots)

        ax_img = fig.add_subplot(gs[0, 0])
        ax_list = [fig.add_subplot(gs[i + 1, 0]) for i in range(n_plots)]

        return ax_img, ax_list, fig
