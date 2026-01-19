# **Terms and Concepts**
- The goal of this file is to explain common terminology in space engineering etc. 


# Heat Exchanger Terminology

### Heat Exchangers
- Designed to transfer thermal energy between two or more fluids (without allowing them to mix)
- Utilize principles in Conduction/Convection/Radiation
- Classified by Flow Arrangement: 
    - Parallel/Co-Current Flow
    - Counter/Counter-Current Flow
    - Crossflow


### Conduction
- Transfer of heat through *Direct molecular/atomic action* 
- Governed by Fourier’s law: 
    - $  q = -k A \frac{dT}{dx}  $
        -  $  q  $ = heat transfer rate,
        -  $  k  $ = thermal conductivity,
        -  $  A  $ = cross-sectional area,
        -  $  \frac{dT}{dx}  $ = temperature gradient.
- i.e. Heat moving through a metal bar

### Convection
- Transfer of heat through the *bulk movement of a fluid or gas*
- Governed by Newton’s law of cooling: 
    - $  q = h A (T_s - T_f)  $
        - $  h  $ = convective heat transfer coefficient,
        - $  A  $ = surface area,
        - $  T_s  $ = surface temperature,
        - $  T_f  $ = fluid temperature.
- i.e. Boiling water (Hot water rises)

### Radiative
- Transfer of heat via *electromagnetic waves* (does not require a medium)
- When a body, above absolute zero, emits/absorbs energy as electromagnetic waves
- ALL objects emit and absorb thermal energy continuously 
- Stefan-Boltzmann Law (for blackbody):
    - $q = \sigma A T^4$
        - $  q  $ = net heat transfer rate (W)
        - $  \sigma  $ = Stefan-Boltzmann constant = $  5.67 \times 10^{-8}  $ W/m²·K⁴
        - $  A  $ = surface area (m²)
        - $  T  $ = absolute temperature (K)
- i.e. black paint absorbing thermal electromagnetic waves from the sun. 

### Number of Transfer Units (NTU)
- dimensionless, used to quantify the heat transfer potential between two fluids
    - NTU = $\frac{U A}{C_{\min}}$
        - $U$ : **Overall heat transfer coefficient** (W/m²·K), which accounts for the thermal resistance between the fluids.
        - $A$ : **Heat transfer surface area** (m²).
        - $C_{\min}$ : The **smaller of the two fluid heat capacity rates** ($C$ = $m$ × $c_p$, where $m$ is mass flow rate and $c_p$ is specific heat capacity).

### Capacity Ratio 
- dimensionless, used to characterize the thermal imbalance between two fluids 
    - $C_r = \frac{C_{\min}}{C_{\max}}$
        - $C_{\min}$: The smaller heat capacity rate (W/K or J/s·K).
        - $C_{\max}$: The larger heat capacity rate.
        - Where the heat capacity rate $C$ for each fluid is $C = m \cdot c_p  $, with $m$ being the mass flow rate (kg/s) and $c_p$ the specific heat capacity (J/kg·K).
- $C_r$ ranges from 0 to 1:

- $C_r$ = 0: Occurs when one fluid has an infinite capacity rate (e.g., in condensers or evaporators where phase change makes effective C infinite). The maximum heat transfer is limited only by the other fluid.
- $C_r$ = 1: Balanced capacities; both fluids experience similar temperature changes.
Values in between indicate asymmetry, where the fluid with higher C (often the coolant) changes temperature less.

### Practical Application

- **Design Impact**: If $C_r$ is low, the exchanger can achieve near-ideal performance with moderate NTU (i.e. smaller size or lower $U$ $A$). High $C_r$ requires larger NTU for the same heat exchanger effectiveness.

- **In Space Contexts**: Space heat exchangers (e.g., on the ISS) often operate with $C_r$ around 0.5–0.8 to balance efficiency and mass. Microgravity doesn't directly alter $C_r$ but affects the heat transfer coefficients (h or U) that feed into NTU.

- **Calculation Tip**: Always identify $C_{\min}$ and $C_{\max}$ from the fluids' properties and flows. If they're equal, $C_r$ = 1, and the maximum temperature change is symmetric.

# Data Center Terminology

### Server
- *Essentially a computer that serves others over a network*. Services that range from holding, processing or transfering data.
    - Types of Servers:
        - Web 
        - Database
        - File
        - Mail
        - Application
        - Game
        - Print
        - DNS
        - Media

### Hardware Server Form Factor

#### Tower Server
- Like a desktop PC tower. Affordable for home/small business.
- Dell or HP tower. 

#### Rack Server
- Standard 19-inch rack. Compact/Stackable. 1U/2U Servers from IBM or Cisco. 
- U == height units, 1U == 1.75 in or 44.45mm

#### Blade Server
- Even more compact. multiple thin 'blades' inside a shared chasis w/ shared power/cooling. 
- HPE BladeSystem or Dell PowerEdge

#### Mainframe Server
- Massive, high-reliability. Huge workloads (like banking).
- IBM zSeries

#### Micro Server
- Small, Low-power. Light tasks.
- Raspberry Pi, Intel NUC

# Materials

### MLI - Multi-Layer Insulation
- This is a type of thermal insulation used on spacecraft. It consists of multiple thin layers of reflective material (usually metallized plastic films) separated by low-conductivity spacers. MLI primarily reduces heat loss/gain by thermal radiation in vacuum (where convection and conduction are minimal). It's one of the most common passive thermal control methods for satellites, probes, and cryogenic systems

### OSR - Optical Solar Reflector
- Specialized thermal control components used on spacecraft to manage temperature in the vacuum of space. They are essentially high-performance mirrors designed to reflect most incoming solar radiation (low solar absorptivity, α) while efficiently emitting heat as infrared radiation (high thermal emissivity, ε). This combination makes OSRs one of the best passive solutions for radiative cooling on satellites, probes, and orbital structures

### PET - Polyethylene Terephthalate
- A type of polyester film (commonly known by trade names like Mylar). It's used as a base substrate in MLI blankets because it's lightweight, strong, and can be easily metallized (e.g., aluminized) for high reflectivity. Pure PET has very low thermal emissivity, which is why it's often coated.

### FEP - Fluorinated Ethylene Propylene
- A fluoropolymer (a type of Teflon-like material) used as a coating or outer layer in MLI blankets. FEP is applied over metallized films (especially on the outer layers) for protection against atomic oxygen erosion, UV radiation, and environmental degradation in space. It has excellent thermal stability, low outgassing, and good optical properties (low solar absorptivity and high infrared emissivity in some configurations).

