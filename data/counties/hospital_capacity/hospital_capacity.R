#!/usr/bin/env Rscript
library(data.table)

setwd("/Users/christian/cwd/data/counties/hospital_capacity")


beds = fread("../../states/hospital_capacity/beds.tsv", sep="\t")
setnames(beds, "state", "st_abbr")
populations = fread("../population/density.tsv")

state_pop = populations[, .(st_population=sum(population)), by=st_abbr]
states = beds[state_pop, on="st_abbr"]
counties = populations[states, on="st_abbr"]
counties[,hospital_beds:=total_hospital_beds/st_population*population]
counties[,icu_beds:=total_icu_beds/st_population*population]
# remove some columns to clean up a bit
counties[,total_hospital_beds:=NULL]
counties[,total_icu_beds:=NULL]

fwrite(counties, "beds.tsv", sep="\t")
