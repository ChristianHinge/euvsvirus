#!/usr/bin/env Rscript
library(data.table)

setwd("/Users/christian/cwd/data/counties/deaths")


age_fatalities = c(0.103181947, 0.842995744, 8.199770342) / 100


cases_deaths = fread("cases_deaths.csv", sep=",")
populations = fread("../population/density.tsv", sep="\t")
health_table = fread("../county_health_rankings/county_health_population.tsv", sep="\t")
health_table[,health:=percent_fair_or_poor_health/100]
age_groups = fread("../county_health_rankings/county_age.tsv", sep="\t")
age_groups[,under18:=percent_less_than_18_years_of_age/100]
age_groups[,over65:=percent_65_and_over/100]
age_groups[,from18to65:=1-under18-over65]

# this fraction of who is infected will die
age_fatality_rate = rowSums(age_fatalities * age_groups[,.(under18,from18to65,over65)])
age_groups[,age_fatality_rate:=age_fatality_rate]
# we also add conservative consideration to the health of the population. 
# https://www.worldometers.info/coronavirus/coronavirus-age-sex-demographics/
# source says 5-10 times more deadly with preexisting condition. 
# We conservatively say that someone classified with "fair or poor health" will have "unhealthy_factor" times the fatality rate.
unhealthy_factor = 1.0
# We want to add this consideration while keeping the overall fatality rate of the nation unchanged.
populations = populations[age_groups[,.(fips,age_fatality_rate)],on="fips"]
populations = populations[health_table[,.(fips,health)], on="fips"]
# number of fatalities if everyone contracted corona
nation_fatalities = sum(populations$population * populations$age_fatality_rate, na.rm=T)
# it should hold:
# nation_fatalities == sum(populations$population * populations$age_fatality_rate * (unhealthy_factor * populations$health + (1-populations$health)) * constant, na.rm=T)
constant = nation_fatalities / sum(populations$population * populations$age_fatality_rate * (unhealthy_factor * populations$health + (1-populations$health)), na.rm=T)
# check
stopifnot(nation_fatalities == sum(populations$population * populations$age_fatality_rate * (unhealthy_factor * populations$health + (1-populations$health)) * constant, na.rm=T))
health_table = health_table[age_groups[,.(fips,age_fatality_rate)],on="fips"]
health_table[,fatality_rate:=age_fatality_rate*(unhealthy_factor * health + (1-health)) * constant]

cases_deaths = cases_deaths[health_table[,.(fips, fatality_rate)], on="fips"]
cases_deaths[,cases_fatality_est:=deaths / fatality_rate]
# some of the confirmed cases are actually higher (mostly for small numbers) 
# but I will not use something like pmax(cases, cases_fatality_est) since those cases are "ahead" of deaths.
cases_deaths[,recovered_est:=cases_fatality_est - deaths]
cases_deaths$recovered_est[is.na(cases_deaths$recovered_est)] = 0.0

fwrite(cases_deaths, "fatality_estimates.tsv", sep="\t")


