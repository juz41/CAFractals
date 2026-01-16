#!/usr/bin/env python

import numpy as np
from scipy.signal import correlate
from simulation import Simulation, SimulationSetup
import setups
import sys

INIT_STEPS = 25
SIZE = 30
STEPS = 2000

def run_time_correlation(name, setup):
    print(f"Running setup: {name}")
    sim = Simulation(setup, SIZE, True)

    # Wstępne kroki
    for _ in range(INIT_STEPS):
        sim.step()
    sim.clear_history()

    # Główna symulacja
    for _ in range(STEPS):
        sim.step()

    history = np.array(sim.history)  # shape: (steps, n_states)
    state_labels = setup.names

    try:
        prey_idx = state_labels.index("prey")
        predator_idx = state_labels.index("predator")
    except ValueError:
        print("Setup does not contain Prey/Predator states. Skipping.")
        return

    prey_counts = history[:, prey_idx]
    predator_counts = history[:, predator_idx]

    # Korelacja Pearsona
    time_corr = np.corrcoef(prey_counts, predator_counts)[0,1]

    # Cross-correlation i lag
    prey_mean = prey_counts - np.mean(prey_counts)
    predator_mean = predator_counts - np.mean(predator_counts)
    cross_corr = correlate(predator_mean, prey_mean, mode='full')
    lags = np.arange(-len(prey_counts)+1, len(prey_counts))
    best_lag = lags[np.argmax(cross_corr)]

    # Wyniki
    print(f"Time correlation (Pearson) Prey vs Predator: {time_corr:.3f}")
    print(f"Maximum cross-correlation lag: {best_lag} steps")

name = "Prey-Predator"
selected_name, selected_setup = name, setups.setups[name]
if selected_name == "ALL":
    for name, setup in selected_setup:
        run_time_correlation(name, setup)
else:
    run_time_correlation(selected_name, selected_setup)
