#!/usr/bin/env python

import numpy as np

class Simulation:
    def __init__(self, n, size, state_count, rules):
        self.n = n
        self.size = size
        self.state_count = state_count
        self.shape = (size,) * n
        self.states = None
        self.grid = None
        self.offsets = None
        self.rules = rules
        
        self._initialize_states()
        self._randomize_grid()
        self._initialize_offsets()
        
        self.neighbors_grid = np.zeros_like(self.grid, dtype=np.uint16)
        
    def _max_neighbor_count(self):
        return 3 ** self.n

    def _initialize_states(self):
        self.states = np.array([int(self._max_neighbor_count() ** (i)) for i in range(self.state_count)], dtype=np.uint16)

    def _randomize_grid(self):
        self.grid = np.random.choice(self.states, size=self.shape)

    def _initialize_offsets(self):
        self.offsets = []
        for delta in np.ndindex(*(3,) * self.n):
            offset = tuple(d - 1 for d in delta)
            if any(offset):
                self.offsets.append(offset)

    def reset(self):
        self.grid = self._initialize_grid()

    def _compute_neighbors(self):
        pad = 1
        padded = np.pad(self.grid, [(pad, pad)] * self.n, mode='constant', constant_values=0)

        self.neighbors_grid = np.zeros_like(self.grid, dtype=np.uint16)

        for off in self.offsets:
            slices = []
            for shift in off:
                if shift == -1:
                    slices.append(slice(0, -2))
                elif shift == 0:
                    slices.append(slice(1, -1))
                elif shift == +1:
                    slices.append(slice(2, None))

            shifted = padded[tuple(slices)]
            self.neighbors_grid += shifted

    def step(self):
        self._compute_neighbors()
        for index in np.ndindex(self.shape):
            neighbor = Neighbor(self.n, self.states, self.neighbors_grid[index])
            state = -1
            for i in range(len(self.states)):
                if self.grid[index] == self.states[i]:
                    state = i
                    break
            if state != -1:
                self.grid[index] = self.states[self.rules.check(state, neighbor)]


class Neighbor:
    def __init__(self, n, states, value):
        self.n = n
        self.states = states
        self.value = value
        self.neighbors = []
        self.compute_neighbors()
        
    def compute_neighbors(self):
        for i in range(len(self.states)-1):
            a = self.value % self.states[i+1]
            self.neighbors.append(int(a/self.states[i]))
            self.value -= a
        self.neighbors.append(int(self.value//self.states[-1]))

    def update(self, value):
        self.value = value
        self.compute_neighbors()

class Rule:
    def __init__(self, start, end, positivity, values):
        self.start = start
        self.end = end
        self.positivity = positivity
        self.values = values

    def check(self, neighbor):
        for key,values in self.values.items():
            if self.positivity:
                if neighbor.neighbors[key] in values:
                    return True
            else:
                if neighbor.neighbors[key] not in values:
                    return True
        return False
                

class Rules:
    def __init__(self):
        self.rules = []

    def add(self, rule):
        self.rules.append(rule)

    def check(self, state, neighbor):
        for rule in self.rules:
            if rule.start != state:
                continue
            if rule.check(neighbor):
                return rule.end
        return state

size = 10
n = 2
count = 2

rules = Rules()
rules.add(Rule(0,1,True, {1:[3]} ))
rules.add(Rule(1,0,False, {1:[2,3]} ))
sim = Simulation(n, size, count, rules)

while True:
    print("-----------------------")
    print(sim.grid)
    sim.step()
    print("-----------------------")
    print(sim.neighbors_grid)
    print(Neighbor(n, sim.states, sim.neighbors_grid[2,2]).neighbors)
    input()
