# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 07:59:28 2024

@author: Administrator

Class to read audio and add audio
"""

import os
import ffmpeg

class TreatAudio:
    def  __init__(self,original_video,_outputVideo):
        self.file_original_video = original_video
        self.file_video_landmarks = _outputVideo
        
    '''
    input: original video
    output : extract audio
    '''
    def ExtractAudio(self):
       #get path of the file
       file_path =  os.path.dirname(self.file_original_video)
       audio_path = os.path.join(file_path, "extracted_audio.wav")

      # Extract audio using ffmpeg
       ffmpeg.input(self.file_original_video).output(audio_path, acodec='pcm_s16le').run(overwrite_output=True)

       return audio_path, file_path
       
   
    
    '''
    input: video, audio
    output : video with audio
    '''
    def AddAudio(self, audio_path, file_path):
        output_path = file_path + '/' + 'video_with_audio.mp4'
        # Define video and audio input streams
        video_input = ffmpeg.input(self.file_video_landmarks)
        audio_input = ffmpeg.input(audio_path)
      # Merge video and audio using ffmpeg
         # Merge video and audio
        ffmpeg.output(
        video_input,
        audio_input,
        output_path,
        vcodec='copy',
        acodec='aac',
        strict='experimental'
    ).run(overwrite_output=True)


    '''
    Resume all files
    '''
    def  __call__(self):
       audio, file_path = self.ExtractAudio()
       self.AddAudio(audio, file_path)