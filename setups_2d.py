import numpy as np
from simulation import SimulationSetup
from rules import *

colors = [(0, 0, 0), (255, 255, 255)]
game_rules = Rules()
game_rules.add(ClassicRule(0, 1, True, {1: [3]}))
game_rules.add(ClassicRule(1, 0, False, {1: [2, 3]}))
game_setup = SimulationSetup(n=2, state_count=2, rules=game_rules, colors=colors, offsets=None)

random_rules = Rules()
random_rules.add(RandomRule())
random_colors = [(100, 100, 100), (150, 150, 150), (200, 200, 200)]
random_setup = SimulationSetup(n=2, state_count=3, rules=random_rules, colors=random_colors, offsets=None)

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
    offsets=None
)

duel_colors = [(255, 255, 0), (0, 255, 255)]
duel_rules = Rules()
duel_rules.add(WeightedRandomRule())
duel_setup = SimulationSetup(
    n=2,
    state_count=2,
    rules=duel_rules,
    colors=duel_colors,
    offsets=None
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
    probability=0.7,
    neighbor_counts={1: [2,3,4]}
))
pp_rules.add(ProbabilisticRule(
    start=1,
    end=2,
    probability=0.5,
    neighbor_counts={2: [1,2,3,4,5,6,7,8]}
))
pp_rules.add(ProbabilisticRule(
    start=2,
    end=0,
    probability=0.85,
    neighbor_counts={1: [0]}
))
pp_rules.add(ProbabilisticRule(
    start=2,
    end=0,
    probability=0.85,
    neighbor_counts={2: [4,5,6,7,8,9]}
))
pp_rules.add(ProbabilisticRule(
    start=2,
    end=2,
    probability=0.8,
    neighbor_counts={1: [1,2,3,4,5,6,7,8]}
))
pp_setup = SimulationSetup(
    n=2,
    state_count=3,
    rules=pp_rules,
    colors=pp_colors,
    offsets=None
)


setups = {
    "Game Of Life": game_setup,
    "Random": random_setup,
    "Map": map_setup,
    "Rock Paper Scissors": rps_setup,
    "Duel" : duel_setup,
    "Prey-Predator" : pp_setup
}
