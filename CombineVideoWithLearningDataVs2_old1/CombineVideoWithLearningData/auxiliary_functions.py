# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:10:32 2024

@author: Administrator
"""
import pandas as pd
import numpy as np

class auxiliary_functions:
     
    """Reads an Excel file and returns the specified column."""
    def read_excel(middle_tube_y, middle_tube_x, input_excel, sheet_name, column_name,_upper_tube = 0, _lower_tube = 0):
      try:
        df = pd.read_excel(input_excel, sheet_name=sheet_name)
         #Convert comma string to list
        if isinstance(column_name, str):
            column_names = [c.strip() for c in column_name.split(",")]
        else:
            column_names = column_name


        # Check columns exist
        for col in column_names:
            if col not in df.columns:
                print(f"Column '{col}' does not exist in sheet '{sheet_name}'.")
                return None

        print("Fitting zero no detected landmarks")

        out = {}

        #data_fitted_middle_y = df['BMR_Middle_y'].replace(0, np.nan)
        data_fitted_middle_y = auxiliary_functions.fill_zeros_with_mean(df['BMR_Middle_y'])

        for col in column_names:
            data_fitted = auxiliary_functions.fill_zeros_with_mean(df[col])
            #%% Remove data which is outside the tube # Replace values greater than the threshold with NaN 
            data_fitted = data_fitted.mask(data_fitted > _lower_tube, np.nan) 
            data_fitted = data_fitted.mask(data_fitted < _upper_tube, np.nan)
            out[col] = data_fitted_middle_y - data_fitted

        result = pd.DataFrame(out)

        return result[column_names[0]] if len(column_names) == 1 else result

      except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return None

    '''
     Fitting the zero points with no detection
     input : the data frame from the snout
     output : data where the zero are replaced with the mean between the contigous values of the region
    '''
# Function to replace zeros with the mean of contiguous non-zero neighbors
    def fill_zeros_with_mean(series):
     data_fitted = series.copy()
     for idx in series.index:
        if series[idx] == 0:
            left_idx = idx - 1
            right_idx = idx + 1
            
            # Find non-zero neighbors
            while left_idx >= 0 and series[left_idx] == 0:
                left_idx -= 1
            while right_idx < len(series) and series[right_idx] == 0:
                right_idx += 1

            neighbors = []
            if left_idx >= 0:
                neighbors.append(series[left_idx])
            if right_idx < len(series):
                neighbors.append(series[right_idx])

            if neighbors:
                data_fitted[idx] = np.nanmean(neighbors) #for ignoring mean

     return data_fitted
