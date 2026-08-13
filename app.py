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


# Convert nested dictionary to editable DataFrame

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


# Convert edited DataFrame back to nested dictionary

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

    # Heterotrophic yield
    "Yh": 0.45,

    # Heterotrophic endogenous decay rate (/day)
    "bH": 0.24,

    # Endogenous residue fraction
    "fh": 0.20,

    # COD / VSS conversion
    "fcv": 1.48,

    # Inert/inorganic solids generated relative
    # to live biomass inventory
    "f_inert_biomass": 0.15
}


constants_data = pd.DataFrame({

    "Constant":
        list(default_modelling_constants.keys()),

    "Value":
        list(default_modelling_constants.values())
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


# Convert editable constants table back to dictionary

modelling_constants = {}

for index, row in constants_data.iterrows():

    modelling_constants[
        row["Constant"]
    ] = row["Value"]


# =========================================================
# 3. INFLUENT SOURCES
# =========================================================

st.header("Influent Sources")


default_source_data = pd.DataFrame({

    "Name": [
        "Influent Source 1",
        "Influent Source 2",
        "Influent Source 3",
        "Influent Source 4"
    ],

    "Active": [
        True,
        False,
        False,
        False
    ],

    # ML/day
    "Flow": [
        10.0,
        10.0,
        0.0,
        0.0
    ],

    # mg/L
    "TSS": [
        200.0,
        100.0,
        0.0,
        0.0
    ],

    "ISS": [
        40.0,
        30.0,
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
# 4. DERIVED COD COLUMNS
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


# Ensure backend fields are populated even for new rows

primary_data["Type"] = "Primary"

primary_data["Modelling Order Group"] = 1

primary_data["Modelling Order Specific"] = range(
    1,
    len(primary_data) + 1
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

    # m3
    "Volume": [
        5000.0,
        5000.0,
        5000.0,
        5000.0
    ],

    # days
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

        "Secondary Type":
            st.column_config.SelectboxColumn(

                options=[
                    "Conventional",
                    "MBR"
                ]
            )
    },

    key="secondary_editor"
)


secondary_data["Type"] = "Secondary"

secondary_data[
    "Modelling Order Group"
] = 2

secondary_data[
    "Modelling Order Specific"
] = range(
    1,
    len(secondary_data) + 1
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

    "Modelling Order Specific": [
        1,
        2,
        3,
        4
    ],

    # Placeholder for filtration modelling
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
        "Modelling Order Group": None,
        "Modelling Order Specific": None
    },

    key="tertiary_editor"
)


tertiary_data["Type"] = "Tertiary"

tertiary_data[
    "Modelling Order Group"
] = 3

tertiary_data[
    "Modelling Order Specific"
] = range(
    1,
    len(tertiary_data) + 1
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


# Active systems only

systems = systems[
    systems["Active"] == True
].copy()


# Put them into modelling order

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

    "ISS",

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
# 11. COMMON NODES DATAFRAME
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

    if row["Active"] == True:

        source_name = row["Name"]

        nodes.loc[source_name] = {

            "Type":
                "Influent Source",

            "Active":
                True,

            "Flow":
                row["Flow"],

            "TSS":
                row["TSS"],

            "ISS":
                row["ISS"],

            "TN":
                row["TN"],

            "TP":
                row["TP"],

            "NH4":
                row["NH4"],

            "NO3":
                row["NO3"],

            "PO4":
                row["PO4"],

            "Soluble biodegradable COD":
                row[
                    "Soluble biodegradable COD"
                ],

            "Particulate biodegradable COD":
                row[
                    "Particulate biodegradable COD"
                ],

            "Soluble non-biodegradable COD":
                row[
                    "Soluble non-biodegradable COD"
                ],

            "Particulate non-biodegradable COD":
                row[
                    "Particulate non-biodegradable COD"
                ],

            "Biodegradable COD":
                row[
                    "Biodegradable COD"
                ],

            "Non-biodegradable COD":
                row[
                    "Non-biodegradable COD"
                ],

            "Total COD":
                row[
                    "Total COD"
                ]
        }


# ---------------------------------------------------------
# ADD ACTIVE SYSTEM NODES
# ---------------------------------------------------------

for index, row in ordered_systems.iterrows():

    system_name = row["Name"]

    nodes.loc[system_name] = {

        "Type":
            row["Type"],

        "Active":
            True,

        "Flow":
            0.0,

        **{
            analyte: 0.0
            for analyte in analytes
        }
    }


# =========================================================
# 12. PERFORMANCE RESULT DATAFRAMES
# =========================================================

df_primary_performance_results = (
    pd.DataFrame()
)

df_secondary_performance_results = (
    pd.DataFrame()
)

df_tertiary_performance_results = (
    pd.DataFrame()
)


# =========================================================
# 13. PERFORMANCE CLASSIFICATION
# =========================================================

def classifyPerformance(
    actual_value,
    benchmark,
    lower_is_better=True
):

    if lower_is_better:

        if actual_value > benchmark:

            return "FAIL"

        elif actual_value >= (
            0.9 * benchmark
        ):

            return "CRITICAL"

        else:

            return "PASS"

    else:

        if actual_value < benchmark:

            return "FAIL"

        elif actual_value <= (
            1.1 * benchmark
        ):

            return "CRITICAL"

        else:

            return "PASS"


# =========================================================
# 14. COMBINE STREAMS ENTERING SYSTEM
# =========================================================

def calcCombinedStreamToSystem(
    system_name,
    pathways,
    nodes,
    analytes
):

    # Find pathways entering system

    incoming_pathways = pathways[

        pathways["Destination"]
        == system_name

    ].copy()


    # Attach upstream-node output values

    incoming_streams = (
        incoming_pathways.merge(

            nodes,

            left_on="Source",

            right_index=True,

            how="left"
        )
    )


    # Remove pathways whose source
    # doesn't currently exist

    incoming_streams = (
        incoming_streams.dropna(
            subset=["Flow"]
        )
    )


    # Apply pathway proportion

    incoming_streams[
        "Adjusted Flow"
    ] = (

        incoming_streams["Flow"]

        * incoming_streams["Proportion"]
    )


    # Combined flow

    total_flow = (

        incoming_streams[
            "Adjusted Flow"
        ].sum()
    )


    # Flow-weighted concentrations

    if total_flow > 0:

        weighted_concentrations = (

            incoming_streams[
                analytes
            ]

            .multiply(

                incoming_streams[
                    "Adjusted Flow"
                ],

                axis=0
            )

            .sum()

            / total_flow
        )

    else:

        weighted_concentrations = (
            pd.Series(
                0.0,
                index=analytes
            )
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
    # DESIGN
    # -----------------------------------------------------

    length = system_data[
        "Length"
    ]

    width = system_data[
        "Width"
    ]

    area = length * width


    # -----------------------------------------------------
    # HYDRAULICS
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
    # PROCESS STREAM
    # -----------------------------------------------------

    output_stream = (
        combined_input_stream.copy()
    )


    # Placeholder:
    # 20% TSS removal

    output_stream.loc[
        0,
        "TSS"
    ] *= 1


    # For now:
    # 0% removal of COD fractions

    for cod_fraction in (
        cod_fraction_analytes
    ):

        output_stream.loc[
            0,
            cod_fraction
        ] *= 1


    # Recalculate derived COD

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
    # PERFORMANCE
    # -----------------------------------------------------

    performance_results = {

        "Area (m²)":
            area,

        "SOR (m/hr)":
            sor,

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
# 16. SECONDARY MODEL
# =========================================================

def modelSecondary(
    system_data,
    combined_input_stream,
    performance_benchmarks,
    modelling_constants
):


    # =====================================================
    # STREAM OUTPUT
    #
    # Secondary currently passes stream concentrations
    # through unchanged.
    #
    # The biomass / MLSS model below is currently used
    # for PERFORMANCE assessment only.
    # =====================================================

    output_stream = (
        combined_input_stream.copy()
    )


    # -----------------------------------------------------
    # INFLUENT
    # -----------------------------------------------------

    flow = combined_input_stream.loc[
        0,
        "Flow"
    ]


    biodegradable_cod = (

        combined_input_stream.loc[
            0,
            "Soluble biodegradable COD"
        ]

        +

        combined_input_stream.loc[
            0,
            "Particulate biodegradable COD"
        ]
    )


    particulate_non_biodegradable_cod = (

        combined_input_stream.loc[
            0,
            "Particulate non-biodegradable COD"
        ]
    )


    influent_iss = (

        combined_input_stream.loc[
            0,
            "ISS"
        ]
    )


    # -----------------------------------------------------
    # SYSTEM DESIGN
    # -----------------------------------------------------

    volume = system_data[
        "Volume"
    ]

    srt = system_data[
        "SRT"
    ]

    secondary_type = system_data[
        "Secondary Type"
    ]


    # -----------------------------------------------------
    # MODELLING CONSTANTS
    # -----------------------------------------------------

    Yh = modelling_constants[
        "Yh"
    ]

    bH = modelling_constants[
        "bH"
    ]

    fh = modelling_constants[
        "fh"
    ]

    fcv = modelling_constants[
        "fcv"
    ]

    f_inert_biomass = (
        modelling_constants[
            "f_inert_biomass"
        ]
    )


    # -----------------------------------------------------
    # ACTIVE BIOMASS INVENTORY
    # -----------------------------------------------------

    if (
        1 + bH * srt
    ) != 0:

        mx_bh = (

            flow

            * biodegradable_cod

            * Yh

            * srt

            / (
                1
                + bH * srt
            )
        )

    else:

        mx_bh = 0.0


    # -----------------------------------------------------
    # ENDOGENOUS BIOMASS / RESIDUE
    # -----------------------------------------------------

    mx_eh = (

        mx_bh

        * fh

        * bH

        * srt
    )


    # -----------------------------------------------------
    # INERT PARTICULATE ORGANICS
    # -----------------------------------------------------

    if fcv > 0:

        mx_ii = (

            particulate_non_biodegradable_cod

            * flow

            / fcv

            * srt
        )

    else:

        mx_ii = 0.0


    # -----------------------------------------------------
    # INORGANIC SUSPENDED SOLIDS INVENTORY
    # -----------------------------------------------------

    mx_iss = (

        influent_iss

        * flow

        * srt

        +

        f_inert_biomass

        * mx_bh
    )


    # -----------------------------------------------------
    # TOTAL MLSS INVENTORY
    # -----------------------------------------------------

    total_tss_mass = (

        mx_bh

        + mx_eh

        + mx_ii

        + mx_iss
    )


    # -----------------------------------------------------
    # MLSS CONCENTRATION
    # -----------------------------------------------------

    if volume > 0:

        estimated_mlss = (

            total_tss_mass

            / volume

            * 1000
        )

    else:

        estimated_mlss = 0.0


    # -----------------------------------------------------
    # SELECT BENCHMARK
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
    # PERFORMANCE RESULTS
    # -----------------------------------------------------

    performance_results = {

        "Secondary Type":
            secondary_type,

        "Inlet Flow (ML/d)":
            flow,

        "Inlet Biodegradable COD (mg/L)":
            biodegradable_cod,

        "SRT (days)":
            srt,

        "Volume (m³)":
            volume,

        "Active Biomass MX_BH (kg)":
            mx_bh,

        "Endogenous Biomass MX_EH (kg)":
            mx_eh,

        "Inert Particulate Organics MX_II (kg)":
            mx_ii,

        "ISS Inventory MX_ISS (kg)":
            mx_iss,

        "Total TSS Inventory (kg)":
            total_tss_mass,

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
# 17. TERTIARY MODEL
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

    system_name = system[
        "Name"
    ]

    system_type = system[
        "Type"
    ]


    st.subheader(
        system_name
    )


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
    # SELECT MODEL FUNCTION
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
    # SAVE OUTPUT STREAM INTO NODES
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
    # DISPLAY STREAM OUTPUT
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
    # DISPLAY PERFORMANCE RESULTS
    # -----------------------------------------------------

    if performance_results:

        st.write(
            "Performance Results"
        )


        performance_df = (
            pd.DataFrame(
                [performance_results]
            )
        )


        st.dataframe(
            performance_df,
            hide_index=True,
            width="stretch"
        )


    # -----------------------------------------------------
    # BUILD SYSTEM-TYPE PERFORMANCE SUMMARY
    # -----------------------------------------------------

    summary_row = {

        "System":
            system_name,

        **performance_results
    }


    if system_type == "Primary":

        df_primary_performance_results = (
            pd.concat(

                [
                    df_primary_performance_results,

                    pd.DataFrame(
                        [summary_row]
                    )
                ],

                ignore_index=True
            )
        )


    elif system_type == "Secondary":

        df_secondary_performance_results = (
            pd.concat(

                [
                    df_secondary_performance_results,

                    pd.DataFrame(
                        [summary_row]
                    )
                ],

                ignore_index=True
            )
        )


    elif system_type == "Tertiary":

        df_tertiary_performance_results = (
            pd.concat(

                [
                    df_tertiary_performance_results,

                    pd.DataFrame(
                        [summary_row]
                    )
                ],

                ignore_index=True
            )
        )


# =========================================================
# 20. PERFORMANCE ASSESSMENT SUMMARY
# =========================================================

st.header(
    "Performance Assessment Summary"
)


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

st.header(
    "Final Node Outputs"
)


st.dataframe(
    nodes,
    width="stretch"
)
