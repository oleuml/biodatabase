#!/bin/sh
# This script executes all small python scripts,
# thus making execution in one step possible.
# Execute this command to make the script runnable: chmod u+x execute_all.sh
# Run it : ./execute_all.sh

# TODO: make it runnable in /src with /data
# TODO: make python script with data names (not in every file)
# TODO: could reduce for loops in the single scripts.

#python regex_chromosome.py
python model_to_pos.py
echo "Finished extracting positions of model & variants from chromosome 7."
python regex_annotation.py
echo "Finished extracting annotations from chr7."
python pos_to_indexed.py
echo "Finished creating all indices with corresponding annotations and models."
