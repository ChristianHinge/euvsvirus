grep '^2020-04-23' us-counties.csv | cat <(head -n1 us-counties.csv) - > cases_deaths.csv
# the file was manually edited afterwards to add make NYC -> NY county with 36061 fips
