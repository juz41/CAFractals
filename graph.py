#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

from simulation import Simulation, SimulationSetup
import setups
import sys

def pick_setup(setups):
    setup_list = list(setups.items())
    n_setups = len(setup_list)

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        try:
            idx = int(arg)
            if idx == -1:
                # Special case: run all setups
                print("Running all setups...")
                return "ALL", setup_list
            elif 0 <= idx < n_setups:
                name, s = setup_list[idx]
                print(f"Using setup #{idx}: {name}")
                return name, s
            else:
                print(f"Index {idx} out of range. Asking for input...")
        except ValueError:
            print(f"Argument '{arg}' is not a valid number. Asking for input...")

    print("Available setups:")
    for i, (name, _) in enumerate(setup_list):
        print(f"{i}: {name}")
    try:
        idx_input = input(f"Enter setup number [0-{n_setups-1}] (default 0): ")
        idx = int(idx_input)
        if idx == -1:
            print("Running all setups...")
            return "ALL", setup_list
        elif 0 <= idx < n_setups:
            name, s = setup_list[idx]
            print(f"Using setup #{idx}: {name}")
            return name, s
        else:
            print(f"Invalid number. Using default setup 0.")
    except (ValueError, EOFError):
        print("No valid input. Using default setup 0.")

    # 3. Fallback to first setup
    name, s = setup_list[0]
    print(f"Using default setup: {name}")
    return name, s

def run_simulation_and_plot(name, setup):
    print(f"Using setup: {name}")
    sim = Simulation(setup, SIZE, True)
    for step in range(INIT_STEPS):
        sim.step()
    sim.clear_history()

    for step in range(STEPS):
        sim.step()

    history = np.array(sim.history)
    n_states = history.shape[1]
    state_labels = setup.names

    colors = None
    if getattr(setup, "colors", None):
        colors = [normalize_color(c) for c in setup.colors[:n_states]]
    if colors is None:
        cmap = plt.get_cmap("tab10")
        colors = [cmap(i % 10) for i in range(n_states)]

    plt.figure(figsize=(10, 6))
    plt.gca().set_facecolor("#d3d3d3")  # light grey
    x = np.arange(history.shape[0])

    # Stack all states
    plt.stackplot(x, history.T, labels=state_labels, colors=colors)

    plt.title(f"State counts over time - setup: {name}, size {SIZE}x{SIZE}")
    plt.xlabel("Step")
    plt.ylabel("Number of cells")
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    SAVE_FILENAME = f"plots/{name}.png"
    plt.savefig(SAVE_FILENAME)
    print(f"Stacked plot saved to {SAVE_FILENAME}")
    # plt.show()

def normalize_color(col):
    if col is None:
        return None
    if isinstance(col, (tuple, list)) and all(isinstance(c, int) for c in col):
        return tuple(c / 255.0 for c in col)
    return col

INIT_STEPS = 25
SIZE = 30
STEPS = 2000

selected_name, selected_setup = pick_setup(setups.setups)
if selected_name == "ALL":
    for name, setup in selected_setup:
        run_simulation_and_plot(name, setup)
else:
    run_simulation_and_plot(selected_name, selected_setup)

