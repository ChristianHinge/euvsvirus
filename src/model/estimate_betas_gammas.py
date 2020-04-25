#!/usr/bin/env python3
import pandas as pd

county_age = pd.read_table("data/counties/county_health_rankings/county_age.tsv", sep="\t")
county_health = pd.read_table("data/counties/county_health_rankings/county_health_population.tsv", sep="\t")
county_uninsured = pd.read_table("data/counties/county_health_rankings/county_uninsured.tsv", sep="\t")







