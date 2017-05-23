Duo
---

Duo is the companion code for the RSS workshop paper "Exploring Active Human Goal Inference in Shared Autonomy and Autonomous Driving" from the [InterACT lab](http://interact.berkeley.edu/).

I called it duo because all of our examples explore inference between _two_ goals.

### Running an Experiment

Write an `<experiement-name>`.json file in `experiments/` (see `experiments/` for examples). Optionall write an `<experiment-name`.py` companion python file, with functions for plotting the results (c.f. any of experiements/*.py).


The experiment can be run:
```
pyhonn exp.py experiments/<experiment-name>.json
```

### Organization of Code

 - `human.py` contains our human models
 - `robot.py` contains our robot models (algorithms)
 - `beliefs.py` contain the observation model, and bayesian inference utilities
 - `sim.py` simulates the interaction between a robot and human given initial config
 - `exp.py` takes an initial configuration (including algorithm for robot, model of robot, start, goals) and runs it, optinally creating plots of the results, whihch are defined in a companion file.


