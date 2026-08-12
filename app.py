import streamlit as st
import pandas as pd


# =========================================================
# PAGE
# =========================================================

st.title("Simple Process Model")


# =========================================================
# 1. PERFORMANCE BENCHMARKS
# =========================================================

st.header("Performance Benchmarks")

# Internal nested dictionary structure
# Values are placeholders for prototype development

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


# Convert dictionary to simple editable table

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
        "System Type": st.column_config.TextColumn(
            disabled=True
        ),
        "Criterion": st.column_config.TextColumn(
            disabled=True
        ),
        "Benchmark": st.column_config.NumberColumn(
            min_value=0.0
        )
    },
    key="benchmark_editor"
)


# Rebuild nested dictionary after user editing

performance_benchmarks = {}

for index, row in benchmark_data.iterrows():

    system_type = row["System Type"]
    criterion = row["Criterion"]
    value = row["Benchmark"]

    if system_type not in performance_benchmarks:
        performance_benchmarks[system_type] = {}

    performance_benchmarks[system_type][criterion] = value


# =========================================================
# 2. MODELLING CONSTANTS
# =========================================================

st.header("Modelling Constants")

default_modelling_constants = {
    "Yh": 0.45,
    "bH": 0.24,
    "fh": 0.20,
    "fcv": 1.48
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
        "Constant": st.column_config.TextColumn(
            disabled=True
        ),
        "Value": st.column_config.NumberColumn(
            min_value=0.0
        )
    },
    key="constants_editor"
)


# Convert editable table back to dictionary

modelling_constants = {}

for index, row in constants_data.iterrows():

    modelling_constants[row["Constant"]] = row["Value"]


# =========================================================
# 3. INFLUENT SOURCES
# =========================================================

st.header("Influent Sources")


# We enter the FOUR fundamental COD fractions.
#
# Biodegradable COD,
# Non-biodegradable COD,
# and Total COD
# will be calculated from these.

default_source_data = pd.DataFrame({

    "Name": [
        "Influent Source 1",
        "Influent Source 2",
        "Influent Source 3",
        "Influent Source 4"
    ],

    "Active": [
        True,
        True,
        False,
        False
    ],

    "Flow": [
        10.0,
        10.0,
        0.0,
        0.0
    ],

    "TSS": [
        200.0,
        100.0,
        0.0,
        0.0
    ],

    "TN": [
        40.0,
        30.0,
        0.0,
        0.0
    ],

    "TP": [
        7.0,
        5.0,
        0.0,
        0.0
    ],

    "Soluble biodegradable COD": [
        100.0,
        80.0,
        0.0,
        0.0
    ],

    "Particulate biodegradable COD": [
        200.0,
        120.0,
        0.0,
        0.0
    ],

    "Soluble non-biodegradable COD": [
        50.0,
        40.0,
        0.0,
        0.0
    ],

    "Particulate non-biodegradable COD": [
        100.0,
        60.0,
        0.0,
        0.0
    ],

    "NH4": [
        25.0,
        20.0,
        0.0,
        0.0
    ],

    "NO3": [
        2.0,
        3.0,
        0.0,
        0.0
    ],

    "PO4": [
        4.0,
        2.0,
        0.0,
        0.0
    ]
})


source_data = st.data_editor(
    default_source_data,
    hide_index=True,
    num_rows="dynamic",
    width="stretch",
    key="source_editor"
)


# =========================================================
# 4. CALCULATE DERIVED COD COLUMNS
# =========================================================

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


# =========================================================
# 5. PRIMARY SYSTEMS
# =========================================================

st.header("Primary Systems")


