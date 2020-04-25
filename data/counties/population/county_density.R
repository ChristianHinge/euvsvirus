
library(data.table)

setwd("/Users/christian/cwd/data/counties/population")


areas = fread("county_area.tsv", sep="\t")
populations = fread("population.tsv", sep="\t", header=F, col.names=c("location", "population"))
dens = areas[populations, on="location"]
dens[, density:=population/area_sqmi]

fwrite(dens, "density.tsv", sep="\t")
