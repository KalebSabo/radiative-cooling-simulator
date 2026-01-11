'''

Space Radiation Simulator
----------------------------------------
Inspired by SpaceX heat shields and future space computing

By: Kaleb Sabo

''' 

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from radiative_cooling_sim import (
    equilibrium_temperature, 
    emitted_power,
    MATERIALS,
    ORBIT_SCENARIOS,
    K as STEFAN_BOLTZMANN_CONSTANT
)



# -------------------------- Streamlit App --------------------------

st.set_page_config(page_title="Space Radiative Cooling Simulator", layout="wide")
st.title("Space Radiative Cooling Simulator")
st.markdown("""
Explore how spacecraft and orbital data centers stay cool in vacuum using only radiation.  
Inspired by SpaceX heat shields and future space computing.
""")

# -------------------------- Settings --------------------------

st.sidebar.header("Settings")
mode = st.sidebar.radio("Choose Mode", ["Orbital Environment", "Custom Settings"])


selected_materials = None

if mode == "Orbital Environment":
    st.sidebar.subheader("Orbital Environment Scenarios", divider=True)
    scenario = st.sidebar.selectbox("Select Orbital Environment", options=list(ORBIT_SCENARIOS.keys()))
    solar_flux = ORBIT_SCENARIOS[scenario]
    st.sidebar.write(f"**Solar Input Power:** {solar_flux:.1f} W/m²")

    selected_materials = st.sidebar.multiselect(
        "Select materials to compare",
        options=list(MATERIALS.keys()),
        default=["White Paint (Z93-type)", "SpaceX Starship Tile (black coating)", "Ideal Radiator"]
    )

    if not selected_materials:
        st.sidebar.warning("Please select at least one material to compare.")
        st.stop()

else:  # Custom Settings
    st.sidebar.subheader("Custom Material")
    emissivity_ir = st.sidebar.slider("IR Emissivity (how well it radiates heat)", 0.0, 1.0, 0.90, 0.01)
    absorptivity_solar = st.sidebar.slider("Solar Absorptivity (how much sunlight it absorbs)", 0.0, 1.0, 0.20, 0.01)
    solar_flux = st.sidebar.slider("Solar Input Power (W/m²)", 0.0, 1400.0, 342.0, 10.0)
    selected_materials = ["Custom Material"]  # This is now always set

# -------------------------- Equilibrium Temperature Display --------------------------

if mode == "Orbital Environment" or mode == "Custom Settings":

    st.subheader("Equilibrium Temperatures")
    st.markdown('''##### Assuming radiative cooling only (no conduction or convection in vacuum) 
                the equilibrium temperature is where emitted thermal power balances absorbed solar and environmental radiation.
    ''')
    # ---------------- Equilibrium Temperature Calculation --------------------------

    cols = st.columns(len(selected_materials))
    results = {}

    for i, mat_name in enumerate(selected_materials):
        with cols[i]:
            if mat_name == "Custom Material":
                e_ir = emissivity_ir
                a_solar = absorptivity_solar
                name_display = "Custom Material"
            else:
                props = MATERIALS[mat_name]
                e_ir = props["emissivity_ir"]
                a_solar = props["absorptivity_solar"]
                name_display = mat_name

            T_eq = equilibrium_temperature(e_ir, a_solar, solar_flux)
            T_celsius = T_eq - 273.15

            ratio = a_solar / e_ir if e_ir > 0 else 999

            st.metric(label=name_display, value=f"{T_celsius:+.1f} °C", delta=f"{T_eq:.0f} K")
            
            if ratio < 0.3:
                st.success(f"Absorptivity/Emissivity ratio: {ratio:.2f}, Excellent cooling!")
            elif ratio > 0.7:
                st.warning(f"Absorptivity/Emissivity ratio: {ratio:.2f}, Gets hot in sunlight")
            else:
                st.info(f"Absorptivity/Emissivity ratio: {ratio:.2f}")

            results[mat_name] = {"T_eq": T_eq, "emissivity_ir": e_ir, "absorptivity_solar": a_solar}

    # -------------------------- Power Balance Graph --------------------------

    st.markdown("### Power Balance Graph")
    fig, ax = plt.subplots(figsize=(10, 6))
    temps_k = np.linspace(150, 700, 500)
    temps_c = temps_k - 273.15

    colors = plt.cm.tab10.colors

    for i, (name, res) in enumerate(results.items()):
        power_emitted = emitted_power(res["emissivity_ir"], temps_k)
        power_absorbed = res["absorptivity_solar"] * solar_flux + res["emissivity_ir"] * STEFAN_BOLTZMANN_CONSTANT * 3**4

        color = colors[i % len(colors)]

        ax.plot(temps_c, power_emitted, label=f"{name} — Radiated Power", linewidth=2, color=color)
        ax.axhline(power_absorbed, linestyle="--", alpha=0.8, label=f"{name} — Absorbed Power", color=color)

    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Power (W/m²)")
    ax.set_title("Radiated vs Absorbed Power\n(Crossing point = equilibrium temperature)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)        

else:
    st.error("Invalid mode selected.")

    