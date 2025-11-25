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

setups = {
    "Game Of Life": game_setup,
    "Random": random_setup,
    "Map": map_setup,
    "Rock Paper Scissors": rps_setup,
    "Duel" : duel_setup, 
}

colors_3d = [(0, 0, 0), (255, 0, 0)]
rules_3d = Rules()
# 3D Game of Life rules:
# - Dead cell becomes alive if exactly 5 neighbors are alive
# - Alive cell dies if less than 4 or more than 5 neighbors are alive
rules_3d.add(ClassicRule(start=0, end=1, positivity=True, values={1:[5]}))
rules_3d.add(ClassicRule(start=1, end=0, positivity=True, values={1:[0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,26]}))  # anything not exactly 4 or 5

game3d_setup = SimulationSetup(
    n=3,
    state_count=2,
    rules=rules_3d,
    colors=colors_3d,
    offsets=None
)

setups_3d = {
    "Game Of Life 3D": game3d_setup,
}

# 1. Life3D Variant A — moderate birth/survival
rules3d_a = Rules()
# Birth if exactly 5 neighbors; survival if 4-6
rules3d_a.add(ClassicRule(start=0, end=1, positivity=True, values={1:[5]}))
rules3d_a.add(ClassicRule(start=1, end=1, positivity=True, values={1:[4,5,6]}))
rules3d_a.add(ClassicRule(start=1, end=0, positivity=True, values={1:[0,1,2,3,7,8,9,10,11,12,13,14,15,26]}))

setup3d_a = SimulationSetup(
    n=3,
    state_count=2,
    rules=rules3d_a,
    colors=[(0,0,0),(0,255,0)],  # black = dead, green = alive
    offsets=None
)

# 2. Life3D Variant B — “3-6 Life”: a bit more generous
rules3d_b = Rules()
rules3d_b.add(ClassicRule(start=0, end=1, positivity=True, values={1:[4,5,6]}))
rules3d_b.add(ClassicRule(start=1, end=1, positivity=True, values={1:[5,6,7]}))
rules3d_b.add(ClassicRule(start=1, end=0, positivity=True, values={1:[0,1,2,3,4,8,9,10,11,12,13,14,15,26]}))

setup3d_b = SimulationSetup(
    n=3,
    state_count=2,
    rules=rules3d_b,
    colors=[(0,0,0),(0,0,255)],  # blue alive
    offsets=None
)

# 3. 3D “Seeds-like” rule — only birth, no survival
#    Dead -> Alive if exactly 2 neighbors; Alive -> Dead always
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

# 4. More “crowded” 3D Life — birth if 6–7, survive if 5–7
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

# Then add them to your setups_3d dict:
setups_3d["3D Life Variant A"] = setup3d_a
setups_3d["3D Life Variant B"] = setup3d_b
setups_3d["3D Seeds"] = setup3d_seeds
setups_3d["3D Dense Life"] = setup3d_crowded
