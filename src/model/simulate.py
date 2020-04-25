#!/usr/bin/env python3
import numpy as np
import pandas as pd
from src.model.simulation.ODEs import simulate_SEIR_betas

## constants
ICU_duration = 5
# fractions of removed that die as a function of age group [<18, otherwise, >=65]
# numbers from Hinge.
removed_fatality = np.asarray([0.103181947, 0.842995744, 8.199770342]) / 100

# read
populations = pd.read_csv("data/counties/population/density.tsv", sep="\t")
age_groups = pd.read_csv("data/counties/county_health_rankings/county_age.tsv", sep="\t")
betas = pd.read_csv("data/counties/betas.tsv", sep="\t")
fips2pop = dict(zip(populations["fips"], populations["population"]))
fips2beta = dict(zip(betas["fips"], betas["beta"]))
fips2age = dict(zip(age_groups["fips"], zip(age_groups["percent_less_than_18_years_of_age"], age_groups["percent_65_and_over"])))


def _simulate_county(fips, duration, I0=1, intervals=None, interval_beta_factors=None):
    """
    Simulate S,E,I,R,t from a county.
    :param fips: 
    :param duration: 
    :param I0: 
    :param intervals: 
    :param interval_beta_factors: 
    :return: 
    """
    N = fips2pop[fips]
    beta = fips2beta[fips]
    arr = simulate_SEIR_betas(duration, N-I0, I0=I0, beta=beta, intervals=intervals, interval_beta_factors=interval_beta_factors)
    arr = pd.DataFrame(arr, columns=["S", "E", "I", "R"])
    arr["t"] = arr.index
    return arr


def simulate_county(fips, duration, I0=1, intervals=None, interval_beta_factors=None):
    """
    Simulate S,E,I,R,t,A,D,ICU from a county 
    :param fips: 
    :param duration: 
    :param I0: 
    :param intervals: 
    :param interval_beta_factors: 
    :return: 
    """
    arr = _simulate_county(fips, duration + ICU_duration, I0=I0, intervals=intervals, interval_beta_factors=interval_beta_factors)
    ages = fips2age[fips]
    ages = np.asarray([ages[0], 100 - sum(ages), ages[1]]) / 100
    arr["D"] = sum(removed_fatality * ages) * arr["R"]
    arr["A"] = arr["R"] - arr["D"]
    daily_dead = np.diff(arr["D"])
    ICU = np.zeros(len(arr))
    for ICU_day in range(ICU_duration):
        ICU[:-ICU_day-1] += daily_dead[ICU_day:]
    arr["ICU"] = ICU
    return arr.iloc[:len(arr)-ICU_duration, :]


