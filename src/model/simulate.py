#!/usr/bin/env python3
import pandas as pd
from src.model.simulation.ODEs import simulate_SEIR_betas

populations = pd.read_table("data/counties/population.tsv", sep="\t")
fips2pop = dict(zip(populations["fips"], populations["population"]))

def simulate_county(fips, duration, beta, intervals=None, interval_beta_factors=None):
    I0 = 1
    N = fips2pop[fips]
    arr = simulate_SEIR_betas(duration, N-I0, I0=I0, beta=beta, intervals=intervals, interval_beta_factors=interval_beta_factors)
    return pd.DataFrame(arr, columns=["S", "E", "I", "R"])

