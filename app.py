import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# PAGE / TABS
# =========================================================

st.title("Simple Process Model")

inputs_tab, constants_tab, results_tab, spa_tab = st.tabs([
    "Inputs",
    "Constants",
    "Results",
    "State Point Analysis"
])


# =========================================================
# INPUTS TAB
# =========================================================

with inputs_tab:

    # -----------------------------------------------------
    # INFLUENT SOURCES
    # -----------------------------------------------------

    st.header("Influent Sources")

    default_source_data = pd.DataFrame({
        "Name": ["Influent Source 1", "Influent Source 2", "Influent Source 3", "Influent Source 4"],
        "Active": [True, True, False, False],
        "Flow": [10.0, 10.0, 0.0, 0.0],
        "TSS": [200.0, 100.0, 0.0, 0.0],
        "ISS": [40.0, 30.0, 0.0, 0.0],
        "TN": [40.0, 30.0, 0.0, 0.0],
        "TP": [7.0, 5.0, 0.0, 0.0],
        "Soluble biodegradable COD": [100.0, 80.0, 0.0, 0.0],
        "Particulate biodegradable COD": [200.0, 120.0, 0.0, 0.0],
        "Soluble non-biodegradable COD": [50.0, 40.0, 0.0, 0.0],
        "Particulate non-biodegradable COD": [100.0, 60.0, 0.0, 0.0],
        "NH4": [25.0, 20.0, 0.0, 0.0],
        "NO3": [2.0, 3.0, 0.0, 0.0],
        "PO4": [4.0, 2.0, 0.0, 0.0]
    })

    source_data = st.data_editor(
        default_source_data,
        hide_index=True,
        num_rows="dynamic",
        width="stretch",
        key="source_editor"
    )

    # -----------------------------------------------------
    # PRIMARY SYSTEMS
    # -----------------------------------------------------

    st.header("Primary Systems")

    default_primary_data = pd.DataFrame({
        "Name": ["Primary 1", "Primary 2", "Primary 3", "Primary 4"],
        "Active": [True, False, False, False],
        "Type": ["Primary"] * 4,
        "Modelling Order Group": [1] * 4,
        "Modelling Order Specific": [1, 2, 3, 4],
        "Length": [30.0] * 4,
        "Width": [10.0] * 4
    })

    primary_data = st.data_editor(
        default_primary_data,
        hide_index=True,
        num_rows="dynamic",
        width="stretch",
        column_config={
            "Type": None,
            "Modelling Order Group": None,
            "Modelling Order Specific": None
        },
        key="primary_editor"
    )

    primary_data["Type"] = "Primary"
    primary_data["Modelling Order Group"] = 1
    primary_data["Modelling Order Specific"] = range(1, len(primary_data) + 1)

    # -----------------------------------------------------
    # SECONDARY SYSTEMS
    # -----------------------------------------------------

    st.header("Secondary Systems")

    default_secondary_data = pd.DataFrame({
        "Name": ["Secondary 1", "Secondary 2", "Secondary 3", "Secondary 4"],
        "Active": [True, False, False, False],
        "Type": ["Secondary"] * 4,
        "Modelling Order Group": [2] * 4,
        "Modelling Order Specific": [1, 2, 3, 4],
        "Secondary Type": ["Conventional"] * 4,
        "Volume": [5000.0] * 4,
        "SRT": [15.0] * 4
    })

    secondary_data = st.data_editor(
        default_secondary_data,
        hide_index=True,
        num_rows="dynamic",
        width="stretch",
        column_config={
            "Type": None,
            "Modelling Order Group": None,
            "Modelling Order Specific": None,
            "Secondary Type": st.column_config.SelectboxColumn(options=["Conventional", "MBR"])
        },
        key="secondary_editor"
    )

    secondary_data["Type"] = "Secondary"
    secondary_data["Modelling Order Group"] = 2
    secondary_data["Modelling Order Specific"] = range(1, len(secondary_data) + 1)

    # -----------------------------------------------------
    # TERTIARY SYSTEMS
    # -----------------------------------------------------

    st.header("Tertiary Systems")

    default_tertiary_data = pd.DataFrame({
        "Name": ["Tertiary 1", "Tertiary 2", "Tertiary 3", "Tertiary 4"],
        "Active": [False, False, False, False],
        "Type": ["Tertiary"] * 4,
        "Modelling Order Group": [3] * 4,
        "Modelling Order Specific": [1, 2, 3, 4],
        "Filter Area": [100.0] * 4
    })

    tertiary_data = st.data_editor(
        default_tertiary_data,
        hide_index=True,
        num_rows="dynamic",
        width="stretch",
        column_config={
            "Type": None,
            "Modelling Order Group": None,
            "Modelling Order Specific": None
        },
        key="tertiary_editor"
    )

    tertiary_data["Type"] = "Tertiary"
    tertiary_data["Modelling Order Group"] = 3
    tertiary_data["Modelling Order Specific"] = range(1, len(tertiary_data) + 1)

    # -----------------------------------------------------
    # PATHWAYS
    # -----------------------------------------------------

    st.header("Pathways")

    default_pathways = pd.DataFrame({
        "Source": ["Influent Source 1", "Influent Source 2", "Primary 1"],
        "Destination": ["Primary 1", "Primary 1", "Secondary 1"],
        "Proportion": [1.0, 1.0, 1.0]
    })

    pathways = st.data_editor(
        default_pathways,
        hide_index=True,
        num_rows="dynamic",
        width="stretch",
        key="pathway_editor"
    )


