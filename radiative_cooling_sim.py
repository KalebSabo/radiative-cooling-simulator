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
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.integrate import quad

if __name__ == "__main__":
    print("Radiative Cooling Simulator Module Loaded")


    # Stefan-Boltzmann Constant
    sigma = 5.670374419e-8  # W/m^2K^4

    def emitted_power(emissivity, temperature):
        """
        Radiated power from surface (graybody assumption).
        
        Parameters:
        emissivity (float): Emissivity of the material (0 to 1).
        temperature (float): Temperature in Kelvin.
        
        Returns:
        float: emitted power in W/m^2.
        """
        return emissivity * sigma * temperature**4

    def planck_spectral_radiance(wavelength, T):
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
        
        exponent = (h * c) / (wavelength * k * T)
        if exponent > 700:  # Prevent overflow in exp
            return np.zeros_like(wavelength)
        
        numerator = 2.0 * h * c**2
        denominator = (wavelength**5) * (np.exp((h * c) / (wavelength * k * T)) - 1)
        
        return numerator / denominator

    def equilibrium_temperature(emissivity_ir, absorptivity_solar, solar_flux, ambient_temp=3.0):
        """
        Calculate the equilibrium temperature of a material.
        
        Parameters:
        emissivity (float): Emissivity of the material (0 to 1).
        ambient_temperature (float): Ambient temperature in Kelvin.
        absorbed_power (float): Power absorbed by the material in W/m^2.
        
        Returns:
        float: Equilibrium temperature in Kelvin.
        """
        def balance(T):
            emitted = emitted_power(emissivity_ir, T)
            absorbed_env = emissivity_ir * sigma * ambient_temperature**4
            absorbed_solar = absorptivity_solar * solar_flux
            return emitted - (absorbed_solar + absorbed_env)
        
        
        T_guess = 300.0 # Initial guess for temperature in Kelvin        
        return fsolve(balance, T_guess)[0]



