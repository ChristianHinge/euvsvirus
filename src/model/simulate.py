#!/usr/bin/env python3
import pandas as pd
from src.model.simulation.ODEs import simulate_SEIR_betas

populations = pd.read_csv("data/counties/population/density.tsv", sep="\t")
fips2pop = dict(zip(populations["fips"], populations["population"]))

def simulate_county(fips, duration, I0=1, intervals=None, interval_beta_factors=None):
    N = fips2pop[fips]
    arr = simulate_SEIR_betas(duration, N-I0, I0=I0, beta=beta, intervals=intervals, interval_beta_factors=interval_beta_factors)
    arr = pd.DataFrame(arr, columns=["S", "E", "I", "R"])
    arr["t"] = arr.index
    return arr

