"""

Radiative Cooling Simulator for Space Applications
----------------------------------------
Focused on vacuum conditions (orbital data centers, space applications).

By: Kaleb Sabo

"""

import numpy as np
from scipy.optimize import fsolve

print("Radiative Cooling Simulator Module Loaded")


# -------------------------- Constants --------------------------

SIGMA = 5.670374419e-8  # W/m^2K^4
H = 6.62607015e-34  # Planck's constant in J·s
C = 3.0e8           # Speed of light in m/s
K = 1.380649e-23    # Boltzmann's constant in J/K

# -------------------------- Core Functions --------------------------

def emitted_power(emissivity, T):
    """
    Radiated power from surface (graybody assumption).
    
    Parameters:
    emissivity (float): Emissivity of the material (0 to 1).
    temperature (float): Temperature in Kelvin.
    
    Returns:
    float: emitted power in W/m^2.
    """
    return emissivity * SIGMA * T**4

def planck_spectral_radiance(wavelength, T):
    """
    Calculate the spectral radiance using Planck's Law.
    
    Parameters:
    wavelength (float): Wavelength in meters.
    temperature (float): Temperature in Kelvin.
    
    Returns:
    float: Spectral radiance in W/m^2/sr/m.
    """
    
    # Prevent overflow
    exponent = (H * C) / (wavelength * K * T)
    if exponent > 700:  
        return np.zeros_like(wavelength)
    
    numerator = 2.0 * H * C**2
    denominator = (wavelength**5) * (np.exp((H * C) / (wavelength * K * T)) - 1)
    
    return numerator / denominator

def equilibrium_temperature(emissivity_ir, absorptivity_solar, solar_flux, ambient_temp=3.0):
    """
    Calculate the equilibrium temperature of a material.
    
    Parameters:
    emissivity_ir (float): Emissivity of the material (0 to 1).
    absorptivity_solar (float): Absorptivity of the material (0 to 1).
    solar_flux (float): Incident solar power in W/m^2.
    ambient_temperature (float): Ambient temperature in Kelvin.
    
    Returns:
    float: Equilibrium temperature in Kelvin.
    """
    def balance(T):
        emitted = emitted_power(emissivity_ir, T)
        absorbed_env = emissivity_ir * SIGMA * ambient_temp**4
        absorbed_solar = absorptivity_solar * solar_flux
        return emitted - (absorbed_solar + absorbed_env)
    
    
    T_eq = 300.0 # Initial guess for temperature in Kelvin        
    return fsolve(balance, T_eq)[0]

# -------------------------- Material Presets --------------------------

MATERIALS = {
"SpaceX Starship Tile (black coating)": {
    "emissivity_ir": 0.90, "absorptivity_solar": 0.85
},
"White Paint (Z93-type)": {
    "emissivity_ir": 0.90, "absorptivity_solar": 0.18
},
"White Paint (AZ93-type)": {
    "emissivity_ir": 0.88, "absorptivity_solar": 0.12
},
"Optical Solar Reflector (OSR)": {
    "emissivity_ir": 0.85, "absorptivity_solar": 0.10
},
"Polished Aluminum": {
    "emissivity_ir": 0.05, "absorptivity_solar": 0.12
},
"Ideal Radiator": {
    "emissivity_ir": 1.00, "absorptivity_solar": 0.00
},
"Black Paint": {
    "emissivity_ir": 0.95, "absorptivity_solar": 0.95
}
}

# -------------------------- Material Degradation Rates --------------------------

# Degradation rates per year in typical space environment (LEO/GEO average)
# Δα_s = change in solar absorptivity (usually increases = darkening)
# Δε   = change in thermal emissivity (usually decreases slightly)

MATERIAL_DEGRADATION_RATES = {
    "SpaceX Starship Tile (black coating)": {
        "delta_alpha_per_year": 0.005,    # Very stable black ceramic
        "delta_epsilon_per_year": -0.002  # Slight emissivity drop
    },
    "White Paint (Z93-type)": {
        "delta_alpha_per_year": 0.015,    # Classic Z-93 degrades noticeably
        "delta_epsilon_per_year": -0.005  # Minor emissivity loss
    },
    "White Paint (AZ93-type)": {
        "delta_alpha_per_year": 0.008,    # Improved version, slower degradation
        "delta_epsilon_per_year": -0.003
    },
    "Optical Solar Reflector (OSR)": {
        "delta_alpha_per_year": 0.003,    # Extremely stable (quartz/silver)
        "delta_epsilon_per_year": -0.001  # Almost no change
    },
    "Polished Aluminum": {
        "delta_alpha_per_year": 0.010,    # Surface oxidation/roughening
        "delta_epsilon_per_year": -0.010  # Emissivity drops as oxide forms
    },
    "Ideal Radiator": {
        "delta_alpha_per_year": 0.000,
        "delta_epsilon_per_year": 0.000   # Theoretical perfect - no degradation
    },
    "Black Paint": {
        "delta_alpha_per_year": 0.002,    # Already near maximum absorptivity
        "delta_epsilon_per_year": -0.008  # Slight emissivity loss from erosion
    }
}

# -------------------------- Example Orbit Scenarios --------------------------

ORBIT_SCENARIOS = {
"Deep Space (no sun)": 0.0,
"Earth Orbit Average": 1366 / 4,  # ~341.5 W/m² (solar constant / 4)
"Full Sun (sun-facing)": 1366.0,
"LEO Hot Case (albedo + Earth IR)": 800.0
}

# -------------------------- Material Degradation Rates --------------------------

DEGREDATION_RATES = {
"SpaceX Starship Tile (black coating)": 0.01,  # per year
"White Paint (Z93-type)": 0.005,
"White Paint (AZ93-type)": 0.005,
"Optical Solar Reflector (OSR)": 0.002,
"Polished Aluminum": 0.003,
"Ideal Radiator": 0.0,
"Black Paint": 0.01
}


# -------------------------- Demo --------------------------

if __name__ == "__main__":
    print("Radiative Cooling Simulator - Space Edition\n")
    
    for scenario_name, flux in ORBIT_SCENARIOS.items():
        print(f"{scenario_name} (Solar Flux: {flux:.1f} W/m²)")
        print("-" * 50)
        for name, props in MATERIALS.items():
            T_eq = equilibrium_temperature(
                props["emissivity_ir"], props["absorptivity_solar"], flux
            )
            print(f"{name:30} → T_eq = {T_eq - 273.15:+6.1f} °C ({T_eq:.0f} K)")
        print()