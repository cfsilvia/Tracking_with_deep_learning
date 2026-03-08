# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 11:22:27 2024

@author: Administrator
"""

from moviepy.editor import VideoFileClip

# Load the video file
input_video = 'F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT.avi'
output_audio = 'F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT.mp3'
video_clip = VideoFileClip(input_video)

# Extract the audio
audio_clip = video_clip.audio

# Save the audio to a file
audio_clip.write_audiofile(output_audio)

# Close the clips
audio_clip.close()
video_clip.close()