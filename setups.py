#!/usr/bin/env python

import setups_1d
import setups_2d
import setups_3d

setups = setups_1d.setups | setups_2d.setups | setups_3d.setups
