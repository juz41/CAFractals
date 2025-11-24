#!/usr/bin/env python

from simulation import *
from simulation2 import *
from rules import *
import setups

sim = Simulation(setups.setups["Game Of Life"], 100)

for i in range(10):
    # print(sim.grid)
    print(i)
    sim.step()
