#!/usr/bin/env zsh
../../src/model/simulate.jl tmp.tsv -t 100 -S 100 --beta=1/7 --dtmax=5
echo $'t\tS\tE\tI\tR' | cat - tmp.tsv > SEIR_100days.tsv
table.py json SEIR_100days.{tsv,json} -H
