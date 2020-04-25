#!/usr/bin/env python3
import numpy as np
import pandas as pd
from src.utilities import array_util as ar

county_age = pd.read_csv("data/counties/county_health_rankings/county_age.tsv", sep="\t")
county_health = pd.read_csv("data/counties/county_health_rankings/county_health_population.tsv", sep="\t")
county_uninsured = pd.read_csv("data/counties/county_health_rankings/county_uninsured.tsv", sep="\t")
county_density = pd.read_csv("data/counties/population/density.tsv", sep="\t")

# there are fewer fips in county_density
# len(county_age["fips"].unique())
# len(county_health["fips"].unique())
# len(county_uninsured["fips"].unique())
# len(county_density["fips"].unique())

# USA r0 is [2.0,2.5] according to Hinge. The extremes of county density is NYC and some random place in alaska.
# we (log) interpolate r0 from 1 to 3 between these extremes
logdens = np.log(county_density["density"])
r0 = ar.lerp(1.5, 3.0, ar.lerp_inverse(min(logdens), max(logdens), logdens))
# r0 == beta / gamma => beta = r0 * gamma
# np.mean(r0) # around mid of [2.0,2.5]
beta = r0 / 14
county_betas = pd.DataFrame({"fips": county_density["fips"], "location": county_density["location"], "beta": beta})
county_betas.to_csv("data/counties/betas.tsv", sep="\t", index=False)


