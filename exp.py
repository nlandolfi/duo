import sys
import imp

import matplotlib.pyplot as plt

import sim
import plot

def run(experiment):
    if "name" not in experiment:
        raise Exception()

    if "conditions" not in experiment:
        raise Exception()

    if "plots" not in experiment:
        raise Exception()

    results = sim.run(experiment["conditions"])

    if len(experiment["plots"]) == 0:
        return

    search = imp.find_module(experiment["name"], ["./experiments/"])
    m = imp.load_module(experiment["name"], *search)

    for p in experiment["plots"]:
        f = getattr(m, p)(plt, plot, results)
        f.savefig("plots/" + experiment["name"] + "-" + p)

if __name__ == '__main__':
    run(sim.load(sys.argv[1]))
