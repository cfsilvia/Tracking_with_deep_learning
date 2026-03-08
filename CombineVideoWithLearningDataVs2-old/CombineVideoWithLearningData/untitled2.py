# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 11:40:59 2024

@author: Administrator
"""

import numpy as np
import matplotlib.pyplot as plt

# Generate a sample signal for demonstration
fs = 500  # Sampling frequency
t = np.linspace(0, 1, fs)
signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)

# Plot the signal
plt.figure(figsize=(10, 4))
plt.plot(t, signal)
plt.title('Time-Domain Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid()
plt.show()

from scipy.fft import fft, fftfreq

# Compute the Fast Fourier Transform (FFT)
N = len(signal)
yf = fft(signal)
xf = fftfreq(N, 1 / fs)

# Plot the frequency spectrum
plt.figure(figsize=(10, 4))
plt.plot(xf, np.abs(yf))
plt.title('Frequency-Domain Signal')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude')
plt.grid()
plt.show()

from scipy.signal import stft

f, t, Zxx = stft(signal, fs, nperseg=100)

plt.figure(figsize=(10, 4))
plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [s]')
plt.colorbar(label='Amplitude')
plt.show()

import pywt

coeffs, freqs = pywt.cwt(signal, np.arange(1, 128), 'morl', sampling_period=1/fs)

plt.figure(figsize=(10, 4))
plt.imshow(np.abs(coeffs), extent=[0, 1, 1, 128], cmap='PRGn', aspect='auto',
           vmax=abs(coeffs).max(), vmin=-abs(coeffs).max())
plt.title('Wavelet Transform (CWT)')
plt.xlabel('Time [s]')
plt.ylabel('Frequency [Hz]')
plt.colorbar(label='Amplitude')
plt.show()