# =========================================================
# CONSTANTS TAB
# =========================================================

with constants_tab:

    # -----------------------------------------------------
    # PERFORMANCE BENCHMARKS
    # -----------------------------------------------------

    st.header("Performance Benchmarks")

    default_performance_benchmarks = {
        "Primary": {
            "SOR (m/hr)": 1.0
        },
        "Secondary": {
            "Max MLSS - Conventional (mg/L)": 4500.0,
            "Max MLSS - MBR (mg/L)": 12000.0
        },
        "Tertiary": {
            "Filtration Rate (m/hr)": 10.0
        }
    }

    benchmark_rows = []

    for system_type, benchmarks in default_performance_benchmarks.items():
        for criterion, value in benchmarks.items():
            benchmark_rows.append({
                "System Type": system_type,
                "Criterion": criterion,
                "Benchmark": value
            })

    benchmark_data = pd.DataFrame(benchmark_rows)

    benchmark_data = st.data_editor(
        benchmark_data,
        hide_index=True,
        width="stretch",
        column_config={
            "System Type": st.column_config.TextColumn(disabled=True),
            "Criterion": st.column_config.TextColumn(disabled=True),
            "Benchmark": st.column_config.NumberColumn(min_value=0.0)
        },
        key="benchmark_editor"
    )

    performance_benchmarks = {}

    for index, row in benchmark_data.iterrows():
        system_type = row["System Type"]
        if system_type not in performance_benchmarks:
            performance_benchmarks[system_type] = {}
        performance_benchmarks[system_type][row["Criterion"]] = row["Benchmark"]

    # -----------------------------------------------------
    # MODELLING CONSTANTS
    # -----------------------------------------------------

    st.header("Modelling Constants")

    default_modelling_constants = {
        "Yh": 0.45,
        "bH": 0.24,
        "fh": 0.20,
        "fcv": 1.48,
        "f_inert_biomass": 0.15
    }

    constants_data = pd.DataFrame({
        "Constant": list(default_modelling_constants.keys()),
        "Value": list(default_modelling_constants.values())
    })

    constants_data = st.data_editor(
        constants_data,
        hide_index=True,
        width="stretch",
        column_config={
            "Constant": st.column_config.TextColumn(disabled=True),
            "Value": st.column_config.NumberColumn(min_value=0.0)
        },
        key="constants_editor"
    )

    modelling_constants = {}

    for index, row in constants_data.iterrows():
        modelling_constants[row["Constant"]] = row["Value"]


# =========================================================
# BACKEND MODEL SETUP
# =========================================================

# Derived COD values

source_data["Biodegradable COD"] = (
    source_data["Soluble biodegradable COD"]
    + source_data["Particulate biodegradable COD"]
)

source_data["Non-biodegradable COD"] = (
    source_data["Soluble non-biodegradable COD"]
    + source_data["Particulate non-biodegradable COD"]
)

source_data["Total COD"] = (
    source_data["Biodegradable COD"]
    + source_data["Non-biodegradable COD"]
)


# Analytes

cod_fraction_analytes = [
    "Soluble biodegradable COD",
    "Particulate biodegradable COD",
    "Soluble non-biodegradable COD",
    "Particulate non-biodegradable COD"
]

derived_cod_analytes = [
    "Biodegradable COD",
    "Non-biodegradable COD",
    "Total COD"
]

other_analytes = [
    "TSS",
    "ISS",
    "TN",
    "TP",
    "NH4",
    "NO3",
    "PO4"
]