default_primary_data = pd.DataFrame({

    "Name": [
        "Primary 1",
        "Primary 2",
        "Primary 3",
        "Primary 4"
    ],

    "Active": [
        True,
        False,
        False,
        False
    ],

    "Type": [
        "Primary",
        "Primary",
        "Primary",
        "Primary"
    ],

    "Modelling Order Group": [
        1,
        1,
        1,
        1
    ],

    "Modelling Order Specific": [
        1,
        2,
        3,
        4
    ],

    "Length": [
        30.0,
        30.0,
        30.0,
        30.0
    ],

    "Width": [
        10.0,
        10.0,
        10.0,
        10.0
    ]
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


# Make sure dynamically-added rows get the right backend values

primary_data["Type"] = "Primary"
primary_data["Modelling Order Group"] = 1
primary_data["Modelling Order Specific"] = (
    range(1, len(primary_data) + 1)
)


# =========================================================
# 6. SECONDARY SYSTEMS
# =========================================================

st.header("Secondary Systems")


default_secondary_data = pd.DataFrame({

    "Name": [
        "Secondary 1",
        "Secondary 2",
        "Secondary 3",
        "Secondary 4"
    ],

    "Active": [
        True,
        False,
        False,
        False
    ],

    "Type": [
        "Secondary",
        "Secondary",
        "Secondary",
        "Secondary"
    ],

    "Modelling Order Group": [
        2,
        2,
        2,
        2
    ],

    "Modelling Order Specific": [
        1,
        2,
        3,
        4
    ],

    "Secondary Type": [
        "Conventional",
        "Conventional",
        "Conventional",
        "Conventional"
    ],

    "Volume": [
        5000.0,
        5000.0,
        5000.0,
        5000.0
    ],

    "SRT": [
        15.0,
        15.0,
        15.0,
        15.0
    ]
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

        "Secondary Type": st.column_config.SelectboxColumn(
            options=[
                "Conventional",
                "MBR"
            ]
        )
    },

    key="secondary_editor"
)


secondary_data["Type"] = "Secondary"
secondary_data["Modelling Order Group"] = 2
secondary_data["Modelling Order Specific"] = (
    range(1, len(secondary_data) + 1)
)


# =========================================================
# 7. TERTIARY SYSTEMS
# =========================================================

st.header("Tertiary Systems")


default_tertiary_data = pd.DataFrame({

    "Name": [
        "Tertiary 1",
        "Tertiary 2",
        "Tertiary 3",
        "Tertiary 4"
    ],

    "Active": [
        False,
        False,
        False,
        False
    ],

    "Type": [
        "Tertiary",
        "Tertiary",
        "Tertiary",
        "Tertiary"
    ],

    "Modelling Order Group": [
        3,
        3,
        3,
        3
    ],

    # Placeholder attribute for future filtration assessment

    "Filter Area": [
        100.0,
        100.0,
        100.0,
        100.0
    ]
})


tertiary_data = st.data_editor(
    default_tertiary_data,
    hide_index=True,
    num_rows="dynamic",
    width="stretch",

    column_config={
        "Type": None,
        "Modelling Order Group": None
    },

    key="tertiary_editor"
)


tertiary_data["Type"] = "Tertiary"
tertiary_data["Modelling Order Group"] = 3
tertiary_data["Modelling Order Specific"] = (
    range(1, len(tertiary_data) + 1)
)


# =========================================================
# 8. COMBINE SYSTEM DATAFRAMES
# =========================================================

systems = pd.concat(
    [
        primary_data,
        secondary_data,
        tertiary_data
    ],
    ignore_index=True
)


systems = systems[
    systems["Active"] == True
].copy()


ordered_systems = systems.sort_values(
    by=[
        "Modelling Order Group",
        "Modelling Order Specific"
    ]
)


# =========================================================
# 9. PATHWAYS
# =========================================================

st.header("Pathways")


default_pathways = pd.DataFrame({

    "Source": [
        "Influent Source 1",
        "Influent Source 2",
        "Primary 1"
    ],

    "Destination": [
        "Primary 1",
        "Primary 1",
        "Secondary 1"
    ],

    "Proportion": [
        1.0,
        1.0,
        1.0
    ]
})


pathways = st.data_editor(
    default_pathways,
    hide_index=True,
    num_rows="dynamic",
    width="stretch",
    key="pathway_editor"
)


# =========================================================
# 10. ANALYTE LIST
# =========================================================

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
    "TN",
    "TP",
    "NH4",
    "NO3",
    "PO4"
]


analytes = (
    other_analytes
    + cod_fraction_analytes
    + derived_cod_analytes
)


# =========================================================
# 11. CREATE COMMON NODES DATAFRAME
# =========================================================

node_columns = [

    "Type",
    "Active",
    "Flow"

] + analytes


nodes = pd.DataFrame(
    columns=node_columns
)


# ---------------------------------------------------------
# ADD ACTIVE INFLUENT SOURCES
# ---------------------------------------------------------

for index, row in source_data.iterrows():

    if row["Active"]:

        source_name = row["Name"]

        nodes.loc[source_name] = {

            "Type": "Influent Source",

            "Active": True,

            "Flow": row["Flow"],

            "TSS": row["TSS"],
            "TN": row["TN"],
            "TP": row["TP"],

            "NH4": row["NH4"],
            "NO3": row["NO3"],
            "PO4": row["PO4"],

            "Soluble biodegradable COD":
                row["Soluble biodegradable COD"],

            "Particulate biodegradable COD":
                row["Particulate biodegradable COD"],

            "Soluble non-biodegradable COD":
                row["Soluble non-biodegradable COD"],

            "Particulate non-biodegradable COD":
                row["Particulate non-biodegradable COD"],

            "Biodegradable COD":
                row["Biodegradable COD"],

            "Non-biodegradable COD":
                row["Non-biodegradable COD"],

            "Total COD":
                row["Total COD"]
        }


# ---------------------------------------------------------
# ADD SYSTEM NODES
# ---------------------------------------------------------

for index, row in ordered_systems.iterrows():

    system_name = row["Name"]

    nodes.loc[system_name] = {

        "Type": row["Type"],

        "Active": True,

        "Flow": 0.0,

        **{
            analyte: 0.0
            for analyte in analytes
        }
    }


# =========================================================
# 12. PERFORMANCE RESULTS DATAFRAMES
# =========================================================

df_primary_performance_results = pd.DataFrame()

df_secondary_performance_results = pd.DataFrame()

df_tertiary_performance_results = pd.DataFrame()


# =========================================================
# 13. PERFORMANCE CLASSIFICATION FUNCTION
# =========================================================

def classifyPerformance(
    actual_value,
    benchmark,
    lower_is_better=True
):

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


# =========================================================
# 14. COMBINE STREAMS ENTERING A SYSTEM
# =========================================================

def calcCombinedStreamToSystem(
    system_name,
    pathways,
    nodes,
    analytes
):

    # Find pathways entering current system

    incoming_pathways = pathways[
        pathways["Destination"] == system_name
    ].copy()


    # Join upstream-node output data onto pathways

    incoming_streams = incoming_pathways.merge(
        nodes,
        left_on="Source",
        right_index=True,
        how="left"
    )


    # Ignore pathways referencing inactive/non-existing nodes

    incoming_streams = incoming_streams.dropna(
        subset=["Flow"]
    )


    # Apply pathway split proportion

    incoming_streams["Adjusted Flow"] = (

        incoming_streams["Flow"]

        * incoming_streams["Proportion"]
    )


    # Total flow to system

    total_flow = (
        incoming_streams["Adjusted Flow"]
        .sum()
    )


    # Flow-weighted concentrations

    if total_flow > 0:

        weighted_concentrations = (

            incoming_streams[analytes]

            .multiply(
                incoming_streams["Adjusted Flow"],
                axis=0
            )

            .sum()

            / total_flow
        )

    else:

        weighted_concentrations = pd.Series(
            0.0,
            index=analytes
        )


    combined_input_stream = (

        weighted_concentrations
        .to_frame()
        .T
    )


    combined_input_stream.insert(
        0,
        "Flow",
        total_flow
    )


    return combined_input_stream


# =========================================================
# 15. PRIMARY MODEL
# =========================================================

def modelPrimary(
    system_data,
    combined_input_stream,
    performance_benchmarks,
    modelling_constants
):

    # -----------------------------------------------------
    # SYSTEM DESIGN
    # -----------------------------------------------------

    length = system_data["Length"]

    width = system_data["Width"]

    area = length * width


    # -----------------------------------------------------
    # HYDRAULIC PERFORMANCE
    # -----------------------------------------------------

    flow = combined_input_stream.loc[
        0,
        "Flow"
    ]


    if area > 0:

        sor = (
            flow
            * 1000
            / 24
            / area
        )

    else:

        sor = 0.0


    benchmark_sor = (
        performance_benchmarks
        ["Primary"]
        ["SOR (m/hr)"]
    )


    status = classifyPerformance(
        sor,
        benchmark_sor,
        lower_is_better=True
    )


    # -----------------------------------------------------
    # PROCESS STREAM IMPACT
    # -----------------------------------------------------

    output_stream = combined_input_stream.copy()


    # Placeholder:
    # 20% TSS removal

    output_stream.loc[
        0,
        "TSS"
    ] *= 0.8


    # Placeholder:
    # 20% removal across all COD fractions

    for cod_fraction in cod_fraction_analytes:

        output_stream.loc[
            0,
            cod_fraction
        ] *= 0.8


    # Recalculate COD totals

    output_stream.loc[
        0,
        "Biodegradable COD"
    ] = (

        output_stream.loc[
            0,
            "Soluble biodegradable COD"
        ]

        +

        output_stream.loc[
            0,
            "Particulate biodegradable COD"
        ]
    )


    output_stream.loc[
        0,
        "Non-biodegradable COD"
    ] = (

        output_stream.loc[
            0,
            "Soluble non-biodegradable COD"
        ]

        +

        output_stream.loc[
            0,
            "Particulate non-biodegradable COD"
        ]
    )


    output_stream.loc[
        0,
        "Total COD"
    ] = (

        output_stream.loc[
            0,
            "Biodegradable COD"
        ]

        +

        output_stream.loc[
            0,
            "Non-biodegradable COD"
        ]
    )


    # -----------------------------------------------------
    # PERFORMANCE RESULTS
    # -----------------------------------------------------

    performance_results = {

        "Area (m²)": area,

        "SOR (m/hr)": sor,

        "Benchmark SOR (m/hr)":
            benchmark_sor,

        "Status":
            status
    }


    return (
        output_stream,
        performance_results
    )


# =========================================================
# 16. SECONDARY MODEL - PLACEHOLDER
# =========================================================

def modelSecondary(
    system_data,
    combined_input_stream,
    performance_benchmarks,
    modelling_constants
):

    # =====================================================
    # IMPORTANT
    #
    # Placeholder steady-state calculation only.
    # We will replace/refine this later.
    # =====================================================


    output_stream = (
        combined_input_stream.copy()
    )


    flow = combined_input_stream.loc[
        0,
        "Flow"
    ]


    biodegradable_cod = (
        combined_input_stream.loc[
            0,
            "Biodegradable COD"
        ]
    )


    particulate_non_biodegradable_cod = (
        combined_input_stream.loc[
            0,
            "Particulate non-biodegradable COD"
        ]
    )


    volume = system_data["Volume"]

    srt = system_data["SRT"]

    secondary_type = (
        system_data["Secondary Type"]
    )


    # -----------------------------------------------------
    # CONSTANTS
    # -----------------------------------------------------

    Yh = modelling_constants["Yh"]

    bH = modelling_constants["bH"]

    fh = modelling_constants["fh"]

    fcv = modelling_constants["fcv"]


    # -----------------------------------------------------
    # PLACEHOLDER BIOMASS CALCULATIONS
    # -----------------------------------------------------

    if (1 + bH * srt) > 0:

        mx_bh = (
            flow
            * biodegradable_cod
            * Yh
            * srt
            / (1 + bH * srt)
        )

    else:

        mx_bh = 0.0


    mx_eh = (
        mx_bh
        * fh
        * bH
        * srt
    )


    if fcv > 0:

        mx_inert = (
            particulate_non_biodegradable_cod
            * flow
            / fcv
            * srt
        )

    else:

        mx_inert = 0.0


    total_solids_mass = (
        mx_bh
        + mx_eh
        + mx_inert
    )


    if volume > 0:

        estimated_mlss = (
            total_solids_mass
            / volume
            * 1000
        )

    else:

        estimated_mlss = 0.0


    # -----------------------------------------------------
    # CHOOSE BENCHMARK
    # -----------------------------------------------------

    if secondary_type == "MBR":

        benchmark_mlss = (
            performance_benchmarks
            ["Secondary"]
            ["Max MLSS - MBR (mg/L)"]
        )

    else:

        benchmark_mlss = (
            performance_benchmarks
            ["Secondary"]
            ["Max MLSS - Conventional (mg/L)"]
        )


    status = classifyPerformance(
        estimated_mlss,
        benchmark_mlss,
        lower_is_better=True
    )


    # -----------------------------------------------------
    # STREAM IMPACT
    # -----------------------------------------------------

    # For now secondary has NO effect on the stream.
    #
    # We will replace this with the real process model later.


    # -----------------------------------------------------
    # PERFORMANCE RESULTS
    # -----------------------------------------------------

    performance_results = {

        "Secondary Type":
            secondary_type,

        "Estimated MLSS (mg/L)":
            estimated_mlss,

        "Benchmark MLSS (mg/L)":
            benchmark_mlss,

        "Status":
            status
    }


    return (
        output_stream,
        performance_results
    )


# =========================================================
# 17. TERTIARY MODEL - PLACEHOLDER
# =========================================================

def modelTertiary(
    system_data,
    combined_input_stream,
    performance_benchmarks,
    modelling_constants
):

    output_stream = (
        combined_input_stream.copy()
    )


    flow = combined_input_stream.loc[
        0,
        "Flow"
    ]


    filter_area = system_data[
        "Filter Area"
    ]


    if filter_area > 0:

        filtration_rate = (
            flow
            * 1000
            / 24
            / filter_area
        )

    else:

        filtration_rate = 0.0


    benchmark_rate = (
        performance_benchmarks
        ["Tertiary"]
        ["Filtration Rate (m/hr)"]
    )


    status = classifyPerformance(
        filtration_rate,
        benchmark_rate,
        lower_is_better=True
    )


    performance_results = {

        "Filtration Rate (m/hr)":
            filtration_rate,

        "Benchmark Filtration Rate (m/hr)":
            benchmark_rate,

        "Status":
            status
    }


    return (
        output_stream,
        performance_results
    )


# =========================================================
# 18. MODEL FUNCTION LOOKUP
# =========================================================

system_model_functions = {

    "Primary":
        modelPrimary,

    "Secondary":
        modelSecondary,

    "Tertiary":
        modelTertiary
}


# =========================================================
# 19. RUN MODEL
# =========================================================

st.header("Model Results")


for index, system in ordered_systems.iterrows():

    system_name = system["Name"]

    system_type = system["Type"]


    st.subheader(system_name)


    # -----------------------------------------------------
    # COMBINE UPSTREAM STREAMS
    # -----------------------------------------------------

    combined_input_stream = (
        calcCombinedStreamToSystem(
            system_name,
            pathways,
            nodes,
            analytes
        )
    )


    st.write(
        "Combined Input Stream"
    )


    st.dataframe(
        combined_input_stream,
        hide_index=True,
        width="stretch"
    )


    # -----------------------------------------------------
    # SELECT CORRECT MODEL FUNCTION
    # -----------------------------------------------------

    model_function = (
        system_model_functions[
            system_type
        ]
    )


    # -----------------------------------------------------
    # RUN SYSTEM MODEL
    # -----------------------------------------------------

    (
        output_stream,
        performance_results

    ) = model_function(

        system,
        combined_input_stream,
        performance_benchmarks,
        modelling_constants
    )


    # -----------------------------------------------------
    # SAVE STREAM OUTPUT INTO NODES
    # -----------------------------------------------------

    nodes.loc[
        system_name,
        "Flow"
    ] = output_stream.loc[
        0,
        "Flow"
    ]


    for analyte in analytes:

        nodes.loc[
            system_name,
            analyte
        ] = output_stream.loc[
            0,
            analyte
        ]


    # -----------------------------------------------------
    # DISPLAY OUTPUT STREAM
    # -----------------------------------------------------

    st.write(
        "Output Stream"
    )


    st.dataframe(
        output_stream,
        hide_index=True,
        width="stretch"
    )


    # -----------------------------------------------------
    # DISPLAY THIS SYSTEM'S PERFORMANCE
    # -----------------------------------------------------

    if performance_results:

        st.write(
            "Performance Results"
        )


        performance_df = pd.DataFrame(
            [performance_results]
        )


        st.dataframe(
            performance_df,
            hide_index=True,
            width="stretch"
        )


    # -----------------------------------------------------
    # ALSO BUILD SYSTEM-TYPE SUMMARY TABLES
    # -----------------------------------------------------

    summary_row = {
        "System": system_name,
        **performance_results
    }


    if system_type == "Primary":

        df_primary_performance_results = pd.concat(
            [
                df_primary_performance_results,
                pd.DataFrame([summary_row])
            ],
            ignore_index=True
        )


    elif system_type == "Secondary":

        df_secondary_performance_results = pd.concat(
            [
                df_secondary_performance_results,
                pd.DataFrame([summary_row])
            ],
            ignore_index=True
        )


    elif system_type == "Tertiary":

        df_tertiary_performance_results = pd.concat(
            [
                df_tertiary_performance_results,
                pd.DataFrame([summary_row])
            ],
            ignore_index=True
        )


# =========================================================
# 20. PERFORMANCE SUMMARY
# =========================================================

st.header("Performance Assessment Summary")


if not df_primary_performance_results.empty:

    st.subheader(
        "Primary Performance Results"
    )

    st.dataframe(
        df_primary_performance_results,
        hide_index=True,
        width="stretch"
    )


if not df_secondary_performance_results.empty:

    st.subheader(
        "Secondary Performance Results"
    )

    st.dataframe(
        df_secondary_performance_results,
        hide_index=True,
        width="stretch"
    )


if not df_tertiary_performance_results.empty:

    st.subheader(
        "Tertiary Performance Results"
    )

    st.dataframe(
        df_tertiary_performance_results,
        hide_index=True,
        width="stretch"
    )


# =========================================================
# 21. FINAL NODE OUTPUTS
# =========================================================

st.header("Final Node Outputs")


st.dataframe(
    nodes,
    width="stretch"
)
