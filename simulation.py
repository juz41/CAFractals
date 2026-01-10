import numpy as np
from dataclasses import dataclass
from rules import Rules

@dataclass
class SimulationSetup():
    n: int
    state_count: int
    rules: Rules
    colors: list
    offsets: list
    names: list

class Simulation:
    def __init__(self, setup, size, history_flag=False):
        self.n = setup.n
        self.size = size
        self.state_count = setup.state_count
        self.shape = (size,) * setup.n
        self.states = None
        self.states_dict = {}
        self.grid = None
        self.offsets = setup.offsets
        self.rules = setup.rules
        
        self._initialize_states()
        if self.offsets == None:
            self._initialize_offsets()
        self._randomize_grid()
        
        self.neighbors_grid = np.zeros_like(self.grid, dtype=np.uint16)

        self.history_flag = history_flag
        self.history = []
        
    def _max_neighbor_count(self):
        return 3 ** self.n

    def _initialize_states(self):
        self.states = np.array([int(self._max_neighbor_count() ** (i)) for i in range(self.state_count)], dtype=np.uint32)
        for i in range(len(self.states)):
            self.states_dict[self.states[i]] = i

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

        self.neighbors_grid = np.zeros_like(self.grid, dtype=np.uint32)

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
        new_grid = self.grid.copy()
        for index in np.ndindex(self.shape):
            neighbor = Neighbor(self.n, self.states, self.neighbors_grid[index], index)
            state = self.states_dict.get(self.grid[index], -1)
            if state != -1:
                new_grid[index] = self.states[self.rules.check(state, neighbor, self)]
        self.grid = new_grid
        if (self.history_flag):
            self.record_history()

    def record_history(self):
        counts = [np.sum(self.grid == state) for state in self.states]
        self.history.append(counts)

    def clear_history(self):
        self.history = []

class Neighbor:
    def __init__(self, n, states, value, location):
        self.location = location
        self.n = n
        self.states = states
        self.state_count = len(states)
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

