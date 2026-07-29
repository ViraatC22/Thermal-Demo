import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects

from thermodynamics import (
    MATERIALS,
    simulation_speed_factor,
    thermal_exchange_step,
)

# ==========================================
# CONFIGURATION & STYLING
# ==========================================
# Set up the Streamlit page configuration
st.set_page_config(
    page_title="Thermodynamics Demo",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI
# This block injects custom CSS to style the app, overriding some Streamlit defaults
# to create a cleaner, more educational look.
st.markdown("""
<style>
    /* Global Fonts & Colors */
    :root {
        --primary-color: #FF4B4B;
        --secondary-color: #1E88E5;
        --bg-color: #F8F9FA;
        --card-bg: #FFFFFF;
        --text-color: #31333F;
    }
    
    /* Main Container Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Cards for Layout */
    /* Defines the look of the custom cards used in the UI */
    .stCard {
        background-color: var(--card-bg);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #E0E0E0;
        margin-bottom: 20px;
    }

    /* Headings Typography */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 0.5rem;
    }
    h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 600;
        color: #444;
    }

    /* Custom Metric Styling */
    /* Styles for the real-time data display boxes */
    .metric-container {
        text-align: center;
        padding: 10px;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid var(--primary-color);
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #333;
    }
    .metric-unit {
        font-size: 1rem;
        color: #888;
        font-weight: normal;
    }

    /* Button Styling */
    /* Makes buttons span the full width and adds hover effects */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* Highlight Box */
    /* Used for the 'Goal' banners at the top of each tab */
    .highlight-box {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
        color: #0d47a1; /* Dark Blue Text for Contrast */
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
# Used to store experiment history so it persists between re-runs
if 'history_1st_law' not in st.session_state:
    st.session_state.history_1st_law = []
if 'history_2nd_law' not in st.session_state:
    st.session_state.history_2nd_law = []

# ==========================================
# SIDEBAR: Theory & Context
# ==========================================
with st.sidebar:
    st.title("Thermal Demo")
    st.markdown("---")
    
    st.subheader("📚 Concepts")
    
    # Expandable sections for physics theory
    with st.expander("First Law (Energy)", expanded=False):
        st.info(r"**$\Delta U = Q - W$**")
        st.markdown(r"""
        Energy is conserved. When you heat a gas:
        1. **$Q$ (Heat)** enters.
        2. Gas expands, doing **$W$ (Work)**.
        3. The rest warms the gas (**$\Delta U$**).
        """)
        
    with st.expander("Second Law (Entropy)", expanded=False):
        st.info(r"**$\Delta S_{total} > 0$**")
        st.markdown("""
        Heat flows spontaneously from **Hot** to **Cold**.
        *   This spreads energy out.
        *   **Entropy ($S$)** measures this spread (disorder).
        *   Total entropy always increases.
        """)
    
    st.markdown("---")
    st.markdown("### 🛠️ How to use")
    st.markdown("""
    1. **Select a Tab** for the law you want to study.
    2. **Adjust Controls** on the left panel.
    3. Click **Start Simulation**.
    4. Watch the **Visuals** & **Metrics**.
    """)
    st.caption("v2.0 | Interactive Demo")

# ==========================================
# MAIN HEADER
# ==========================================
st.title("Thermodynamics Simulator")
st.markdown("Interactive demonstration of the First and Second Laws of Thermodynamics.")

# Tabs for switching between simulations
tab1, tab2 = st.tabs(["🔥 First Law: Work & Energy", "🧊 Second Law: Heat & Entropy"])

# ==========================================
# HELPER: Drawing Piston (First Law)
# ==========================================
def draw_piston_clean(ax, piston_height, temp, heat_on, cyl_width=4, cyl_height=12, base_y=1):
    """
    Draws the piston cylinder, gas, and flame for the First Law simulation.
    Uses Matplotlib patches for high-quality vector graphics.
    """
    ax.clear()
    
    # Cylinder styling
    wall_color = '#333333'
    wall_width = 4
    
    # Draw Walls (Left, Right, Bottom)
    ax.plot([-cyl_width/2, -cyl_width/2], [base_y, base_y+cyl_height], color=wall_color, lw=wall_width) # Left
    ax.plot([cyl_width/2, cyl_width/2], [base_y, base_y+cyl_height], color=wall_color, lw=wall_width)   # Right
    ax.plot([-cyl_width/2, cyl_width/2], [base_y, base_y], color=wall_color, lw=wall_width)             # Bottom
    
    # Gas Color Calculation
    # Interpolates from Blue (300K) to Red (800K+) based on temperature
    t_norm = min(1.0, max(0.0, (temp - 300) / 500))
    gas_color = plt.cm.RdYlBu_r(t_norm) # Reverse Red-Yellow-Blue colormap
    
    # Draw Gas Volume
    gas_rect = patches.Rectangle(
        (-cyl_width/2 + 0.05, base_y + 0.05), cyl_width - 0.1, piston_height, 
        facecolor=gas_color, alpha=0.6, zorder=1
    )
    ax.add_patch(gas_rect)
    
    # Draw Piston Head
    piston_y = base_y + piston_height
    rect_piston = patches.FancyBboxPatch(
        (-cyl_width/2, piston_y), cyl_width, 0.8,
        boxstyle="round,pad=0.1",
        facecolor='#546E7A', edgecolor='#37474F', linewidth=2, zorder=2
    )
    ax.add_patch(rect_piston)
    
    # Draw Connecting Rod (Visual decoration)
    ax.plot([0, 0], [piston_y + 0.8, piston_y + 4], color='#90A4AE', lw=6, zorder=1)
    
    # Particle Simulation (Visual only)
    # Generates random points inside the gas volume to represent molecules
    np.random.seed(int(temp) + 10) # Seed varies with temp to show movement
    n_particles = 40
    # Restrict particles to gas volume
    px = np.random.uniform(-cyl_width/2 + 0.3, cyl_width/2 - 0.3, n_particles)
    py = np.random.uniform(base_y + 0.3, piston_y - 0.3, n_particles)
    
    # Particle size increases slightly with temperature
    size = 15 + (temp - 300)/20
    ax.scatter(px, py, c='white', edgecolors='black', s=size, alpha=0.6, zorder=3)
    
    # Heat Source Visualization (Vector Flame)
    if heat_on:
        # Draw a realistic flame using 3 layers of Polygons for depth
        flame_center_y = base_y - 2.5
        
        # 1. Outer Flame (Red-Orange Base) - Wavy asymmetric shape
        outer_verts = [
            (0.0, flame_center_y - 0.5),    # Bottom Center
            (-0.45, flame_center_y - 0.3),  # Bottom Left
            (-0.5, flame_center_y + 0.3),   # Mid Left Bulge
            (-0.2, flame_center_y + 0.7),   # Top Left Shoulder
            (0.0, flame_center_y + 1.1),    # Main Tip
            (0.2, flame_center_y + 0.6),    # Top Right Valley
            (0.4, flame_center_y + 0.8),    # Right Secondary Tip
            (0.5, flame_center_y + 0.2),    # Mid Right Bulge
            (0.4, flame_center_y - 0.3)     # Bottom Right
        ]
        flame_outer = patches.Polygon(outer_verts, closed=True, color='#FF5722', zorder=10)
        ax.add_patch(flame_outer)
        
        # 2. Middle Flame (Orange) - Slightly smaller
        mid_verts = [
            (0.0, flame_center_y - 0.4),
            (-0.3, flame_center_y - 0.2),
            (-0.35, flame_center_y + 0.2),
            (-0.1, flame_center_y + 0.5),
            (0.0, flame_center_y + 0.8),    # Mid Tip
            (0.15, flame_center_y + 0.4),
            (0.3, flame_center_y + 0.5),    # Right Mid Tip
            (0.35, flame_center_y + 0.1),
            (0.25, flame_center_y - 0.2)
        ]
        flame_mid = patches.Polygon(mid_verts, closed=True, color='#FF9800', zorder=11)
        ax.add_patch(flame_mid)
        
        # 3. Inner Core (Yellow/White Hot) - Smallest and brightest
        inner_verts = [
            (0.0, flame_center_y - 0.3),
            (-0.15, flame_center_y - 0.1),
            (-0.1, flame_center_y + 0.2),
            (0.0, flame_center_y + 0.5),    # Core Tip
            (0.1, flame_center_y + 0.2),
            (0.15, flame_center_y - 0.1)
        ]
        flame_inner = patches.Polygon(inner_verts, closed=True, color='#FFEB3B', zorder=12)
        ax.add_patch(flame_inner)
        
        # Label below flame
        ax.text(0, base_y - 1.4, "HEATING", fontsize=10, color='#D32F2F', ha='center', fontweight='bold')

    # Clean up Chart axes
    ax.set_xlim(-6, 6)
    ax.set_ylim(-2, 16)
    ax.axis('off')

# ==========================================
# HELPER: Drawing Thermal Blocks (Second Law)
# ==========================================
def draw_thermal_blocks(ax, temp_left, temp_right, material_name):
    """
    Draws the two thermal blocks touching each other.
    Visualizes temperature using color and labels.
    """
    ax.clear()
    
    # Dynamic Color Mapping
    # Maps temperature 0-200C to a color gradient
    norm = plt.Normalize(0, 200)
    cmap = plt.cm.RdYlBu_r
    
    color_left = cmap(norm(temp_left))
    color_right = cmap(norm(temp_right))
    
    # Draw Left Block (Initially Hot)
    rect_left = patches.Rectangle((0.1, 0.3), 0.4, 0.4, facecolor=color_left, edgecolor='#333', linewidth=2)
    ax.add_patch(rect_left)
    
    # Draw Right Block (Initially Cold) - Touching the left block
    rect_right = patches.Rectangle((0.5, 0.3), 0.4, 0.4, facecolor=color_right, edgecolor='#333', linewidth=2)
    ax.add_patch(rect_right)
    
    # Temperature Labels
    # Uses path_effects to add a black outline to the white text for readability
    ax.text(0.3, 0.5, f"{temp_left:.1f}°C", ha='center', va='center', color='white', fontweight='bold', fontsize=12, path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
    ax.text(0.7, 0.5, f"{temp_right:.1f}°C", ha='center', va='center', color='white', fontweight='bold', fontsize=12, path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
    
    # Material Label
    ax.text(0.5, 0.8, f"Material: {material_name}", ha='center', fontsize=10, color='#555')
    
    # Heat Flow Arrow (only if significant temp difference)
    if abs(temp_left - temp_right) > 0.5:
        direction = "➡️" if temp_left > temp_right else "⬅️"
        ax.text(0.5, 0.5, direction, ha='center', va='center', fontsize=20, zorder=10)

    # Set axes limits
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

# ==========================================
# TAB 1: FIRST LAW
# ==========================================
with tab1:
    st.markdown('<div class="highlight-box">💡 <b>Goal:</b> Convert Heat Energy into Mechanical Work. Observe how the piston moves as the gas expands.</div>', unsafe_allow_html=True)
    
    col_control, col_vis = st.columns([1, 2], gap="large")
    
    with col_control:
        st.markdown("### 🎛️ Controls")
        with st.container():
            st.label_visibility = "visible"
            
            st.markdown("**1. System Setup**")
            n_moles = st.number_input("Gas Amount (Moles)", 0.5, 5.0, 1.0, step=0.5, help="More gas = More volume")
            
            st.markdown("**2. Action**")
            heat_to_add = st.slider("Heat Input (Joules)", 100, 3000, 1000, step=100, help="Energy added to the system")
            
            st.markdown("<br>", unsafe_allow_html=True)
            run_btn_1 = st.button("🔥 Inject Heat & Run", type="primary")

    with col_vis:
        st.markdown("### 🔭 Visualization")
        
        # Placeholder for the Matplotlib plot
        plot_spot = st.empty()
        
        # Metrics Area
        st.markdown("#### Real-time Metrics")
        m1, m2, m3 = st.columns(3)
        metric_spot_q = m1.empty()
        metric_spot_w = m2.empty()
        metric_spot_u = m3.empty()
        
        # Default Initial State
        metric_spot_q.metric("Heat Added (Q)", "0 J")
        metric_spot_w.metric("Work Done (W)", "0 J")
        metric_spot_u.metric("Internal Energy (ΔU)", "0 J")
        
        if run_btn_1:
            # Physical Constants
            R = 8.314       # Gas constant
            Cv = 12.47      # Heat capacity at constant volume
            Cp = 20.78      # Heat capacity at constant pressure
            P_atm = 101325  # Atmospheric pressure
            T_start = 300   # Initial temperature (Kelvin)
            
            # Animation Configuration
            steps = 30
            heat_step = heat_to_add / steps
            V_start = (n_moles * R * T_start) / P_atm
            
            fig, ax = plt.subplots(figsize=(6, 4))
            
            # Animation Loop
            for i in range(steps + 1):
                current_heat = i * heat_step
                
                # Physics Calculations (Isobaric Expansion)
                # 1. Temperature change based on Heat Capacity (Cp)
                delta_T = current_heat / (n_moles * Cp)
                T_curr = T_start + delta_T
                
                # 2. Volume change based on Ideal Gas Law (PV=nRT)
                V_curr = (n_moles * R * T_curr) / P_atm
                
                # 3. Work Done (W = P * dV)
                work_done = P_atm * (V_curr - V_start)
                
                # 4. Internal Energy Change (dU = n * Cv * dT)
                delta_U = n_moles * Cv * delta_T
                
                # Scaling for visual representation
                scale = 4.0 / V_start
                h_curr = V_curr * scale
                
                # Draw Frame
                draw_piston_clean(ax, h_curr, T_curr, heat_on=(i < steps))
                plot_spot.pyplot(fig)
                
                # Update Metrics
                metric_spot_q.metric("Heat Added (Q)", f"{int(current_heat)} J")
                metric_spot_w.metric("Work Done (W)", f"{work_done:.1f} J")
                metric_spot_u.metric("Internal Energy (ΔU)", f"{delta_U:.1f} J")
                
                time.sleep(0.03) # Frame delay
            
            # Log Experiment to History
            st.session_state.history_1st_law.insert(0, {
                "Time": time.strftime("%H:%M:%S"),
                "Heat (J)": heat_to_add,
                "Work (J)": round(work_done, 1),
                "ΔU (J)": round(delta_U, 1),
                "Final Temp (K)": round(T_curr, 1)
            })
        else:
            # Static Initial View (Before run)
            fig, ax = plt.subplots(figsize=(6, 4))
            draw_piston_clean(ax, 4.0, 300, False)
            plot_spot.pyplot(fig)

    # History Table
    if st.session_state.history_1st_law:
        st.markdown("### 📋 Experiment Log")
        st.dataframe(
            pd.DataFrame(st.session_state.history_1st_law),
            use_container_width=True,
            hide_index=True
        )

# ==========================================
# TAB 2: SECOND LAW
# ==========================================
with tab2:
    st.markdown('<div class="highlight-box">💡 <b>Goal:</b> Observe spontaneous heat flow. Heat moves from Hot → Cold until Equilibrium is reached.</div>', unsafe_allow_html=True)

    col_control_2, col_vis_2 = st.columns([1, 2], gap="large")
    
    with col_control_2:
        st.markdown("### 🎛️ Setup")
        with st.container():
            material_name = st.selectbox("Block Material", list(MATERIALS.keys()), help="Different materials conduct heat at different rates")
            
            st.markdown("---")
            st.markdown("**Initial Temperatures**")
            t_hot_init = st.slider("🔴 Hot Block (°C)", 50, 200, 100)
            t_cold_init = st.slider("🔵 Cold Block (°C)", 0, 40, 20)
            
            st.markdown("---")
            mass_block = st.number_input("Mass (kg)", 0.1, 5.0, 1.0)
            
            st.markdown("<br>", unsafe_allow_html=True)
            run_btn_2 = st.button("▶️ Start Simulation", type="primary")

    with col_vis_2:
        st.markdown("### 📈 Real-time Data")
        
        # Containers for Visuals to maintain layout stability
        block_vis_container = st.empty()
        chart_container = st.empty()
        status_container = st.empty()
        
        if run_btn_2:
            # Physics Setup
            props = MATERIALS[material_name]
            Th = t_hot_init + 273.15 # Convert to Kelvin
            Tc = t_cold_init + 273.15
            S_total = 0
            
            hist_time, hist_Th, hist_Tc, hist_S = [], [], [], []
            
            # Simulation Loop Config
            max_steps = 5000
            step_count = 0
            equilibrium_tolerance = 0.05
            initial_temperature_gap = Th - Tc
            
            progress_bar = st.progress(0)
            
            # Setup Plot for Blocks
            fig_blocks, ax_blocks = plt.subplots(figsize=(6, 2.5))
            
            # Run until thermal equilibrium or the defensive iteration limit.
            while (Th - Tc) > equilibrium_tolerance and step_count < max_steps:
                step_count += 1

                step = thermal_exchange_step(
                    Th,
                    Tc,
                    mass_kg=mass_block,
                    specific_heat_j_per_kg_k=props["specific_heat"],
                    conductivity=props["conductivity"],
                    speed_factor=simulation_speed_factor(props["conductivity"]),
                )
                Th = step.hot_temperature_k
                Tc = step.cold_temperature_k
                S_total += step.entropy_change_j_per_k
                
                # Data Recording
                hist_time.append(step_count)
                hist_Th.append(Th - 273.15) # Convert back to Celsius for plot
                hist_Tc.append(Tc - 273.15)
                hist_S.append(S_total)
                
                # Adaptive Rendering
                # Rendering every frame is slow. We skip frames as the simulation stabilizes.
                should_render = (
                    step_count < 20
                    or step_count % 25 == 0
                    or (Th - Tc) < 0.1
                )
                
                if should_render:
                    # 1. Update Block Visualization (Matplotlib)
                    draw_thermal_blocks(ax_blocks, Th - 273.15, Tc - 273.15, material_name)
                    block_vis_container.pyplot(fig_blocks)
                    
                    # 2. Update Charts (Plotly)
                    df = pd.DataFrame({
                        "Time": hist_time,
                        "Hot": hist_Th,
                        "Cold": hist_Tc,
                        "Entropy": hist_S
                    })
                    
                    fig = go.Figure()
                    # Temperature Traces
                    fig.add_trace(go.Scatter(x=df.Time, y=df.Hot, name="Hot Block", line=dict(color='#FF5252', width=3)))
                    fig.add_trace(go.Scatter(x=df.Time, y=df.Cold, name="Cold Block", line=dict(color='#448AFF', width=3)))
                    
                    # Entropy Trace (Secondary Y Axis)
                    fig.add_trace(go.Scatter(x=df.Time, y=df.Entropy, name="Entropy (J/K)", 
                                           line=dict(color='#66BB6A', dash='dot', width=2), yaxis="y2"))
                    
                    # Chart Layout Configuration
                    fig.update_layout(
                        title="Temperature Convergence",
                        margin=dict(l=10, r=10, t=60, b=10), # Adjusted margins
                        height=350,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(title="Simulation Steps", showgrid=False),
                        yaxis=dict(title="Temperature (°C)", showgrid=True, gridcolor='#eee'),
                        yaxis2=dict(title="Entropy (J/K)", overlaying="y", side="right", showgrid=False),
                        legend=dict(orientation="h", y=1.1)
                    )
                    chart_container.plotly_chart(fig, use_container_width=True)
                    
                    # Variable sleep to keep animation smooth but not too slow
                    time.sleep(0.01)
                
                # Update progress bar based on how much the temperature gap has closed
                remaining_gap = max(0.0, Th - Tc)
                prog = 1.0 - (remaining_gap / initial_temperature_gap)
                progress_bar.progress(min(1.0, max(0.0, prog)))
            
            # Report the actual terminal state instead of forcing a success.
            remaining_gap = max(0.0, Th - Tc)
            progress_bar.progress(
                min(1.0, max(0.0, 1.0 - remaining_gap / initial_temperature_gap))
            )
            progress_bar.empty()

            if remaining_gap <= equilibrium_tolerance:
                status_container.success(
                    f"✅ Equilibrium reached at {Th - 273.15:.1f} °C. "
                    f"Total Entropy increased by {S_total:.4f} J/K"
                )
            else:
                status_container.warning(
                    "Simulation stopped at its safety limit with a "
                    f"{remaining_gap:.2f} °C temperature gap remaining."
                )
            
            # Log Experiment
            st.session_state.history_2nd_law.insert(0, {
                "Material": material_name,
                "Mass": mass_block,
                "Init ΔT": t_hot_init - t_cold_init,
                "Final Entropy (J/K)": round(S_total, 4)
            })
            
        else:
            # Placeholder State when not running
            st.info("Click 'Start Simulation' to begin.")
            
            # Show static initial blocks
            fig_static, ax_static = plt.subplots(figsize=(6, 2.5))
            draw_thermal_blocks(ax_static, 100, 20, "Iron") # Default values
            block_vis_container.pyplot(fig_static)