analytes = other_analytes + cod_fraction_analytes + derived_cod_analytes


# Combine systems and determine modelling order

systems = pd.concat(
    [primary_data, secondary_data, tertiary_data],
    ignore_index=True
)

systems = systems[systems["Active"] == True].copy()

ordered_systems = systems.sort_values(
    by=["Modelling Order Group", "Modelling Order Specific"]
)


# =========================================================
# NODES
# =========================================================

node_columns = ["Type", "Active", "Flow"] + analytes
nodes = pd.DataFrame(columns=node_columns)

for index, row in source_data.iterrows():

    if row["Active"] == True:

        source_name = row["Name"]

        nodes.loc[source_name] = {
            "Type": "Influent Source",
            "Active": True,
            "Flow": row["Flow"],
            "TSS": row["TSS"],
            "ISS": row["ISS"],
            "TN": row["TN"],
            "TP": row["TP"],
            "NH4": row["NH4"],
            "NO3": row["NO3"],
            "PO4": row["PO4"],
            "Soluble biodegradable COD": row["Soluble biodegradable COD"],
            "Particulate biodegradable COD": row["Particulate biodegradable COD"],
            "Soluble non-biodegradable COD": row["Soluble non-biodegradable COD"],
            "Particulate non-biodegradable COD": row["Particulate non-biodegradable COD"],
            "Biodegradable COD": row["Biodegradable COD"],
            "Non-biodegradable COD": row["Non-biodegradable COD"],
            "Total COD": row["Total COD"]
        }

for index, row in ordered_systems.iterrows():

    nodes.loc[row["Name"]] = {
        "Type": row["Type"],
        "Active": True,
        "Flow": 0.0,
        **{analyte: 0.0 for analyte in analytes}
    }


# =========================================================
# PERFORMANCE RESULT DATAFRAMES
# =========================================================

df_primary_performance_results = pd.DataFrame()
df_secondary_performance_results = pd.DataFrame()
df_tertiary_performance_results = pd.DataFrame()


# =========================================================
# FUNCTIONS
# =========================================================

def classifyPerformance(actual_value, benchmark, lower_is_better=True):

    if lower_is_better:
        if actual_value > benchmark:
            return "FAIL"
        elif actual_value >= 0.9 * benchmark:
            return "CRITICAL"
        else:
            return "PASS"

    else:
        if actual_value < benchmark:
            return "FAIL"
        elif actual_value <= 1.1 * benchmark:
            return "CRITICAL"
        else:
            return "PASS"


def calcCombinedStreamToSystem(system_name, pathways, nodes, analytes):

    incoming_pathways = pathways[pathways["Destination"] == system_name].copy()

    incoming_streams = incoming_pathways.merge(
        nodes,
        left_on="Source",
        right_index=True,
        how="left"
    )

    incoming_streams = incoming_streams.dropna(subset=["Flow"])

    incoming_streams["Adjusted Flow"] = (
        incoming_streams["Flow"]
        * incoming_streams["Proportion"]
    )

    total_flow = incoming_streams["Adjusted Flow"].sum()

    if total_flow > 0:

        weighted_concentrations = (
            incoming_streams[analytes]
            .multiply(incoming_streams["Adjusted Flow"], axis=0)
            .sum()
            / total_flow
        )

    else:
        weighted_concentrations = pd.Series(0.0, index=analytes)

    combined_input_stream = weighted_concentrations.to_frame().T
    combined_input_stream.insert(0, "Flow", total_flow)

    return combined_input_stream


# =========================================================
# PRIMARY MODEL
# =========================================================

def modelPrimary(system_data, combined_input_stream, performance_benchmarks, modelling_constants):

    length = system_data["Length"]
    width = system_data["Width"]
    area = length * width
    flow = combined_input_stream.loc[0, "Flow"]

    sor = flow * 1000 / 24 / area if area > 0 else 0.0
    benchmark_sor = performance_benchmarks["Primary"]["SOR (m/hr)"]
    status = classifyPerformance(sor, benchmark_sor, lower_is_better=True)

    output_stream = combined_input_stream.copy()

    # Placeholder primary removal
    output_stream.loc[0, "TSS"] *= 0.8

    for cod_fraction in cod_fraction_analytes:
        output_stream.loc[0, cod_fraction] *= 0.8

    output_stream.loc[0, "Biodegradable COD"] = (
        output_stream.loc[0, "Soluble biodegradable COD"]
        + output_stream.loc[0, "Particulate biodegradable COD"]
    )

    output_stream.loc[0, "Non-biodegradable COD"] = (
        output_stream.loc[0, "Soluble non-biodegradable COD"]
        + output_stream.loc[0, "Particulate non-biodegradable COD"]
    )

    output_stream.loc[0, "Total COD"] = (
        output_stream.loc[0, "Biodegradable COD"]
        + output_stream.loc[0, "Non-biodegradable COD"]
    )

    performance_results = {
        "Area (m²)": area,
        "SOR (m/hr)": sor,
        "Benchmark SOR (m/hr)": benchmark_sor,
        "Status": status
    }

    return output_stream, performance_results


