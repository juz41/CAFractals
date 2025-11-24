#!/usr/bin/env python

from simulation import Simulation, SimulationSetup
from rules import *

randomRules = Rules()
randomRules.add(RandomRule())
RandomSetup = SimulationSetup(
    "Random",
    n=4,
    state_count=3,
    rules=randomRules,
    colors=None,
    offsets=None,
)

sim = Simulation(RandomSetup, 3)

while True:
    print("-----------------------")
    print(sim.grid)
    sim.step()
    print("-----------------------")
    input()

