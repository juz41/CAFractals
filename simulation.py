import numpy as np
from dataclasses import dataclass
from rules import Rules

@dataclass
class SimulationSetup():
    name: str
    n: int
    size: int
    state_count: int
    rules: Rules
    colors: list

class Simulation:
    def __init__(self, setup):
        self.n = setup.n
        self.size = setup.size
        self.state_count = setup.state_count
        self.shape = (setup.size,) * setup.n
        self.states = None
        self.grid = None
        self.offsets = None
        self.rules = setup.rules
        
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

