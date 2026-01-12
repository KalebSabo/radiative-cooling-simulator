'''
Space Radiative Cooling Simulator
----------------------------------------
Explore how spacecraft stay cool in vacuum using only radiation.  
Inspired by SpaceX heat shields and future space computing.

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
graph_view = st.sidebar.checkbox(
    "Zoom on Intersections",
    value=False,
    help="Centers the graph on equilibrium crossing points for easier comparison"
)
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

selected_materials = None
solar_flux = None

if mode == "Orbital Environment":
    st.sidebar.subheader("Orbital Environment Scenarios", divider=True)
    scenario = st.sidebar.selectbox("Select Orbital Environment", options=list(ORBIT_SCENARIOS.keys()), index=2)
    solar_flux = ORBIT_SCENARIOS[scenario]
    st.sidebar.write(f"**Solar Input Power:** {solar_flux:.1f} W/m²")

    selected_materials = st.sidebar.multiselect(
        "Select materials to compare",
        options=list(MATERIALS.keys()),
        default=["White Paint (Z93-type)", "SpaceX Starship Tile (black coating)", "Optical Solar Reflector (OSR)"]
    )

    if not selected_materials:
        st.sidebar.warning("Please select at least one material to compare.")
        st.stop()

else:  # Custom Settings
    st.sidebar.subheader("Custom Material")
    emissivity = st.sidebar.slider("IR Emissivity (how well it radiates heat)", 0.0, 1.0, 0.90, 0.01)
    absorptivity = st.sidebar.slider("Solar Absorptivity (how much sunlight it absorbs)", 0.0, 1.0, 0.20, 0.01)
    solar_flux = st.sidebar.slider("Solar Input Power (W/m²)", 0.0, 1400.0, 342.0, 10.0)
    selected_materials = ["Custom Material"]

# -------------------------- Equilibrium Temperatures --------------------------

st.subheader("Equilibrium Temperatures")
st.markdown("""
Assuming radiative cooling only (no conduction or convection in vacuum),  
the equilibrium temperature is where emitted power balances absorbed solar and environmental radiation.
""")
if simulate_degradation:
    st.info("**Fresh** = new material properties. **Degraded** = after years of space exposure (increased absorptivity, slight emissivity loss).")

cols = st.columns(len(selected_materials))
results = {}

for i, mat_name in enumerate(selected_materials):
    with cols[i]:
        # Fresh properties
        if mat_name == "Custom Material":
            emissivity_fresh = emissivity
            absorptivity_fresh = absorptivity
        else:
            props = MATERIALS[mat_name]
            emissivity_fresh = props["emissivity_ir"]
            absorptivity_fresh = props["absorptivity_solar"]

        # Fresh equilibrium
        T_eq_fresh = equilibrium_temperature(emissivity_fresh, absorptivity_fresh, solar_flux)
        T_c_fresh = T_eq_fresh - 273.15

        st.metric(
            label=f"{mat_name} (Fresh)",
            value=f"{T_c_fresh:+.1f} °C",
            delta=f"{T_eq_fresh:.0f} K"
        )

        # Degraded (if enabled)
        emissivity_deg = emissivity_fresh
        absorptivity_deg = absorptivity_fresh
        if simulate_degradation:
            emissivity_deg, absorptivity_deg = get_degraded_properties(mat_name, years_exposed)
            T_eq_deg = equilibrium_temperature(emissivity_deg, absorptivity_deg, solar_flux)
            T_c_deg = T_eq_deg - 273.15

            delta_temp = T_c_deg - T_c_fresh
            delta_str = f"{delta_temp:+.1f} °C change"

            st.metric(
                label=f"{mat_name} (Degraded)",
                value=f"{T_c_deg:+.1f} °C",
                delta=delta_str,
                delta_color="normal" if delta_temp >= 0 else "inverse"
            )

        # Store for graph
        results[mat_name] = {
            "emissivity": emissivity_fresh,
            "absorptivity": absorptivity_fresh,
            "emissivity_deg": emissivity_deg,
            "absorptivity_deg": absorptivity_deg
        }

# -------------------------- Power Balance Graph --------------------------

st.markdown("### Power Balance Graph")

fig, ax = plt.subplots(figsize=(12, 7))
temps_k = np.linspace(100, 800, 800)  # Wide range for visibility
temps_c = temps_k - 273.15

colors = plt.cm.tab10.colors

# Collect all absorbed powers to compute stats (for zoom)
absorbed_powers = []
for name, res in results.items():
    p_abs = res["absorptivity"] * solar_flux + res["emissivity"] * STEFAN_BOLTZMANN_CONSTANT * 3**4
    absorbed_powers.append(p_abs)
    
    if simulate_degradation:
        p_abs_deg = res["absorptivity_deg"] * solar_flux + res["emissivity_deg"] * STEFAN_BOLTZMANN_CONSTANT * 3**4
        absorbed_powers.append(p_abs_deg)

# Set y-limits based on toggle
if graph_view and absorbed_powers:  # Zoom mode
    avg_absorbed = np.mean(absorbed_powers)
    y_range = max(absorbed_powers) - min(absorbed_powers)
    y_margin = max(150, y_range * 0.6)  # Adaptive, at least 150 W/m² padding
    y_min = max(0, avg_absorbed - y_margin)
    y_max = avg_absorbed + y_margin
else:  # Full view
    y_min = 0
    y_max = None  # Let matplotlib auto-scale (or set a high value if needed)

# Plot loop
for i, (name, res) in enumerate(results.items()):
    color = colors[i % len(colors)]

    # Fresh
    p_emitted = emitted_power(res["emissivity"], temps_k)
    p_absorbed = res["absorptivity"] * solar_flux + res["emissivity"] * STEFAN_BOLTZMANN_CONSTANT * 3**4
    ax.plot(temps_c, p_emitted, label=f"{name} – Fresh Radiated", color=color, linewidth=2.2)
    ax.axhline(p_absorbed, color=color, linestyle="--", alpha=0.8, label=f"{name} – Fresh Absorbed")

    # Degraded
    if simulate_degradation:
        p_emitted_deg = emitted_power(res["emissivity_deg"], temps_k)
        p_absorbed_deg = res["absorptivity_deg"] * solar_flux + res["emissivity_deg"] * STEFAN_BOLTZMANN_CONSTANT * 3**4
        ax.plot(temps_c, p_emitted_deg, label=f"{name} – Degraded Radiated", color=color, linestyle=":", linewidth=2)
        ax.axhline(p_absorbed_deg, color=color, linestyle="-.", alpha=0.6, label=f"{name} – Degraded Absorbed")

ax.set_xlabel("Temperature (°C)", fontsize=11)
ax.set_ylabel("Power (W/m²)", fontsize=11)
ax.set_title("Radiated vs Absorbed Power (Fresh vs Degraded)")
ax.set_ylim(y_min, y_max)  # Apply zoom or full view

ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0., fontsize=9)
ax.grid(True, alpha=0.3, linestyle='--')

plt.tight_layout()
st.pyplot(fig)