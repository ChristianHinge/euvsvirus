grep '^2020-04-23' us-counties.csv | cat <(head -n1 us-counties.csv) - > cases_deaths.csv
