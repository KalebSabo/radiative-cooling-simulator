# Radiative Cooling Simulation
#
#
### 
# 
# Computes net radiative power (using Stefan-Boltzmann's Law) 
# Integrates Planck's Law of Spectral Radiance 
# Includes functions for equilibrium temperature solving,
# material presets of differing emissivity 
# 
###

import numpy as np
import matplotlib as plt
import scipy as sp

# Stefan-Boltzmann Constant
sigma = 5.670374419e-8  # W/m^2K^4

def stefan_boltzmann_radiative_power(emissivity, temperature):
    """
    Calculate the net radiative power using Stefan-Boltzmann's Law.
    
    Parameters:
    emissivity (float): Emissivity of the material (0 to 1).
    temperature (float): Temperature in Kelvin.
    
    Returns:
    float: Net radiative power in W/m^2.
    """
    return emissivity * sigma * temperature**4

def planck_spectral_radiance(wavelength, temperature):
    """
    Calculate the spectral radiance using Planck's Law.
    
    Parameters:
    wavelength (float): Wavelength in meters.
    temperature (float): Temperature in Kelvin.
    
    Returns:
    float: Spectral radiance in W/m^2/sr/m.
    """
    h = 6.62607015e-34  # Planck's constant in J·s
    c = 3.0e8           # Speed of light in m/s
    k = 1.380649e-23    # Boltzmann's constant in J/K
    
    numerator = 2.0 * h * c**2
    denominator = (wavelength**5) * (np.exp((h * c) / (wavelength * k * temperature)) - 1)
    
    return numerator / denominator

def equilibrium_temperature(emissivity, ambient_temperature, absorbed_power):
    """
    Calculate the equilibrium temperature of a material.
    
    Parameters:
    emissivity (float): Emissivity of the material (0 to 1).
    ambient_temperature (float): Ambient temperature in Kelvin.
    absorbed_power (float): Power absorbed by the material in W/m^2.
    
    Returns:
    float: Equilibrium temperature in Kelvin.
    """
    def power_balance(temp):
        return stefan_boltzmann_radiative_power(emissivity, temp) - absorbed_power
    
    
    initial_guess = ambient_temperature
    equilibrium_temp = sp.fsolve(power_balance, initial_guess)[0]
    
    return equilibrium_temp



