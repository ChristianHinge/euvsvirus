#!/usr/bin/env python3
import numpy as np
from src.model.simulate import simulate_county

fips = np.loadtxt("data/counties/fips.txt", dtype=int)

for _fips in fips:
    arr = simulate_county(_fips, 500)
    print("{}\t{}".format(_fips, max(arr["ICU"]) / arr["icu_beds"][0]))
