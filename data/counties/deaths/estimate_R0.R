#!/usr/bin/env Rscript
library(data.table)

setwd("/Users/christian/cwd/data/counties/deaths")


removed_fatality = c(0.103181947, 0.842995744, 8.199770342) / 100


cases_deaths = fread("cases_deaths.csv", sep=",")
age_groups = fread("../county_health_rankings/county_age.tsv", sep="\t")
age_groups[,under18:=percent_less_than_18_years_of_age/100]
age_groups[,over65:=percent_65_and_over/100]
age_groups[,from18to65:=1-under18-over65]
# this fraction of who is infected will die
overall_fatality = rowSums(removed_fatality * age_groups[,.(under18,from18to65,over65)])
age_groups[,fatality_rate:=overall_fatality]

cases_deaths = cases_deaths[age_groups[,.(fips, fatality_rate)], on="fips"]
cases_deaths[,cases_fatality_est:=deaths / fatality_rate]
# some of the confirmed cases are actually higher (mostly for small numbers) 
# but I will not use something like pmax(cases, cases_fatality_est) since those cases are "ahead" of deaths.
cases_deaths[,recovered_est:=cases_fatality_est - deaths]

fwrite(na.omit(cases_deaths), "fatality_estimates.tsv", sep="\t")
