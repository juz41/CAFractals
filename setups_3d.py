import numpy as np
from simulation import SimulationSetup
from rules import *

colors_3d = [(0, 0, 0), (255, 0, 0)]
rules_3d = Rules()
rules_3d.add(ClassicRule(start=0, end=1, positivity=True, values={1:[5]}))
rules_3d.add(ClassicRule(start=1, end=0, positivity=True, values={1:[0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,26]}))  # anything not exactly 4 or 5
game3d_setup = SimulationSetup(
    n=3,
    state_count=2,
    rules=rules_3d,
    colors=colors_3d,
    offsets=None
)

rules3d_a = Rules()
rules3d_a.add(ClassicRule(start=0, end=1, positivity=True, values={1:[5]}))
rules3d_a.add(ClassicRule(start=1, end=1, positivity=True, values={1:[4,5,6]}))
rules3d_a.add(ClassicRule(start=1, end=0, positivity=True, values={1:[0,1,2,3,7,8,9,10,11,12,13,14,15,26]}))
setup3d_a = SimulationSetup(
    n=3,
    state_count=2,
    rules=rules3d_a,
    colors=[(0,0,0),(0,255,0)],
    offsets=None
)

rules3d_b = Rules()
rules3d_b.add(ClassicRule(start=0, end=1, positivity=True, values={1:[4,5,6]}))
rules3d_b.add(ClassicRule(start=1, end=1, positivity=True, values={1:[5,6,7]}))
rules3d_b.add(ClassicRule(start=1, end=0, positivity=True, values={1:[0,1,2,3,4,8,9,10,11,12,13,14,15,26]}))
setup3d_b = SimulationSetup(
    n=3,
    state_count=2,
    rules=rules3d_b,
    colors=[(0,0,0),(0,0,255)],
    offsets=None
)

rules3d_seeds = Rules()
rules3d_seeds.add(ClassicRule(start=0, end=1, positivity=True, values={1:[2]}))
rules3d_seeds.add(ClassicRule(start=1, end=0, positivity=True, values={1:list(range(0,27))}))  # die always
setup3d_seeds = SimulationSetup(
    n=3,
    state_count=2,
    rules=rules3d_seeds,
    colors=[(0,0,0),(255,255,255)],
    offsets=None
)

rules3d_crowded = Rules()
rules3d_crowded.add(ClassicRule(start=0, end=1, positivity=True, values={1:[6,7]}))
rules3d_crowded.add(ClassicRule(start=1, end=1, positivity=True, values={1:[5,6,7]}))
rules3d_crowded.add(ClassicRule(start=1, end=0, positivity=True, values={1:[0,1,2,3,4,8,9,10,11,12,13,14,15,26]}))
setup3d_crowded = SimulationSetup(
    n=3,
    state_count=2,
    rules=rules3d_crowded,
    colors=[(0,0,0),(255,165,0)],  # orange alive
    offsets=None
)


setups = {
    "Game Of Life 3D": game3d_setup,
    "3D Life Variant A": setup3d_a,
    "3D Life Variant B": setup3d_b,
    "3D Seeds": setup3d_seeds,
    "3D Dense Life": setup3d_crowded
}
