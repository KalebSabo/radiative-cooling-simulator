# Planck's Law Graph
# This script plots Planck's Law for blackbody radiation at different temperatures.
# By: Kaleb Sabo

import numpy as np
import matplotlib.pyplot as plt

temperatures = [300, 500, 1800, 5800]  # Temperatures in Kelvin, room temp, red-hot, Starship, Sun
wavelengths = np.linspace(1e-9, 3e-6, 1000)  # Wavelengths from 1 nm to 100 mm

def planck_graph(wavelengths, temperatures): # Function to plot Planck's Law
    h = 6.626e-34  # Planck's constant in J·s
    c = 3e8        # Speed of light in m/s
    k = 1.381e-23  # Boltzmann's constant in J/K

    plt.figure(figsize=(10, 6))

    for T in temperatures:
        intensity = (2 * h * c**2) / (wavelengths**5) * (1 / (np.exp((h * c) / (wavelengths * k * T)) - 1))
        plt.plot(wavelengths * 1e9, intensity, label=f'T = {T} K')  # Convert wavelengths to nm for plotting

    # Highlight visible light spectrum (400-700 nm)
    plt.axvspan(400, 700, alpha=0.2, color='blue', label='Visible Light Spectrum')
    
    plt.title("Planck's Law for Blackbody Radiation")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Spectral Radiance (W·sr⁻¹·m⁻³)")
    plt.yscale('log')
    plt.xscale('log')
    plt.legend()
    plt.grid(True)
    plt.xlim(1, 1e8)  # Wavelength range in nm
    plt.ylim(1e-20, 1e15)  # Intensity range
    plt.savefig('./Images/planck_radiation.png', dpi=300, bbox_inches='tight')
    print("Plot saved as planck_radiation.png")
    plt.show()

planck_graph(wavelengths, temperatures)