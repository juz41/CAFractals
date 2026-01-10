import numpy as np
from simulation import SimulationSetup
from rules import *

colors_3d = [(0, 0, 0), (255, 0, 0)]
rules_3d = Rules()
rules_3d.add(ClassicRule(start=0, end=1, positivity=True, values={1:[5]}))
rules_3d.add(ClassicRule(start=1, end=1, positivity=True, values={1:[3,4,5,6]}))
rules_3d.add(ClassicRule(start=1, end=0, positivity=True, values={1:list(range(0, 28))}))
game3d_setup = SimulationSetup(
    n=3,
    state_count=2,
    rules=rules_3d,
    colors=colors_3d,
    offsets=None,
    names = ["Dead", "Alive"]
)

rules_3d_b = Rules()
rules_3d_b.add(ClassicRule(start=0, end=1, positivity=True, values={1:[3,4]}))
rules_3d_b.add(ClassicRule(start=1, end=1, positivity=True, values={1:[3,4]}))
rules_3d_b.add(ClassicRule(start=1, end=0, positivity=True, values={1:list(range(0, 28))}))
game3d_b_setup = SimulationSetup(
    n=3,
    state_count=2,
    rules=rules_3d_b,
    colors=[(0,0,0),(0,0,255)],
    offsets=None,
    names = ["Dead", "Alive"]
)


setups = {
    "Game Of Life 3D": game3d_setup,
    "Game Of Life 3D Sparse": game3d_b_setup,
}
