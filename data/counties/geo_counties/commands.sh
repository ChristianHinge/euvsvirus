sed 's/{/{#/g' geojson-counties-fips.json | tr '#' '\n' | grep '"id"' | sed 's/.*"id": "//' | sed 's/".*//' > fips.txt
# how many IDs overlap?
cut -f1 < ../simulations/risk_index0.tsv | sed 1d | commul both - fips.txt
