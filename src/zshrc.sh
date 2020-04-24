#!/usr/bin/env zsh

# get abs path of this script
SRC=$0:A:h
export PATH="$PATH:$SRC"
export PYTHONPATH="$PYTHONPATH:$SRC"