# =========================================================
# SECONDARY MODEL
# =========================================================

def modelSecondary(system_data, combined_input_stream, performance_benchmarks, modelling_constants):

    output_stream = combined_input_stream.copy()

    flow = combined_input_stream.loc[0, "Flow"]

    biodegradable_cod = (
        combined_input_stream.loc[0, "Soluble biodegradable COD"]
        + combined_input_stream.loc[0, "Particulate biodegradable COD"]
    )

    particulate_non_biodegradable_cod = (
        combined_input_stream.loc[0, "Particulate non-biodegradable COD"]
    )

    influent_iss = combined_input_stream.loc[0, "ISS"]

    volume = system_data["Volume"]
    srt = system_data["SRT"]
    secondary_type = system_data["Secondary Type"]

    Yh = modelling_constants["Yh"]
    bH = modelling_constants["bH"]
    fh = modelling_constants["fh"]
    fcv = modelling_constants["fcv"]
    f_inert_biomass = modelling_constants["f_inert_biomass"]

    mx_bh = (
        flow * biodegradable_cod * Yh * srt / (1 + bH * srt)
        if (1 + bH * srt) != 0
        else 0.0
    )

    mx_eh = mx_bh * fh * bH * srt

    mx_ii = (
        particulate_non_biodegradable_cod * flow / fcv * srt
        if fcv > 0
        else 0.0
    )

    mx_iss = influent_iss * flow * srt + f_inert_biomass * mx_bh

    total_tss_mass = mx_bh + mx_eh + mx_ii + mx_iss

    estimated_mlss = (
        total_tss_mass / volume * 1000
        if volume > 0
        else 0.0
    )

    if secondary_type == "MBR":
        benchmark_mlss = performance_benchmarks["Secondary"]["Max MLSS - MBR (mg/L)"]
    else:
        benchmark_mlss = performance_benchmarks["Secondary"]["Max MLSS - Conventional (mg/L)"]

    status = classifyPerformance(
        estimated_mlss,
        benchmark_mlss,
        lower_is_better=True
    )

    performance_results = {
        "Secondary Type": secondary_type,
        "Inlet Flow (ML/d)": flow,
        "Inlet Biodegradable COD (mg/L)": biodegradable_cod,
        "SRT (days)": srt,
        "Volume (m³)": volume,
        "Active Biomass MX_BH (kg)": mx_bh,
        "Endogenous Biomass MX_EH (kg)": mx_eh,
        "Inert Particulate Organics MX_II (kg)": mx_ii,
        "ISS Inventory MX_ISS (kg)": mx_iss,
        "Total TSS Inventory (kg)": total_tss_mass,
        "Estimated MLSS (mg/L)": estimated_mlss,
        "Benchmark MLSS (mg/L)": benchmark_mlss,
        "Status": status
    }

    return output_stream, performance_results


# =========================================================
# TERTIARY MODEL
# =========================================================

def modelTertiary(system_data, combined_input_stream, performance_benchmarks, modelling_constants):

    output_stream = combined_input_stream.copy()

    flow = combined_input_stream.loc[0, "Flow"]
    filter_area = system_data["Filter Area"]

    filtration_rate = (
        flow * 1000 / 24 / filter_area
        if filter_area > 0
        else 0.0
    )

    benchmark_rate = performance_benchmarks["Tertiary"]["Filtration Rate (m/hr)"]

    status = classifyPerformance(
        filtration_rate,
        benchmark_rate,
        lower_is_better=True
    )

    performance_results = {
        "Filtration Rate (m/hr)": filtration_rate,
        "Benchmark Filtration Rate (m/hr)": benchmark_rate,
        "Status": status
    }

    return output_stream, performance_results


# =========================================================
# MODEL FUNCTION LOOKUP
# =========================================================

