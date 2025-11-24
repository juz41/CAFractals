#!/usr/bin/env python

from simulation import Simulation, SimulationSetup
from rules import Rules, ClassicRule

colors = [(0,0,0), (255,255,255)]
rules = Rules()
rules.add(ClassicRule(0,1,True, {1:[3]}))
rules.add(ClassicRule(1,0,False, {1:[2,3]}))

GameOfLifeSetup = SimulationSetup(
    "Game Of Life",
    n=2,
    size=10,
    state_count=2,
    rules=rules,
    colors=colors,
)

sim = Simulation(GameOfLifeSetup)

while True:
    print("-----------------------")
    print(sim.grid)
    sim.step()
    print("-----------------------")
    input()

