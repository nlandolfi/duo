#!/bin/bash

python exp.py experiments/boltzmann-passive-vs-active.json
python exp.py experiments/boltzmann-wrong-prior.json
python exp.py experiments/boltzmann-diff-temperature.json
python exp.py experiments/boltzmann-noisy-human.json

python exp.py experiments/lazy-passive-vs-active.json
python exp.py experiments/lazy-wrong-prior.json
python exp.py experiments/lazy-diff-threshold.json
