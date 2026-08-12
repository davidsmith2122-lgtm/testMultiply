"""
app.py

UI layer only — everything it needs comes from model.py.
This mirrors the structure of "the Excel model":
  1. System Inputs
  2. General Modelling Parameters
  3. Influent Characterisation
  4. Growth
  5. Active Year / Output
  6. Forecasted Outputs

STRUCTURAL MOCKUP ONLY — calculations are placeholders (see model.py).
The point of this version is to see the FLOW and LAYOUT, not real numbers.
"""

import streamlit as st
import pandas as pd
from model import (
    DEFAULT_UNITS,
    DEFAULT_PARAMS,
    run_process_flow,
    check_pass_fail,
    interpolate_adwf,
)

st.set_page_config(page_title="WWTP Model — Structural Mockup test", layout="wide")
st.title("Wastewater Treatment Model — Structural Mockup")
st.caption("Placeholder calculations only. Purpose of this version: confirm the "
           "flow between systems and the overall UI layout before real equations go in.")

# ---------------------------------------------------------
# Session state — this is what makes edits "stick" across reruns.
# Without this, every rerun would reset back to the defaults.
# ---------------------------------------------------------
if "units" not in st.session_state:
    st.session_state.units = {k: dict(v) for k, v in DEFAULT_UNITS.items()}

if "growth_df" not in st.session_state:
    st.session_state.growth_df = pd.DataFrame({
        "year": [2026, 2027, 2028, 2029, 2030],
        "adwf": [100, 110, 120, 135, 150],  # placeholder units
    })

if "influent_df" not in st.session_state:
    st.session_state.influent_df = pd.DataFrame({
        "parameter": ["BOD", "TSS", "Ammonia"],
        "Source 1": [250, 300, 30],
        "Source 2": [180, 220, 25],
    })

tabs = st.tabs([
    "System Inputs",
    "General Parameters",
    "Influent Characterisation",
    "Growth",
    "Active Year / Output",
    "Forecast",
])

# ---------------------------------------------------------
# TAB 1: System Inputs — build the process flow structure
# ---------------------------------------------------------
with tabs[0]:
    st.header("System Inputs")
    st.caption(
        "Each unit declares where its input comes from: 'Influent', or one "
        "or more other units. Listing more than one source models a "
        "convergence point (e.g. two secondary trains feeding one tertiary)."
    )

    st.subheader("Current process units")
    for name, config in st.session_state.units.items():
        cols = st.columns([3, 2, 4, 1])
        cols[0].write(f"**{name}**")
        cols[1].write(config["type"])
        cols[2].write("Input from: " + ", ".join(config["inputs"]))
        if cols[3].button("Remove", key=f"remove_{name}"):
            del st.session_state.units[name]
            st.rerun()

    st.divider()
    st.subheader("Add a new unit")

    available_sources = ["Influent"] + list(st.session_state.units.keys())

    new_name = st.text_input("Unit name (e.g. 'Tertiary 2')")
    new_type = st.selectbox("Unit type", ["Primary", "Secondary", "Tertiary"])
    new_inputs = st.multiselect(
        "Input source(s) — select more than one to model a convergence point",
        available_sources,
    )

    if st.button("Add unit"):
        if new_name and new_inputs:
            st.session_state.units[new_name] = {"type": new_type, "inputs": new_inputs}
            st.success(f"Added '{new_name}'")
            st.rerun()
        else:
            st.warning("Give the unit a name and pick at least one input source.")

# ---------------------------------------------------------
# TAB 2: General Parameters
# ---------------------------------------------------------
with tabs[1]:
    st.header("General Modelling Parameters")
    st.caption("Placeholder — the 'most people shouldn't need to touch these' values.")

    for unit_type, params in DEFAULT_PARAMS.items():
        st.subheader(unit_type)
        for key, value in params.items():
            st.number_input(f"{unit_type} — {key}", value=value, key=f"param_{unit_type}_{key}")

# ---------------------------------------------------------
# TAB 3: Influent Characterisation
# ---------------------------------------------------------
with tabs[2]:
    st.header("Influent Characterisation")
    st.caption("One column per source. Edit directly, like Excel.")
    st.session_state.influent_df = st.data_editor(
        st.session_state.influent_df, num_rows="dynamic", key="influent_editor"
    )

# ---------------------------------------------------------
# TAB 4: Growth
# ---------------------------------------------------------
with tabs[3]:
    st.header("Growth (Average Dry Weather Flow forecast)")
    st.session_state.growth_df = st.data_editor(
        st.session_state.growth_df, num_rows="dynamic", key="growth_editor"
    )
    st.line_chart(st.session_state.growth_df.set_index("year"))

# ---------------------------------------------------------
# TAB 5: Active Year / Output
# ---------------------------------------------------------
with tabs[4]:
    st.header("Active Year & Current Results")

    active_year = st.selectbox("Active year", st.session_state.growth_df["year"])
    adwf = interpolate_adwf(st.session_state.growth_df, active_year)
    st.write(f"ADWF for {active_year}: **{adwf}**")

    external_sources = {"Influent": adwf}
    results = run_process_flow(st.session_state.units, DEFAULT_PARAMS, external_sources)

    st.subheader("Results by unit")
    results_df = pd.DataFrame(results.items(), columns=["Unit", "Flow (placeholder)"])
    st.dataframe(results_df, use_container_width=True)

    status = check_pass_fail(results, limit=100)  # placeholder limit
    if status == "PASS":
        st.success(f"Status: {status}")
    else:
        st.error(f"Status: {status}")

# ---------------------------------------------------------
# TAB 6: Forecast — same model, run once per year in Growth
# ---------------------------------------------------------
with tabs[5]:
    st.header("Forecasted Outputs")
    st.caption("Runs the exact same model across every year in the Growth table.")

    forecast_rows = []
    for _, row in st.session_state.growth_df.iterrows():
        year = row["year"]
        results_year = run_process_flow(
            st.session_state.units, DEFAULT_PARAMS, {"Influent": row["adwf"]}
        )
        status_year = check_pass_fail(results_year, limit=100)
        forecast_rows.append({"year": year, **results_year, "status": status_year})

    forecast_df = pd.DataFrame(forecast_rows)
    st.dataframe(forecast_df, use_container_width=True)
