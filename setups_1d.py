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
    offsets=None,
    names=["Dead", "Alive"]
)

sierp_rules = Rules()
sierp_rules.add(SierpinskiRule())
sierp_setup = SimulationSetup(
    n=1,
    state_count=2,
    rules=sierp_rules,
    colors=[(0, 0, 0), (255, 255, 255)],
    offsets=None,
    names=["Dead", "Alive"]
)

def setup_from_1d(rule_number: int, alive_color=(255, 255, 255), dead_color=(0, 0, 0)):
    rules = Rules()
    rules.add(RuleN(rule_number))

    setup = SimulationSetup(
        n=1,
        state_count=2,
        rules=rules,
        colors=[dead_color, alive_color],
        offsets=None,
        names=["Dead", "Alive"]
    )
    return setup


setups = {
    "1D Elementary" : one_d_setup,
    "Sierpinski Triangle" : sierp_setup,
    "Sierpinski Triangle (Rule90)" : setup_from_1d(90),
}
