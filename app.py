"""
app.py

This file is ONLY the UI layer. It imports calculation functions from
model.py rather than doing math itself. If you ever swap Streamlit for
something else, model.py doesn't need to change at all.
"""

import streamlit as st
from model import calculate_stream, calculate_system

st.title("Process Mockup: Tabs + Columns + Model Separation")

# ---------------------------------------------------------
# EXAMPLE 1: st.tabs -> like Excel tabs (separate pages)
# ---------------------------------------------------------
st.header("Example 1: Tabs (separate systems)")

system_names = ["System A", "System B", "System C"]
tabs = st.tabs(system_names)

for tab, name in zip(tabs, system_names):
    with tab:
        st.subheader(name)
        x = st.number_input(f"{name} - input value", key=f"{name}_x")
        factor = st.number_input(f"{name} - factor", value=1.0, key=f"{name}_factor")

        result = calculate_system(x, factor)
        st.write(f"Result: {result}")


# ---------------------------------------------------------
# EXAMPLE 2: st.columns -> like Excel columns (side by side)
# ---------------------------------------------------------
st.header("Example 2: Columns (parallel streams, side by side)")

stream_names = ["Stream 1", "Stream 2", "Stream 3"]
cols = st.columns(len(stream_names))

for col, name in zip(cols, stream_names):
    with col:
        st.subheader(name)
        x = st.number_input(f"{name} - x", key=f"{name}_x")
        y = st.number_input(f"{name} - y", key=f"{name}_y")

        result = calculate_stream(x, y)
        st.write(f"Result: {result}")


# ---------------------------------------------------------
# EXAMPLE 3: simple "source toggle" mockup
# one system's input can come from another system's output
# ---------------------------------------------------------
st.header("Example 3: Simple source toggle (System B fed by System A)")

st.subheader("System A")
a_input = st.number_input("System A - manual input", key="a_input")
a_factor = st.number_input("System A - factor", value=1.0, key="a_factor")
a_result = calculate_system(a_input, a_factor)
st.write(f"System A result: {a_result}")

st.subheader("System B")
b_source = st.selectbox("System B input source", ["Manual entry", "System A output"])

if b_source == "Manual entry":
    b_input = st.number_input("System B - manual input", key="b_input")
else:
    b_input = a_result
    st.write(f"Using System A's result as input: {b_input}")

b_factor = st.number_input("System B - factor", value=1.0, key="b_factor")
b_result = calculate_system(b_input, b_factor)
st.write(f"System B result: {b_result}")
