#!/usr/bin/env python

from simulation import Simulation, SimulationSetup
from rules import *

colors = [(0,0,0), (255,255,255)]
GameOfLifeRules = Rules()
GameOfLifeRules.add(ClassicRule(0,1,True, {1:[3]}))
GameOfLifeRules.add(ClassicRule(1,0,False, {1:[2,3]}))

GameOfLifeSetup = SimulationSetup(
    "Game Of Life",
    n=2,
    size=10,
    state_count=2,
    rules=GameOfLifeRules,
    colors=colors,
)

randomRules = Rules()
randomRules.add(RandomRule())
RandomSetup = SimulationSetup(
    "Random",
    n=2,
    size=3,
    state_count=3,
    rules=randomRules,
    colors=None,
)

sim = Simulation(RandomSetup)

while True:
    print("-----------------------")
    print(sim.grid)
    sim.step()
    print("-----------------------")
    input()

