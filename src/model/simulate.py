#!/usr/bin/env python3
import pandas as pd
from src.model.simulation.ODEs import simulate_SEIR_betas

populations = pd.read_csv("data/counties/population/density.tsv", sep="\t")
# betas = pd.read_csv("data/counties/betas.tsv", sep="\t")
# gammas = pd.read_csv("data/counties/gammas.tsv", sep="\t")
fips2pop = dict(zip(populations["fips"], populations["population"]))
# fips2beta = dict(zip(betas["fips"], betas["beta"]))
# fips2gamma = dict(zip(gammas["fips"], gammas["gamma"]))

def simulate_county(fips, duration, I0=1, intervals=None, interval_beta_factors=None):
    beta = 1/7
    gamma = 1/14
    # N, beta, gamma = fips2pop[fips], fips2beta[fips], fips2gamma[fips]
    N = fips2pop[fips]
    arr = simulate_SEIR_betas(duration, N-I0, I0=I0, beta=beta, gamma=gamma, intervals=intervals, interval_beta_factors=interval_beta_factors)
    arr = pd.DataFrame(arr, columns=["S", "E", "I", "R"])
    arr["t"] = arr.index
    return arr

