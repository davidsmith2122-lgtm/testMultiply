"""
model.py

This file contains ONLY plain Python logic — no Streamlit, no UI code.
The idea: this file could later be reused as-is inside a FastAPI backend,
a script, a test suite, or anything else. The UI (app.py) is just one
possible "front end" for these functions.
"""


def calculate_stream(x: float, y: float) -> float:
    """
    Mock calculation for a single stream.
    Replace this with real wastewater modeling logic later.
    """
    return x * y


def calculate_system(input_value: float, factor: float) -> float:
    """
    Mock calculation for a 'system' that takes a single input
    (which might come from a user OR from another system's output)
    and applies some factor to it.
    """
    return input_value * factor


def run_process_flow(system_configs: dict) -> dict:
    """
    Given a dictionary describing multiple systems and where each one's
    input comes from (manual value, or another system's output),
    calculate results in order and return all outputs.

    system_configs example:
    {
        "System A": {"source": "manual", "value": 10, "factor": 1.5},
        "System B": {"source": "System A", "factor": 2.0},
    }
    """
    results = {}

    for name, config in system_configs.items():
        if config["source"] == "manual":
            input_value = config["value"]
        else:
            # pull the output from a previously calculated system
            input_value = results[config["source"]]

        results[name] = calculate_system(input_value, config["factor"])

    return results
