#!/usr/bin/env python3
import pandas as pd
from src.model.simulate import simulate_county

density = pd.read_csv("data/counties/population/density.tsv", sep="\t")

arr = simulate_county(1043, 500)


print("fips\tmax_icu\tmax_icu/icu_beds\tD\tD/pop")
for fips, pop in zip(density["fips"], density["population"]):
    arr = simulate_county(fips, 500)
    max_icu = max(arr["ICU"])
    icu_beds = arr.at[0, "icu_beds"]
    D = arr.at[len(arr)-1, "D"]
    print("\t".join(map(str, (fips, max_icu, max_icu/icu_beds, D, D/pop))))
