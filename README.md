[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://radiative-cooling-simulator-kalebsabo.streamlit.app/)

# Space Radiative Cooling Simulator 🌌

A interactive web tool for simulating radiative cooling in space environments. Explore how objects reject heat via thermal radiation in vacuum.

## Demo / Live App

[Try it live here!](https://radiative-cooling-simulator-kalebsabo.streamlit.app/)

## Features

- Features templates for different solar events and material/paint
- In Custom Mode, Adjust parameters manually like emissivity, absorptivity and solar flux
- Adjustable plots of cooling curves and equilibrium temperatures
- Based on Stefan-Boltzmann's and Planck's laws of blackbody radiation. 
- Educational explanations and tooltips

Notes on equations and derivations in `notes/` folder.

- [General Notes](01_Notes/Terms_Concepts.md)
- [Planck's Law](01_Notes/01_Plancks_Law.md)
- [Stefan-Boltzmann Law](01_Notes/02_Stefon_Boltzmann_Law.md)

![Planck's Law Graph](02_Images/planck_radiation.png)

## References & Resources

- [Link to REFERENCES file](REFERENCES.md)

Special thanks to open NASA resources and the aerospace thermal control community for making this knowledge accessible.

## Installation

```bash
git clone https://github.com/KalebSabo/radiative-cooling-simulator.git
cd radiative-cooling-simulator  
pip install -r requirements.txt 
python radiative_cooling_sim.py  # Run basic simulation
streamlit run app.py  # Interactive dashboard
