import streamlit as st
import pandas as pd


# =========================================================
# PAGE
# =========================================================

st.title("Simple Process Model")


# =========================================================
# 1. INFLUENT SOURCES
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
    "COD": [
        450.0,
        300.0,
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
    key="source_editor"
)


# =========================================================
# 2. PRIMARY SYSTEMS
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
    column_config={
        "Type": None,
        "Modelling Order Group": None,
        "Modelling Order Specific": None
    },
    key="primary_editor"
)


# =========================================================
# 3. SECONDARY SYSTEMS
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
    column_config={
        "Type": None,
        "Modelling Order Group": None,
        "Modelling Order Specific": None
    },
    key="secondary_editor"
)


# =========================================================
# 4. TERTIARY SYSTEMS
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
    ]
})

tertiary_data = st.data_editor(
    default_tertiary_data,
    hide_index=True,
    num_rows="dynamic",
    column_config={
        "Type": None,
        "Modelling Order Group": None,
        "Modelling Order Specific": None
    },
    key="tertiary_editor"
)


# =========================================================
# 5. COMBINE SYSTEM DATAFRAMES
# =========================================================

systems = pd.concat(
    [
        primary_data,
        secondary_data,
        tertiary_data
    ],
    ignore_index=True
)

# Keep active systems only
systems = systems[
    systems["Active"] == True
].copy()

# Put systems into modelling order
ordered_systems = systems.sort_values(
    by=[
        "Modelling Order Group",
        "Modelling Order Specific"
    ]
)


# =========================================================
# 6. PATHWAYS
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
    key="pathway_editor"
)


# =========================================================
# 7. ANALYTE LIST
# =========================================================

analytes = [
    "TSS",
    "TN",
    "TP",
    "COD",
    "NH4",
    "NO3",
    "PO4"
]


# =========================================================
# 8. CREATE COMMON NODES DATAFRAME
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
# Add active influent sources to nodes
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
            "COD": row["COD"],
            "NH4": row["NH4"],
            "NO3": row["NO3"],
            "PO4": row["PO4"]
        }


# ---------------------------------------------------------
# Add active systems to nodes
# ---------------------------------------------------------

for index, row in ordered_systems.iterrows():

    system_name = row["Name"]

    nodes.loc[system_name] = {
        "Type": row["Type"],
        "Active": True,
        "Flow": 0.0,
        "TSS": 0.0,
        "TN": 0.0,
        "TP": 0.0,
        "COD": 0.0,
        "NH4": 0.0,
        "NO3": 0.0,
        "PO4": 0.0
    }


# =========================================================
# 9. COMBINE STREAMS ENTERING A SYSTEM
# =========================================================

def calcCombinedStreamToSystem(
    system_name,
    pathways,
    nodes,
    analytes
):

    # Find pathways entering this system
    incoming_pathways = pathways[
        pathways["Destination"] == system_name
    ].copy()


    # Join output information from the upstream nodes
    incoming_streams = incoming_pathways.merge(
        nodes,
        left_on="Source",
        right_index=True,
        how="left"
    )


    # Apply pathway split proportion to flow
    incoming_streams["Adjusted Flow"] = (
        incoming_streams["Flow"]
        * incoming_streams["Proportion"]
    )


    # Total combined flow
    total_flow = incoming_streams[
        "Adjusted Flow"
    ].sum()


    # Flow-weighted average concentrations
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


    # Return a standard one-row stream DataFrame
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
# 10. PRIMARY MODELLING FUNCTION
# =========================================================

def modelPrimary(
    system_data,
    combined_input_stream
):

    # -----------------------------------------------------
    # DESIGN INFORMATION
    # -----------------------------------------------------

    length = system_data["Length"]
    width = system_data["Width"]

    area = length * width


    # -----------------------------------------------------
    # HYDRAULIC PERFORMANCE
    # -----------------------------------------------------

    # Flow is ML/day
    flow = combined_input_stream.loc[
        0,
        "Flow"
    ]

    # Convert:
    # ML/day x 1000 = m3/day
    # /24 = m3/hr
    # /area = m/hr

    if area > 0:

        sor = (
            flow
            * 1000
            / 24
            / area
        )

    else:

        sor = 0.0


    # -----------------------------------------------------
    # PROCESS STREAM IMPACT
    # -----------------------------------------------------

    output_stream = combined_input_stream.copy()

    # Placeholder removals for now:
    # 20% TSS removal
    # 20% COD removal

    output_stream.loc[0, "TSS"] *= 0.8
    output_stream.loc[0, "COD"] *= 0.8

    # All other analytes pass through unchanged


    # -----------------------------------------------------
    # PERFORMANCE RESULTS
    # -----------------------------------------------------

    performance_results = {
        "Area (m²)": area,
        "SOR (m/hr)": sor
    }

    return output_stream, performance_results


# =========================================================
# 11. SECONDARY MODELLING PLACEHOLDER
# =========================================================

def modelSecondary(
    system_data,
    combined_input_stream
):

    # For now simply pass everything through
    output_stream = combined_input_stream.copy()

    performance_results = {}

    return output_stream, performance_results


# =========================================================
# 12. TERTIARY MODELLING PLACEHOLDER
# =========================================================

def modelTertiary(
    system_data,
    combined_input_stream
):

    # For now simply pass everything through
    output_stream = combined_input_stream.copy()

    performance_results = {}

    return output_stream, performance_results


# =========================================================
# 13. MODEL FUNCTION LOOKUP
# =========================================================

# This lets the main modelling loop remain generic.

system_model_functions = {
    "Primary": modelPrimary,
    "Secondary": modelSecondary,
    "Tertiary": modelTertiary
}


# =========================================================
# 14. RUN MODEL
# =========================================================

st.header("Model Results")


for index, system in ordered_systems.iterrows():

    system_name = system["Name"]
    system_type = system["Type"]

    st.subheader(system_name)


    # -----------------------------------------------------
    # COMBINE ALL STREAMS FEEDING THIS SYSTEM
    # -----------------------------------------------------

    combined_input_stream = calcCombinedStreamToSystem(
        system_name,
        pathways,
        nodes,
        analytes
    )


    st.write("Combined Input Stream")

    st.dataframe(
        combined_input_stream,
        hide_index=True,
        width="stretch"
    )


    # -----------------------------------------------------
    # FIND THE CORRECT SYSTEM MODELLING FUNCTION
    # -----------------------------------------------------

    model_function = system_model_functions[
        system_type
    ]


    # -----------------------------------------------------
    # RUN SYSTEM-SPECIFIC MODEL
    # -----------------------------------------------------

    output_stream, performance_results = model_function(
        system,
        combined_input_stream
    )


    # -----------------------------------------------------
    # STORE SYSTEM OUTPUT BACK INTO NODES
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

    st.write("Output Stream")

    st.dataframe(
        output_stream,
        hide_index=True,
        width="stretch"
    )


    # -----------------------------------------------------
    # DISPLAY PERFORMANCE RESULTS IF THEY EXIST
    # -----------------------------------------------------

    if performance_results:

        st.write("Performance Results")

        performance_df = pd.DataFrame(
            [performance_results]
        )

        st.dataframe(
            performance_df,
            hide_index=True,
            width="stretch"
        )


# =========================================================
# 15. FINAL NODE OUTPUTS
# =========================================================

st.header("Final Node Outputs")

st.dataframe(
    nodes,
    width="stretch"
)
