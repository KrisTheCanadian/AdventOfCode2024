#!/bin/bash

for day in $(seq -w 2 25); do
    copier copy --trust gh:gahjelle/template-aoc-python -d year=2024 -d day=$day -d puzzle_name="" -d puzzle_dir=$day 2024/
done
