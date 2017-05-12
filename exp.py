import sys
import imp

import matplotlib.pyplot as plt

import sim

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

    search = imp.find_module(experiment["name"], ["./"])
    m = imp.load_module(experiment["name"], *search)

    for plot in experiment["plots"]:
        f = getattr(m, plot)(plt, results)
        f.savefig("plots/" + plot)

if __name__ == '__main__':
    run(sim.load(sys.argv[1]))
