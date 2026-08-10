"""
model.py

Pure Python model logic — no Streamlit imports here at all.

IMPORTANT: This is a STRUCTURAL MOCKUP. The actual wastewater engineering
equations have NOT been supplied yet, so all calculations below are
placeholders (simple multipliers) purely to demonstrate how flow moves
from one process unit to the next. Swap the guts of calculate_unit()
out for real equations later — nothing else needs to change.
"""

import pandas as pd


# ---------------------------------------------------------
# Default process units.
#
# Each unit just says: "what type am I" and "where does my input
# come from". A source can be "Influent" or the name of any other
# unit. This one structure naturally covers:
#   - 1-to-1   (Secondary A only ever takes from Primary A)
#   - 1-to-many (nothing special needed — two units just both list
#                the same upstream unit as their source)
#   - many-to-1 (Tertiary 1 lists BOTH Secondary A and Secondary B —
#                this is your old convoluted SUMIF/FILTER, now just
#                a list)
#
# Units must be listed in a valid calculation order: every unit's
# inputs must already appear earlier in this dict (or be "Influent").
# ---------------------------------------------------------
DEFAULT_UNITS = {
    "Primary A":   {"type": "Primary",   "inputs": ["Influent"]},
    "Primary B":   {"type": "Primary",   "inputs": ["Influent"]},
    "Secondary A": {"type": "Secondary", "inputs": ["Primary A"]},
    "Secondary B": {"type": "Secondary", "inputs": ["Primary B"]},
    "Tertiary 1":  {"type": "Tertiary",  "inputs": ["Secondary A", "Secondary B"]},  # convergence point
}

# "General modelling parameters" — the stuff most people shouldn't touch.
# Grouped by unit TYPE for now (all Primaries share settings, etc.) —
# easy to switch to per-unit overrides later if needed.
DEFAULT_PARAMS = {
    "Primary":   {"removal_factor": 0.9},
    "Secondary": {"removal_factor": 0.8},
    "Tertiary":  {"removal_factor": 0.95},
}


def calculate_unit(unit_type: str, input_value: float, params: dict) -> float:
    """
    PLACEHOLDER calculation.

    Real version will take dimensions, number of units, influent
    characteristics, etc. and apply actual treatment equations.
    For now: just applies a flat "removal factor" to whatever flows in,
    so we can see numbers move through the system end to end.
    """
    factor = params.get(unit_type, {}).get("removal_factor", 1.0)
    return input_value * factor


def run_process_flow(units: dict, params: dict, external_sources: dict) -> dict:
    """
    Walks through `units` in the order given, calculating each one's
    output based on the sum of its input source(s).

    external_sources: e.g. {"Influent": 120}  -- values that come from
    outside the unit graph entirely (influent flow, in this mockup).

    Returns: {unit_name: output_value, ...} for every unit, plus the
    external sources themselves.
    """
    results = dict(external_sources)

    for name, config in units.items():
        input_value = sum(results[src] for src in config["inputs"])
        results[name] = calculate_unit(config["type"], input_value, params)

    return results


def check_pass_fail(results: dict, limit: float) -> str:
    """
    PLACEHOLDER pass/fail check.

    Real version will check actual consent/compliance limits per
    parameter (BOD, TSS, ammonia, etc.), not just a single number.
    For now: checks the LAST unit's output value against a flat limit.
    """
    final_value = list(results.values())[-1]
    return "PASS" if final_value <= limit else "FAIL"


def interpolate_adwf(growth_df: pd.DataFrame, year) -> float:
    """Look up ADWF for a given year from the growth table."""
    row = growth_df.loc[growth_df["year"] == year]
    if row.empty:
        return None
    return float(row["adwf"].values[0])
