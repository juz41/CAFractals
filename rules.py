from abc import ABC, abstractmethod
import numpy as np

class IRule(ABC):
    @abstractmethod
    def check(self, curr, neighbor, sim):
        pass

class RandomRule(IRule):
    def __init__(self):
        pass

    def check(self, curr, neighbor, sim):
        return np.random.randint(neighbor.state_count)

class ClassicRule(IRule):
    def __init__(self, start, end, positivity, values):
        self.start = start
        self.end = end
        self.positivity = positivity
        self.values = values

    def check(self, curr, neighbor, sim):
        # print(str(curr)+" "+str(sim.grid[neighbor.location]))
        if curr != self.start:
            return -1
        for key,values in self.values.items():
            if self.positivity:
                if neighbor.neighbors[key] not in values:
                    return -1
            else:
                if neighbor.neighbors[key] in values:
                    return -1
        return self.end

class WeightedRandomRule(IRule):
    def __init__(self):
        pass

    def check(self, curr, neighbor, sim):
        counts = np.array(neighbor.neighbors)            
        probabilities = counts / counts.sum()
        return np.random.choice(np.arange(neighbor.state_count), p=probabilities)

class MajorityRule(IRule):
    def __init__(self):
        pass

    def check(self, curr, neighbor, sim):
        max = -1
        max_nei = -1
        arr = neighbor.neighbors
        for i in range(len(arr)):
            if arr[i] == max:
                max_nei = -1
            if arr[i] > max:
                max = arr[i]
                max_nei = i
        return max_nei

class ProbabilisticRule(IRule):
    def __init__(self, start, end, probability=1.0, neighbor_counts=None, positivity=True):
        self.start = start
        self.end = end
        self.probability = probability
        self.neighbor_counts = neighbor_counts or {}
        self.positivity = positivity

    def check(self, curr, neighbor, sim):
        if curr != self.start:
            return -1

        counts = neighbor.neighbors

        for state, valid_counts in self.neighbor_counts.items():
            if self.positivity:
                if counts[state] not in valid_counts:
                    return -1
            else:
                if counts[state] in valid_counts:
                    return -1

        if np.random.rand() < self.probability:
            return self.end
        else:
            return self.start

    
class Rules:
    def __init__(self):
        self.rules = []

    def add(self, rule):
        self.rules.append(rule)

    def check(self, state, neighbor, sim):
        for rule in self.rules:
            res = rule.check(state, neighbor, sim)
            if res != -1:
                return res
        return state
    
