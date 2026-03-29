# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 10:26:25 2023

@author: Administrator
"""
import numpy as np
import pandas as pd
import glob
from dask_image.imread import imread
from natsort import natsorted

'''
This library treats the data from the napari to give the correct format
'''

'''
function to read the data from the rect for each image
Input: list of arrays. Each array save four points for each frame,
Ouput: pandas frame each row has number of frame x,y center rect and width large of the rectangle 
'''
class HelperFunctions:
    def __init__(self):
        #create an empty dataframe
        self.df = pd.DataFrame(columns = ['frame', 'x-center-rec','y-center-rec','width-rec','height-rec'])
        self.dataframepoints = pd.DataFrame()
        self.Total = pd.DataFrame()
        self.df1 = pd.DataFrame(columns = ['frame', 'x-center-rec','y-center-rec','width-rec','height-rec', 'filename'])
        self.size_list = []
    '''
    Create rectangle dataframe
    '''

    def GetRectangleInf(self,Data,mouse,im_path,PATH_FOLDER):
        
          #real size of the pictures
         size_list = getSize(im_path)
         
       #  print(size_list)
         count  = 0
         filenames = natsorted(glob.glob(im_path))

        
        # print(Data)
         while len(Data) > 0:
             #Remove first element of the list
             
             B = Data.pop(0)
             sizeP = size_list.pop(0)
             
             height = abs(B[3,1]-B[0,1])
             width = abs(B[2,2]-B[3,2])
             ycenter = (B[0,1]+B[2,1])/2
             xcenter = (B[0,2]+B[2,2])/2
            # print(xcenter)
            
             self.df1.loc[len(self.df1)] = {'frame' : B[0,0], 'x-center-rec' : xcenter, 'y-center-rec' : ycenter, 'width-rec' : width, 'height-rec' : height, 'filename':filenames[count]}
             #normalize[]
             self.df.loc[len(self.df)] = {'frame' : B[0,0], 'x-center-rec' : xcenter/sizeP[2], 'y-center-rec' : ycenter/sizeP[1], 'width-rec' : width/sizeP[2], 'height-rec' : height/sizeP[1]}
             count += 1
         
         filename = PATH_FOLDER  + '//' + mouse + '.csv'
         #print(filename)
         self.df1.to_csv(filename, sep=',', index=False, encoding='utf-8')
        # print(self.df)
    '''
    Create data frame for points
    '''
         
    def GetPointsInf(self,labels,points,LABELS):
        #convert numpy array into pandas array
        labelsframe= pd.DataFrame(labels['label'])
       # print('points')
        print(points)
        pointsframe = pd.DataFrame(points)
        print(pointsframe)
        print(labelsframe)
        aux_1 = pd.concat([pointsframe,labelsframe], axis = 1)
        print(aux_1)
        print(aux_1.columns)
        aux_1.columns = ['0','1','2','3']
        print(aux_1)
        aux_2 = aux_1.pivot(index = '0',columns = '3')
        print(aux_2)
       
        columnsnumber = auxiliary(LABELS)
        print(columnsnumber)
        
        self.dataframepoints = aux_2.iloc[:,columnsnumber]
        
        #in order to get the correct xy reorder the data
        self.dataframepoints = OrderData(self.dataframepoints)
        print('dataframepoints')
        print(self.dataframepoints)
        
    '''
    Join points with planes
    '''    
    def FusionData(self,PATH_FOLDER):
            print(self.df)
            self.Total = pd.concat([self.df,self.dataframepoints], axis = 1)

            path = PATH_FOLDER + '//test2.csv'
            self.Total.to_csv(path, sep=',', index=False, encoding='utf-8')
            print(self.Total)
        
        
    '''
    Conversion pandas to text 
    '''
    def ConverionPandastoText(self,PATH_FOLDER,shape,im_path):
        #get all the files
        output = GetFilenames(PATH_FOLDER)
        size_list = getSize(im_path)
        print(len(self.Total.index))
        for index in range(len(self.Total.index)):
            any_row = self.Total.iloc[index,self.Total.columns!='frame']
            print(any_row)
            #normalize the data
            shape = size_list.pop(0)
            print(shape)
            any_row = Normalize(any_row,shape)
            list_0 = any_row.values.tolist()
            
            any_row_as_string_0 = ' '.join([str(item) for item in list_0])
            #Replace '\n' with comma
            any_row_as_string = '0'+' '+ any_row_as_string_0 + "\n"
            #Get any row of dataframe as string
            #print(any_row_as_string_0)
            #save as txt file
            print("Here Silvia")
            print(output[index])
            file1 = open(output[index],"w")#write mode
            file1.write(any_row_as_string)
            file1.close()
    
'''

Auxiliary functions
'''

def auxiliary(LABELS):
        columnsnumber = []
        #create vector with numbers
        for index  in  range(0, len(LABELS)):
            columnsnumber.append(index)
            columnsnumber.append(index+len(LABELS))
        return columnsnumber
    
'''
#get all the files for text
input: folder name
output: list of filenames
'''

def GetFilenames(PATH_FOLDER):
    output = []
    #get all filenames of the images
    im_path = PATH_FOLDER + '//images//train//*.png'
    
    filenames = natsorted(glob.glob(im_path))
    
    for f in filenames:
       aux = PATH_FOLDER + '//labels//train//' + (((f.split('\\'))[1]).split('.'))[0] + '.txt'
       output.append(aux)
       
    return output
    
'''
Normalize the data with the width and height
input : data, w and h
output: return the normalized data
'''
def  Normalize(any_row,shape):
    
    for index in range(4,len(any_row)):
        if index % 2 == 0:
           any_row[index] = any_row[index]/shape[2]
        else:
           any_row[index] = any_row[index]/shape[1]
    return any_row

'''
Reorder the data in order to get correct x and y
'''
def OrderData(data):
    
   new = []
   for index in range(0,len(data.columns),2):
      new.append(index+1)
      new.append(index)
     
   data_new = data.iloc[:,new]
   
   return data_new

'''
Auxiliary functions
'''
'''
Get a list with the size of each picture
'''
def getSize(im_path):
    filenames = natsorted(glob.glob(im_path))
    size_list = []
    for f in filenames:
        aux_s = imread(f)
        size_p =aux_s.shape
        size_list.append(size_p)
    return size_list
