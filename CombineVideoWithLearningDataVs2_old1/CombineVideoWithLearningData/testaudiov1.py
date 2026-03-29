# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 12:23:19 2024

@author: Administrator
"""

import numpy as np
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip
import librosa



# Load the video file
input_video = 'F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT.avi'
temp_audio_file  = 'F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT.wav'
# Load the video file
video_clip = VideoFileClip(input_video)

# Extract the audio
audio_clip = video_clip.audio

# Write the audio to a temporary file
#temp_audio_file = "temp_audio.wav"
audio_clip.write_audiofile(temp_audio_file)

# Load the audio file using librosa
audio_data, original_sample_rate = librosa.load(temp_audio_file, sr=None)



# Define the target sample rate
target_sample_rate = 24  # For example, 16 kHz

# Resample the audio data
resampled_audio_data = librosa.resample(audio_data, orig_sr=original_sample_rate, target_sr=target_sample_rate)

# Plot the original audio waveform
plt.figure(figsize=(14, 5))
plt.subplot(2, 1, 1)
plt.plot(audio_data)
plt.title('Original Audio Waveform')
plt.xlabel('Sample')
plt.ylabel('Amplitude')

# Plot the resampled audio waveform
plt.subplot(2, 1, 2)
plt.plot(resampled_audio_data)
plt.title('Resampled Audio Waveform')
plt.xlabel('Sample')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()

# Clean up
audio_clip.close()
video_clip.close()