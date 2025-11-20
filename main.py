import numpy as np

class Simulation:
    def __init__(self, n, size, n_states):
        self.n = n
        self.size = size
        self.n_states = n_states
        self.shape = (size,) * n

        self.states = self._compute_states()
        self.grid = self._initialize_grid()

    def _max_neighbor_count(self):
        return 3 ** self.n

    def _compute_states(self):
        return [int(self._max_neighbor_count() ** (i - 1)) for i in range(self.n_states)]

    def _initialize_grid(self):
        return np.random.choice(self.states, size=self.shape)

    def reset(self):
        self.grid = self._initialize_grid()


sim = Simulation(3, 2, 3)
print(sim.grid)
