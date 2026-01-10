import numpy as np
from simulation import SimulationSetup
from rules import *

one_d_rules = Rules()
one_d_rules.add(RandomRule())
one_d_setup = SimulationSetup(
    n=1,
    state_count=2,
    rules=one_d_rules,
    colors=[(0, 0, 0), (255, 255, 255)],
    offsets=None
)


setups = {
    "1D Elementary" : one_d_setup,
}
