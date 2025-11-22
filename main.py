#!/usr/bin/env python

import numpy as np

class Simulation:
    def __init__(self, n, size, state_count):
        self.n = n
        self.size = size
        self.state_count = state_count
        self.shape = (size,) * n
        self.states = None
        self.grid = None
        self.offsets = None
        
        self._initialize_states()
        self._randomize_grid()
        self._initialize_offsets()
        
        self.neighbors_grid = np.zeros_like(self.grid, dtype=np.uint16)
        self._compute_neighbors()
        

    def _max_neighbor_count(self):
        return 3 ** self.n

    def _initialize_states(self):
        self.states = np.array([int(self._max_neighbor_count() ** (i - 1)) for i in range(self.state_count)], dtype=np.uint16)

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


    def _step(self):
        pass

class Neighbor:
    def __init__(self, n, states, value):
        self.n = n
        self.states = states
        self.value = value
        self.neighbors = []
        self.compute_neighbors()
        
    def compute_neighbors(self):
        for i in range(1, len(self.states)-1):
            a = self.value % self.states[i+1]
            self.value -= a
            self.neighbors.append(a)
        self.neighbors.append(self.value//self.states[-1])

    def update(self, value):
        self.value = value
        self.compute_neighbors()

class Rule:
    def __init__(self, start, end, postivity, values):
        self.start = start
        self.end = end
        self.positivty = positivty
        self.values = values

    def check(self, values):
        pass
        

n = 2
count = 3
sim = Simulation(n, 4, count)
print(sim.grid)
print("-----------------------")
print(sim.neighbors_grid)
print("-----------------------")
nei = Neighbor(n, sim.states, sim.neighbors_grid[1, 1])
print("-----------------------")
for val in nei.neighbors:
    print(val)
