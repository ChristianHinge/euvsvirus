#!/usr/bin/env python3
import numpy as np
import pandas as pd
from src.model.simulation.ODEs import simulate_SEIR_betas

## constants
ICU_duration = 5
# fractions of removed that die as a function of age group [<18, otherwise, >=65]
# numbers from Hinge.
removed_fatality = np.asarray([0.103181947, 0.842995744, 8.199770342]) / 100
# beta_factors for lock-down, panic and partial lock-down 
# for a typical beta, gamma, r0 (1/7, 1/14, r0=2) to a beta that results in r0 = 1, 3, 1.5
# r0 = beta_factor * beta / gamma => beta_factor = r0 * gamma / beta = r0 / 2
BETA_FACTORS = [1/2, 3/2, 1.5/2]

# read
populations = pd.read_csv("data/counties/population/density.tsv", sep="\t")
age_groups = pd.read_csv("data/counties/county_health_rankings/county_age.tsv", sep="\t")
betas = pd.read_csv("data/counties/betas.tsv", sep="\t")
beds = pd.read_csv("data/counties/hospital_capacity/beds.tsv", sep="\t")
recovered = pd.read_csv("data/counties/deaths/fatality_estimates.tsv", sep="\t")
fips2pop = dict(zip(populations["fips"], populations["population"]))
fips2beta = dict(zip(betas["fips"], betas["beta"]))
fips2age = dict(zip(age_groups["fips"], zip(age_groups["percent_less_than_18_years_of_age"], age_groups["percent_65_and_over"])))
fips2beds = dict(zip(beds["fips"], zip(beds["hospital_beds"], beds["icu_beds"])))
fips2recovered = dict(zip(recovered["fips"], recovered["recovered_est"]))


def simulate_county(fips, duration, I0=1, lockdown=None, panic=None, partial_lockdown=None):
    """
    Simulate S,E,I,R,t,A,D,ICU from a county 
    :param fips: FIPS ID for county
    :param duration: int number of days to run simulation for
    :param I0: Number of infected at day 0
    :param lockdown: inclusive time interval for reduction of transmission rate
    :param panic: inclusive time interval for increase in transmission rate
    :param partial_lockdown: inclusive time interval for partial reduction of transmission rate
    :return: pandas DataFrame
    """
    intervals, beta_factors = [], []
    if lockdown is not None:
        intervals.append(lockdown)
        beta_factors.append(BETA_FACTORS[0])
    if panic is not None:
        intervals.append(panic)
        beta_factors.append(BETA_FACTORS[1])
    if partial_lockdown is not None:
        intervals.append(partial_lockdown)
        beta_factors.append(BETA_FACTORS[2])
    
    arr = _simulate_county(fips, duration + ICU_duration, I0=I0, intervals=intervals, beta_factors=beta_factors)
    arr = _add_AD(arr, fips)
    arr = _add_ICU(arr)
    arr = _add_beds(arr, fips)
    return arr.iloc[:len(arr)-ICU_duration, :]


def _simulate_county(fips, duration, I0=1, intervals=None, beta_factors=None):
    """
    Simulate S,E,I,R,t from a county.
    :param fips: 
    :param duration: 
    :param I0: 
    :param intervals: 
    :param beta_factors: 
    :return: 
    """
    N = fips2pop[fips]
    R0 = fips2recovered[fips]
    beta = fips2beta[fips]
    arr = simulate_SEIR_betas(duration, N-I0-R0, I0=I0, R0=R0, beta=beta, intervals=intervals, beta_factors=beta_factors)
    arr = pd.DataFrame(arr, columns=["S", "E", "I", "R"])
    arr["t"] = arr.index
    return arr


def _add_AD(arr, fips):
    """
    Add A,D columns
    :param arr: 
    :param fips: 
    :return: 
    """
    ages = fips2age[fips]
    ages = np.asarray([ages[0], 100 - sum(ages), ages[1]]) / 100
    arr["D"] = sum(removed_fatality * ages) * arr["R"]
    arr["A"] = arr["R"] - arr["D"]
    return arr


def _add_ICU(arr):
    """
    Add ICU column.
    :param arr: has column D
    :return: 
    """
    daily_dead = np.diff(arr["D"])
    ICU = np.zeros(len(arr))
    for ICU_day in range(ICU_duration):
        ICU[:-ICU_day - 1] += daily_dead[ICU_day:]
    arr["ICU"] = ICU
    return arr


def _add_beds(arr, fips):
    arr["hospital_beds"], arr["icu_beds"] = fips2beds[fips]
    return arr

