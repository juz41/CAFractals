import numpy as np
from simulation import SimulationSetup
from rules import *
import colorsys

colors = [(0, 0, 0), (255, 255, 255)]
game_rules = Rules()
game_rules.add(ClassicRule(0, 1, True, {1: [3]}))
game_rules.add(ClassicRule(1, 0, False, {1: [2, 3]}))
game_setup = SimulationSetup(n=2, state_count=2, rules=game_rules, colors=colors, offsets=None, names = ["Dead", "Alive"])

random_rules = Rules()
random_rules.add(RandomRule())
random_colors = [(100, 100, 100), (150, 150, 150), (200, 200, 200)]
random_setup = SimulationSetup(n=2, state_count=3, rules=random_rules, colors=random_colors, offsets=None, names = ["r1", "r2", "r3"])

map_colors = [
    (0, 0, 255),
    (255, 255, 150),
    (0, 200, 0),
]
map_rules = Rules()
map_rules.add(ClassicRule(
    start=0,
    end=1,
    positivity=True,
    values={1: [6, 7, 8]}
))
map_rules.add(ClassicRule(
    start=0,
    end=1,
    positivity=True,
    values={2: [5, 6, 7, 8]}
))
map_rules.add(ClassicRule(
    start=1,
    end=0,
    positivity=True,
    values={0: [5, 6, 7, 8]}
))
map_rules.add(ClassicRule(
    start=1,
    end=2,  
    positivity=True,
    values={1: [5, 6, 7, 8]}
))
map_rules.add(ClassicRule(
    start=1,
    end=2,
    positivity=True,
    values={2: [5, 6, 7, 8]}
))
map_rules.add(ClassicRule(
    start=2,
    end=1,
    positivity=True,
    values={0: [3, 4, 5, 6, 7, 8]}
))
map_rules.add(ClassicRule(
    start=2,
    end=1,
    positivity=True,
    values={1: [4, 5, 6, 7, 8]}
))
map_setup = SimulationSetup(
    n=2,
    state_count=3,
    rules=map_rules,
    colors=map_colors,
    offsets=None,
    names = ["water", "beach", "land"]
)

rps_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
rps_rules = Rules()
rps_rules.add(ClassicRule(0, 0, True, {2: [0, 1, 2]}))
rps_rules.add(ClassicRule(0, 2, True, {1: [0, 1, 2]}))
rps_rules.add(ClassicRule(1, 1, True, {0: [0, 1, 2]}))
rps_rules.add(ClassicRule(1, 0, True, {2: [0, 1, 2]}))
rps_rules.add(ClassicRule(2, 2, True, {1: [0, 1, 2]}))
rps_rules.add(ClassicRule(2, 1, True, {0: [0, 1, 2]}))
rps_setup = SimulationSetup(
    n=2,
    state_count=3,
    rules=rps_rules,
    colors=rps_colors,
    offsets=None,
    names = ["rock", "paper", "scissors"]
)

duel_colors = [(255, 255, 0), (0, 255, 255)]
duel_rules = Rules()
duel_rules.add(WeightedRandomRule())
duel_setup = SimulationSetup(
    n=2,
    state_count=2,
    rules=duel_rules,
    colors=duel_colors,
    offsets=None,
    names = ["s1", "s2"]
)

pp_colors = [
    (0, 0, 0),
    (0, 200, 0),
    (200, 0, 0),
]
pp_rules = Rules()
pp_rules.add(ProbabilisticRule(
    start=0,
    end=1,
    probability=0.8,
    neighbor_counts={1: [2,3,4]}
))
pp_rules.add(ProbabilisticRule(
    start=1,
    end=2,
    probability=0.4,
    neighbor_counts={2: [1,2,3,4,5,6,7,8]}
))
pp_rules.add(ProbabilisticRule(
    start=2,
    end=0,
    probability=1.0,
    neighbor_counts={1: [0]}
))
pp_rules.add(ProbabilisticRule(
    start=2,
    end=0,
    probability=0.95,
    neighbor_counts={2: [4,5,6,7,8,9]}
))
pp_setup = SimulationSetup(
    n=2,
    state_count=3,
    rules=pp_rules,
    colors=pp_colors,
    offsets=None,
    names = ["empty", "prey", "predator"]
)

# https://en.wikipedia.org/wiki/Cyclic_cellular_automaton
def cyclic_setup_factory(n: int):
    # Generate evenly spaced rainbow colors
    cyclic_colors = [
        tuple(int(c * 255) for c in colorsys.hsv_to_rgb(i / n, 1.0, 1.0))
        for i in range(n)
    ]

    cyclic_rules = Rules()

    for i in range(n):
        cyclic_rules.add(
            ClassicRule(
                start=i,
                end=(i + 1) % n,
                positivity=True,
                values={
                    (i + 1) % n: list(range(1, 9))
                }
            )
        )

    return SimulationSetup(
        n=2,
        state_count=n,
        rules=cyclic_rules,
        colors=cyclic_colors,
        offsets=None,
        names=[f"n_{i}" for i in range(n)]
    )

def setup_from_b_s(rule_string: str, alive_color=(255, 255, 255), dead_color=(0, 0, 0)):
    b_part, s_part = rule_string.upper().split('/')
    b_nums = [int(c) for c in b_part.replace('B','')]
    s_nums = [int(c) for c in s_part.replace('S','')]

    rules = Rules()
    rules.add(ClassicRule(start=0, end=1, positivity=True, values={1: b_nums}))
    rules.add(ClassicRule(start=1, end=1, positivity=True, values={1: s_nums}))
    all_counts = list(range(0, 9))
    dead_counts = [n for n in all_counts if n not in s_nums]
    rules.add(ClassicRule(start=1, end=0, positivity=True, values={1: dead_counts}))

    setup = SimulationSetup(
        n=2,
        state_count=2,
        rules=rules,
        colors=[dead_color, alive_color],
        offsets=None,
        names=["Dead", "Alive"]
    )
    return setup


setups = {
    "Game Of Life": game_setup,
    "Random": random_setup,
    "Map": map_setup,
    "Rock Paper Scissors": rps_setup,
    "Duel" : duel_setup,
    "Prey-Predator" : pp_setup,
    "Cyclic (Rainbow) 6" : cyclic_setup_factory(6),
    "Cyclic (Rainbow) 10" : cyclic_setup_factory(10),
    "Cyclic (Rainbow) 16" : cyclic_setup_factory(16),
    "Game Of Life (B3/S23)" : setup_from_b_s("B3/S23"),
    "Maze (B3/S12345)" : setup_from_b_s("B3/S12345"),
    "Mazectric (B3/S1234)" : setup_from_b_s("B3/S1234"),
}