system_model_functions = {
    "Primary": modelPrimary,
    "Secondary": modelSecondary,
    "Tertiary": modelTertiary
}


# =========================================================
# RUN MODEL
# =========================================================

for index, system in ordered_systems.iterrows():

    system_name = system["Name"]
    system_type = system["Type"]

    combined_input_stream = calcCombinedStreamToSystem(
        system_name,
        pathways,
        nodes,
        analytes
    )

    model_function = system_model_functions[system_type]

    output_stream, performance_results = model_function(
        system,
        combined_input_stream,
        performance_benchmarks,
        modelling_constants
    )

    nodes.loc[system_name, "Flow"] = output_stream.loc[0, "Flow"]

    for analyte in analytes:
        nodes.loc[system_name, analyte] = output_stream.loc[0, analyte]

    summary_row = {
        "System": system_name,
        **performance_results
    }

    if system_type == "Primary":

        df_primary_performance_results = pd.concat(
            [df_primary_performance_results, pd.DataFrame([summary_row])],
            ignore_index=True
        )

    elif system_type == "Secondary":

        df_secondary_performance_results = pd.concat(
            [df_secondary_performance_results, pd.DataFrame([summary_row])],
            ignore_index=True
        )

    elif system_type == "Tertiary":

        df_tertiary_performance_results = pd.concat(
            [df_tertiary_performance_results, pd.DataFrame([summary_row])],
            ignore_index=True
        )


# =========================================================
# RESULTS TAB
# =========================================================

with results_tab:

    st.header("Performance Assessment Summary")

    if not df_primary_performance_results.empty:

        st.subheader("Primary Performance Results")

        st.dataframe(
            df_primary_performance_results,
            column_order=[
                "System",
                "Area (m²)",
                "SOR (m/hr)",
                "Benchmark SOR (m/hr)",
                "Status"
            ],
            hide_index=True,
            width="stretch"
        )

    if not df_secondary_performance_results.empty:

        st.subheader("Secondary Performance Results")

        st.dataframe(
            df_secondary_performance_results,
            column_order=[
                "System",
                "SRT (days)",
                "Estimated MLSS (mg/L)",
                "Benchmark MLSS (mg/L)",
                "Status"
            ],
            hide_index=True,
            width="stretch"
        )

    if not df_tertiary_performance_results.empty:

        st.subheader("Tertiary Performance Results")

        st.dataframe(
            df_tertiary_performance_results,
            column_order=[
                "System",
                "Filtration Rate (m/hr)",
                "Benchmark Filtration Rate (m/hr)",
                "Status"
            ],
            hide_index=True,
            width="stretch"
        )

    st.header("Final Node Outputs")

    st.dataframe(
        nodes,
        width="stretch"
    )


# =========================================================
# STATE POINT ANALYSIS TAB
# COMPLETELY STANDALONE FOR NOW
# =========================================================

