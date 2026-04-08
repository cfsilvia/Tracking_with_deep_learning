# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 08:38:43 2023

@author: Administrator
"""

#Join data from pose estimation with behaviour table
'''
-Open behaviour data
-Concentrate in the column Time_Relative_sf, Behaviour and Event Typ
1)- To time table remove  the first time from every column 
2)- Look for the elapsed time from the beggining of the movie and begin with the behaviour observation.
input parameters: time 0 of the movie and time of the observer.
3)_ Add this time to the time
4)_Devide by 33fps to get frame - do new column
5)- Create a new table- extract data with start event and with stop event join Change the name of time and frame
6) add zero
7)-go to pose position. open the table
8)- go troug the first table add a new column behaviour equal nothing- mark between the start stop the relevant 
frames with the behaviour- for each mouse
'''


def main():
    #Settings
    pose_file = "F:/YaelShammaiData/AnnotationFromYael/C57 103-1mcut_Yolovs3_White.xlsx"
    behaviour_file = "F:/YaelShammaiData/AnnotationFromYael/20230806 social interaction BTBR-C57 + Balbc - BTBR 103-1m - Event Logs.xlsx"
    initial_time_video = "10:59:33.945"
    initial_time_observer = "11:27:16.470"

if __name__ == "__main__":
    main() 