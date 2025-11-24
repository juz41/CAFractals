import numpy as np
from simulation import SimulationSetup
from rules import *

colors = [(0, 0, 0), (255, 255, 255)]
game_rules = Rules()
game_rules.add(ClassicRule(0, 1, True, {1: [3]}))
game_rules.add(ClassicRule(1, 0, False, {1: [2, 3]}))
game_setup = SimulationSetup("Game Of Life", n=2, state_count=2, rules=game_rules, colors=colors, offsets=None)

random_rules = Rules()
random_rules.add(RandomRule())
random_colors = [(100, 100, 100), (150, 150, 150), (200, 200, 200)]
random_setup = SimulationSetup("Random", n=2, state_count=3, rules=random_rules, colors=random_colors, offsets=None)


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
    "Map",
    n=2,
    state_count=3,
    rules=map_rules,
    colors=map_colors,
    offsets=None,
)

# Rock-Paper-Scissors
rps_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
rps_rules = Rules()
rps_rules.add(ClassicRule(0, 0, True, {2: [0, 1, 2]}))
rps_rules.add(ClassicRule(0, 2, True, {1: [0, 1, 2]}))
rps_rules.add(ClassicRule(1, 1, True, {0: [0, 1, 2]}))
rps_rules.add(ClassicRule(1, 0, True, {2: [0, 1, 2]}))
rps_rules.add(ClassicRule(2, 2, True, {1: [0, 1, 2]}))
rps_rules.add(ClassicRule(2, 1, True, {0: [0, 1, 2]}))
rps_setup = SimulationSetup(
    "Rock Paper Scissors",
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
    "Duel",
    n=2,
    state_count=2,
    rules=duel_rules,
    colors=duel_colors,
    offsets=None
)


colors_3d = [(0, 0, 0), (255, 0, 0)]
rules_3d = Rules()
# 3D Game of Life rules:
# - Dead cell becomes alive if exactly 5 neighbors are alive
# - Alive cell dies if less than 4 or more than 5 neighbors are alive
rules_3d.add(ClassicRule(start=0, end=1, positivity=True, values={1:[5]}))
rules_3d.add(ClassicRule(start=1, end=0, positivity=True, values={1:[0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,26]}))  # anything not exactly 4 or 5

game3d_setup = SimulationSetup(
    name="3D Game of Life",
    n=3,
    state_count=2,
    rules=rules_3d,
    colors=colors_3d,
    offsets=None
)

setups = {
    "Game Of Life": game_setup,
    "Random": random_setup,
    "Map": map_setup,
    "Rock Paper Scissors": rps_setup,
    "Duel" : duel_setup, 
}
