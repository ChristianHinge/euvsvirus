#!/usr/bin/env zsh
cut -f1,5 < county_health_population.tsv | tr -d '\r' | sed 1d | sed $'s/\t/: /' | sed 's/$/,/' | cat <(echo '{') - <(echo '}') > county_heath.json
cut -f-4 < county_health_population.tsv > ../population.tsv
