from abc import ABC, abstractmethod
import numpy as np

class IRule(ABC):
    @abstractmethod
    def check(self, curr, neighbor, grid):
        pass

class RandomRule(IRule):
    def __init__(self):
        pass

    def check(self, curr, neighbor, grid):
        return np.random.randint(neighbor.state_count)

class ClassicRule(IRule):
    def __init__(self, start, end, positivity, values):
        self.start = start
        self.end = end
        self.positivity = positivity
        self.values = values

    def check(self, curr, neighbor, grid):
        # print(str(curr)+" "+str(grid[neighbor.location]))
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

    def check(self, curr, neighbor, grid):
        counts = np.array(neighbor.neighbors)            
        probabilities = counts / counts.sum()
        return np.random.choice(np.arange(neighbor.state_count), p=probabilities)

class MajorityRule(IRule):
    def __init__(self):
        pass

    def check(self, curr, neighbor, grid):
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
    
class Rules:
    def __init__(self):
        self.rules = []

    def add(self, rule):
        self.rules.append(rule)

    def check(self, state, neighbor, grid):
        for rule in self.rules:
            res = rule.check(state, neighbor, grid)
            if res != -1:
                return res
        return state
    
