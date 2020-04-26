#!/usr/bin/env python3
import pandas as pd
from src.model.simulate import simulate_county

density = pd.read_csv("data/counties/population/density.tsv", sep="\t")

print("fips\tPeak ICU\tPeak ICU/ICU beds\tFatalities\tFatalities/population")
for fips, pop in zip(density["fips"], density["population"]):
    arr = simulate_county(fips, 500, floats=True)
    max_icu = max(arr["ICU"])
    icu_beds = arr.at[0, "ICU beds"]
    dead = arr.at[len(arr)-1, "Dead"]
    print("\t".join(map(str, (fips, max_icu, max_icu/icu_beds, dead, dead/pop))))
