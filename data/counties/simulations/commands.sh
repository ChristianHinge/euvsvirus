#!/usr/bin/env zsh
cd ../../..
data/counties/simulations/simulate_all_counties.py > data/counties/simulations/county_risk.tsv
cd -
cut -f1,3,5 < county_risk.tsv | sed 1d | awk -F$'\t' '{print $1, $2*$3}' | tr ' ' '\t' | cat <(echo $'fips\tRisk index') - > risk_index.tsv
cut -f1 < county_risk.tsv | awk '{if (NR == 1) {print} else {printf "%05d\n", $1}}' | paste - <(cut -f2- < county_risk.tsv) <(cut -f2 < risk_index.tsv) | tr '\t' ',' > risk_index0.csv
