import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(
    page_title="Structural Safety Analyzer",
    page_icon="🏗️",
    layout="wide"
)

# ----------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #f4f6f8;
}
.metric-box {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
}
h1 {
    color: #003366;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# MATERIAL DATABASE
# ----------------------------------------------------
materials = {
    "Steel": {"E": 200e9, "yield": 250e6},
    "Cast Iron": {"E": 110e9, "yield": 130e6},
    "Aluminum": {"E": 69e9, "yield": 95e6},
    "Titanium": {"E": 116e9, "yield": 830e6},
    "Copper": {"E": 117e9, "yield": 70e6},
    "Brass": {"E": 100e9, "yield": 200e6},
    "Concrete": {"E": 30e9, "yield": 40e6},
    "Wood": {"E": 12e9, "yield": 40e6}
}

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.title("🏗️ Structural Safety Analyzer")
st.markdown("### Live Beam Deflection & Material Comparison Dashboard")

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------
st.sidebar.header("Beam Parameters")

material = st.sidebar.selectbox(
    "Select Material",
    list(materials.keys())
)

length = st.sidebar.slider(
    "Beam Length (m)",
    1.0,
    10.0,
    5.0
)

load = st.sidebar.slider(
    "Applied Load (N)",
    100,
    10000,
    3000
)

width = st.sidebar.slider(
    "Beam Width (mm)",
    50,
    300,
    100
)

height = st.sidebar.slider(
    "Beam Height (mm)",
    50,
    500,
    200
)

# ----------------------------------------------------
# CALCULATIONS
# ----------------------------------------------------
E = materials[material]["E"]
yield_strength = materials[material]["yield"]

b = width / 1000
h = height / 1000

I = (b * h**3) / 12

deflection = (load * length**3) / (48 * E * I)

stress = (load * length * h/2) / (4 * I)

fos = yield_strength / stress

# ----------------------------------------------------
# METRICS
# ----------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Deflection",
    f"{deflection*1000:.2f} mm"
)

col2.metric(
    "Stress",
    f"{stress/1e6:.2f} MPa"
)

col3.metric(
    "Yield Strength",
    f"{yield_strength/1e6:.0f} MPa"
)

col4.metric(
    "Factor of Safety",
    f"{fos:.2f}"
)

# ----------------------------------------------------
# SAFETY STATUS
# ----------------------------------------------------
st.subheader("Safety Assessment")

if fos > 2:
    st.success("✅ SAFE DESIGN")
elif fos > 1:
    st.warning("⚠️ MARGINALLY SAFE")
else:
    st.error("❌ UNSAFE DESIGN")

# ----------------------------------------------------
# BEAM DEFLECTION GRAPH
# ----------------------------------------------------
x = np.linspace(0, length, 100)

y = -deflection * np.sin(np.pi * x / length)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=x,
        y=y*1000,
        mode="lines",
        name="Deflection"
    )
)

fig.update_layout(
    title="Live Beam Deflection Profile",
    xaxis_title="Beam Length (m)",
    yaxis_title="Deflection (mm)",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# MATERIAL COMPARISON
# ----------------------------------------------------
st.subheader("Material Comparison")

comparison = []

for mat, props in materials.items():

    E_mat = props["E"]

    d = (load * length**3) / (
        48 * E_mat * I
    )

    comparison.append([
        mat,
        round(d*1000, 3)
    ])

df = pd.DataFrame(
    comparison,
    columns=["Material", "Deflection (mm)"]
)

st.dataframe(df, use_container_width=True)

fig2 = go.Figure()

fig2.add_trace(
    go.Bar(
        x=df["Material"],
        y=df["Deflection (mm)"]
    )
)

fig2.update_layout(
    title="Material vs Deflection",
    xaxis_title="Material",
    yaxis_title="Deflection (mm)",
    height=500
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------------------------
# REPORT
# ----------------------------------------------------
st.subheader("Engineering Summary")

st.write(f"""
**Selected Material:** {material}

**Beam Length:** {length:.2f} m

**Applied Load:** {load} N

**Maximum Deflection:** {deflection*1000:.2f} mm

**Maximum Stress:** {stress/1e6:.2f} MPa

**Factor of Safety:** {fos:.2f}
""")

st.info(
    "This application is developed for ICT in Structural Safety. "
    "It visualizes beam behavior under different loading conditions "
    "and compares structural materials used in engineering design."
)
