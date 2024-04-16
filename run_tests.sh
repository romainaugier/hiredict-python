#!/bin/bash

python src/tests.py

if [[ $? -ne 0 ]]; then
    echo "Error during hiredict-python tests"
    exit 1 
fi