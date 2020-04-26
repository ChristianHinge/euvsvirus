#!/usr/bin/env zsh
cd ../../..
data/counties/simulations/simulate_all_counties.py > data/counties/simulations/county_risk.tsv
cd -
cut -f1,2 < county_risk.tsv | sed 1d | sed $'s/\t/: /' | sed 's/$/,/' | cat <(echo '{') - <(echo '}') > max_icu.json
cut -f1,3 < county_risk.tsv | sed 1d | sed $'s/\t/: /' | sed 's/$/,/' | cat <(echo '{') - <(echo '}') > max_icu_per_icu_beds.json
cut -f1,4 < county_risk.tsv | sed 1d | sed $'s/\t/: /' | sed 's/$/,/' | cat <(echo '{') - <(echo '}') > D.json
cut -f1,5 < county_risk.tsv | sed 1d | sed $'s/\t/: /' | sed 's/$/,/' | cat <(echo '{') - <(echo '}') > D_per_population.json
cut -f1,3,5 < county_risk.tsv | sed 1d | awk -F$'\t' '{print $1, $2*$3}' | tr ' ' '\t' | cat <(echo $'fips\trisk') - > risk_index.tsv
sed 1d risk_index.tsv | awk -F $'\t' '{printf "%05d %s\n", $1, $2}' | tr ' ' '\t' | cat <(head -n1 risk_index.tsv) - > risk_index0.tsv
cat risk_index0.tsv | sed 1d | sed $'s/\t/: /' | sed 's/$/,/' | cat <(echo '{') - <(echo '}') > risk_index.json
