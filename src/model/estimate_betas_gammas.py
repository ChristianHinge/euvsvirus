#!/usr/bin/env python3
import pandas as pd

county_age = pd.read_csv("data/counties/county_health_rankings/county_age.tsv", sep="\t")
county_health = pd.read_csv("data/counties/county_health_rankings/county_health_population.tsv", sep="\t")
county_uninsured = pd.read_csv("data/counties/county_health_rankings/county_uninsured.tsv", sep="\t")
county_density = pd.read_csv("data/counties/population/density.tsv", sep="\t")

# there are fewer fips in county_density
# len(county_age["fips"].unique())
# len(county_health["fips"].unique())
# len(county_uninsured["fips"].unique())
# len(county_density["fips"].unique())
fips = county_density["fips"]



