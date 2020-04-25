#!/usr/bin/env zsh
cut -f5 population/density.tsv | sed 1d > fips.txt