with spa_tab:

    st.header("State Point Analysis")
    st.caption("Standalone mock-up — not linked to the process model.")

    col1, col2 = st.columns(2)

    with col1:

        spa_Qi = st.number_input(
            "Influent Flow Qi (m³/hr)",
            min_value=0.0,
            value=100.0,
            key="spa_Qi"
        )

        spa_Qr = st.number_input(
            "Recycle Flow Qr (m³/hr)",
            min_value=0.0,
            value=40.5,
            key="spa_Qr"
        )

        spa_A = st.number_input(
            "Clarifier Area A (m²)",
            min_value=0.01,
            value=55.0,
            key="spa_A"
        )

    with col2:

        spa_MLSS = st.number_input(
            "MLSS (kg/m³)",
            min_value=0.0,
            value=3.0,
            key="spa_MLSS"
        )

        spa_SVI = st.number_input(
            "SVI (mL/g)",
            min_value=0.0,
            value=150.0,
            key="spa_SVI"
        )

        spa_max_mlss = st.number_input(
            "Maximum concentration shown (kg/m³)",
            min_value=1.0,
            value=20.0,
            key="spa_max_mlss"
        )

    # -----------------------------------------------------
    # SPA CALCULATIONS
    # -----------------------------------------------------

    spa_x_range = np.linspace(0, spa_max_mlss, 1000)

    spa_j_tap = (spa_Qi + spa_Qr) * spa_MLSS / spa_A
    spa_vi = spa_Qi / spa_A
    spa_vr = spa_Qr / spa_A

    spa_recycle_ratio = spa_Qr / spa_Qi if spa_Qi > 0 else 0.0

    spa_v0 = 17.4 * np.exp(-0.0113 * spa_SVI)
    spa_p_hin = -0.9834 * np.exp(-0.00581 * spa_SVI) + 1.043
    spa_vs = spa_v0 * np.exp(-spa_p_hin * spa_x_range)

    spa_j_grav = spa_vs * spa_x_range
    spa_j_over = spa_vi * spa_x_range
    spa_j_under = -spa_vr * spa_x_range + spa_j_tap

    spa_j_state_point = spa_vi * spa_MLSS
    spa_j_overflowAtMLSS = spa_vi * spa_MLSS
    spa_j_gravityAtMLSS = (
        spa_v0
        * np.exp(-spa_p_hin * spa_MLSS)
        * spa_MLSS
    )

    spa_SHC2 = (
        spa_j_overflowAtMLSS
        < spa_j_gravityAtMLSS
    )

    spa_underflow_concentration = (
        spa_j_tap / spa_vr
        if spa_vr > 0
        else np.nan
    )

    # -----------------------------------------------------
    # SPA RESULTS
    # -----------------------------------------------------

    st.subheader("Results")

    spa_results = pd.DataFrame({
        "Parameter": [
            "Influent Flow",
            "Recycle Flow",
            "Recycle Ratio",
            "Clarifier Area",
            "MLSS",
            "SVI",
            "Overflow Velocity",
            "Recycle Velocity",
            "v₀",
            "Hindered Settling Parameter",
            "Overflow Flux at MLSS",
            "Gravity Flux at MLSS",
            "Underflow Concentration",
            "SHC2"
        ],
        "Value": [
            f"{spa_Qi:.2f} m³/hr",
            f"{spa_Qr:.2f} m³/hr",
            f"{spa_recycle_ratio:.3f}",
            f"{spa_A:.2f} m²",
            f"{spa_MLSS:.2f} kg/m³",
            f"{spa_SVI:.0f} mL/g",
            f"{spa_vi:.3f} m/hr",
            f"{spa_vr:.3f} m/hr",
            f"{spa_v0:.3f} m/hr",
            f"{spa_p_hin:.3f}",
            f"{spa_j_overflowAtMLSS:.3f} kg/m².hr",
            f"{spa_j_gravityAtMLSS:.3f} kg/m².hr",
            (
                f"{spa_underflow_concentration:.2f} kg/m³"
                if not np.isnan(spa_underflow_concentration)
                else "N/A"
            ),
            "PASS" if spa_SHC2 else "FAIL"
        ]
    })

    st.dataframe(
        spa_results,
        hide_index=True,
        width="stretch"
    )

    if spa_SHC2:
        st.success("SHC2 satisfied: overflow flux at MLSS is below the gravity flux.")
    else:
        st.error("SHC2 not satisfied: overflow flux at MLSS exceeds the gravity flux.")

    # -----------------------------------------------------
    # SPA PLOT
    # -----------------------------------------------------

    st.subheader("State Point Diagram")

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(
        spa_x_range,
        spa_j_grav,
        label="Gravity Flux"
    )

    ax.plot(
        spa_x_range,
        spa_j_over,
        label="Overflow"
    )

    ax.plot(
        spa_x_range,
        spa_j_under,
        label="Underflow"
    )

    ax.scatter(
        spa_MLSS,
        spa_j_state_point,
        s=80,
        label="State Point"
    )

    if not np.isnan(spa_underflow_concentration):

        ax.scatter(
            spa_underflow_concentration,
            0,
            s=60,
            label="Underflow Concentration"
        )

    ax.set_xlabel("Solids Concentration (kg/m³)")
    ax.set_ylabel("Solids Flux (kg/m².hr)")
    ax.set_title("State Point Analysis")
    ax.legend()
    ax.set_ylim(0, None)
    ax.set_xlim(0, spa_max_mlss)
    ax.grid(True)

    st.pyplot(fig)

    # -----------------------------------------------------
    # RAW SPA DATA
    # -----------------------------------------------------

    with st.expander("Show Calculation Data"):

        spa_calculation_data = pd.DataFrame({
            "Concentration (kg/m³)": spa_x_range,
            "Settling Velocity (m/hr)": spa_vs,
            "Gravity Flux (kg/m².hr)": spa_j_grav,
            "Overflow Flux (kg/m².hr)": spa_j_over,
            "Underflow Flux (kg/m².hr)": spa_j_under
        })

        st.dataframe(
            spa_calculation_data,
            hide_index=True,
            width="stretch"
        )
