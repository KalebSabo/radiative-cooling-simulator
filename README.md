[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://radiative-cooling-simulator-kalebsabo.streamlit.app/)

# Space Radiative Cooling Simulator 🌌

A interactive web tool for simulating radiative cooling in space environments. Explore how objects reject heat via thermal radiation in vacuum—perfect for aerospace engineering, physics education, and satellite thermal management.

## Demo / Live App

![SpaceRadiativeCoolingScreenshot](Images\SpaceRadiativeCoolingSimPic.png)  

[Try it live here!](https://radiative-cooling-simulator-kalebsabo.streamlit.app/)

## Features

- Features templates for different solar events and material/paint
- In Custom Mode, Adjust parameters manually like emissivity, absorptivity and solar flux
- Adjustable plots of cooling curves and equilibrium temperatures
- Based on Stefan-Boltzmann's and Planck's laws of blackbody radiation. 
- Educational explanations and tooltips

Notes on equations and derivations in `notes/` folder.

## Installation

```bash
git clone https://github.com/KalebSabo/radiative-cooling-simulator.git
cd radiative-cooling-simulator  
pip install -r requirements.txt 
python radiative_cooling_sim.py  # Run basic simulation
streamlit run app.py  # Interactive dashboard