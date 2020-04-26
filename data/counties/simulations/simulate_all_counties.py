#!/usr/bin/env python3
import pandas as pd
from src.model.simulate import simulate_county
from matplotlib import pyplot as plt

density = pd.read_csv("data/counties/population/density.tsv", sep="\t")

arr = simulate_county(1043, 500, lockdown=[0, 200])
plt.plot(arr["Days"], arr["Infected"])
plt.plot(arr["Days"], arr["Susceptible"])

print("fips\tmax_icu\tmax_icu/icu_beds\tDead\tDead/pop")
for fips, pop in zip(density["fips"], density["population"]):
    arr = simulate_county(fips, 500)
    max_icu = max(arr["ICU"])
    icu_beds = arr.at[0, "icu_beds"]
    D = arr.at[len(arr)-1, "Dead"]
    print("\t".join(map(str, (fips, max_icu, max_icu/icu_beds, D, D/pop))))
