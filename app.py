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
    get_degraded_properties,
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
    scenario = st.sidebar.selectbox("Select Orbital Environment", 
                                    options=list(ORBIT_SCENARIOS.keys()))
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

    simulate_degradation = st.sidebar.checkbox(
    "Simulate Degradation Over Time",
    value=False,
    help="Shows how material properties degrade due to space radiation exposure"
    )

    years_exposed = 0.0
    if simulate_degradation:
        years_exposed = st.sidebar.slider(
            "Years of Exposure in Orbit",
            min_value=0.0,
            max_value=15.0,
            value=0.0,
            step=0.5,
            format="%.1f years"
        )

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
            # Base (fresh) properties
            if mat_name == "Custom Material":
                emissivity = emissivity_ir
                absorptivity = absorptivity_solar
            else:
                props = MATERIALS[mat_name]
                emissivity = props["emissivity_ir"]
                absorptivity   = props["absorptivity_solar"]
        
        # Fresh equilibrium
        T_eq_fresh = equilibrium_temperature(emissivity, absorptivity, solar_flux)
        T_c_fresh  = T_eq_fresh - 273.15
        
        # Show fresh metric
        delta_fresh = f"{T_eq_fresh:.0f} K"
        label = f"{mat_name} (Fresh)"
        if simulate_degradation:
            label += f" ({years_exposed:.1f} yr)"
        
        st.metric(
            label=label,
            value=f"{T_c_fresh:+.1f} °C",
            delta=delta_fresh
        )
        
        # Degraded properties & metric (if enabled)
        if simulate_degradation:
            emissivity_deg, absorptivity_deg = get_degraded_properties(mat_name, years_exposed)
            T_eq_deg = equilibrium_temperature(emissivity_deg, absorptivity_deg, solar_flux)
            T_c_deg  = T_eq_deg - 273.15
            
            delta_temp = T_c_deg - T_c_fresh
            delta_str  = f"{delta_temp:+.1f} °C change"
            
            st.metric(
                label=f"{mat_name} (Degraded)",
                value=f"{T_c_deg:+.1f} °C",
                delta=delta_str,
                delta_color="normal" if delta_temp >= 0 else "inverse"
            )
        
        # Store for graph
        results[mat_name] = {
            "emissivity": emissivity,
            "absorptivity": absorptivity,
            "T_eq": T_eq_fresh,
            "emissivity_deg": emissivity_deg if simulate_degradation else emissivity,
            "absorptivity_deg": absorptivity_deg if simulate_degradation else absorptivity,
            "T_eq_deg": T_eq_deg if simulate_degradation else T_eq_fresh
        }

# --- Power Balance Graph (enhanced with degraded lines) ---
    st.markdown("### Power Balance Graph")
    fig, ax = plt.subplots(figsize=(10, 6))
    temps_k = np.linspace(150, 700, 500)
    temps_c = temps_k - 273.15

    colors = plt.cm.tab10.colors

    for i, (name, res) in enumerate(results.items()):
        # Fresh
        p_emitted = emitted_power(res["emissivity"], temps_k)
        p_absorbed = res["absorptivity"] * solar_flux + res["emissivity"] * STEFAN_BOLTZMANN_CONSTANT * 3**4
        
        color = colors[i % len(colors)]
        ax.plot(temps_c, p_emitted, label=f"{name} Fresh", color=color, linewidth=2)
        ax.axhline(p_absorbed, color=color, linestyle="--", absorptivity=0.7)
        
        # Degraded (dashed)
        if simulate_degradation:
            p_emitted_deg = emitted_power(res["emissivity_deg"], temps_k)
            p_absorbed_deg = res["absorptivity_deg"] * solar_flux + res["emissivity_deg"] * STEFAN_BOLTZMANN_CONSTANT * 3**4
            
            ax.plot(temps_c, p_emitted_deg, label=f"{name} Degraded", color=color, linestyle=":", linewidth=2)
            ax.axhline(p_absorbed_deg, color=color, linestyle="-.", absorptivity=0.5)

    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Power (W/m²)")
    ax.set_title("Radiated vs Absorbed Power (Fresh vs Degraded)")
    ax.legend()
    ax.grid(True, absorptivity=0.3)
    st.pyplot(fig)
        