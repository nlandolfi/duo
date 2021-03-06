import sys
import imp

import matplotlib.pyplot as plt

import sim
import plot

def replace(d, var):
    for key in d:
        val = d[key]
        if (type(val) == str or type(val) == unicode) and val[0] == "$":
            d[key] = var[val]
        if type(val) == dict:
            val = val.copy()
            d[key] = val
            replace(val, var)
        if type(val) == list:
            for (i, v) in enumerate(val):
                if type(v) == str and v[0] == "$":
                    raise Exception("overwritin glist value nick doesn't know if this works")
                    val[i] = var[v]

def expand(ic, variable_set):
    nic = ic.copy()
    replace(nic, variable_set)
    return nic

def repeat(reps, c):
    print(c)
    if reps == 1:
        return sim.run(c)
    else:
        return [sim.run(c) for i in range(reps)]

def run(experiment):
    if "name" not in experiment:
        raise Exception()

    if "conditions" not in experiment:
        raise Exception()

    if "variables" not in experiment:
        raise Exception()

    if "plots" not in experiment:
        raise Exception()

    reps = 1
    if "repetitions" in experiment:
        reps = experiment["repetitions"]

    vs = experiment["variables"]
    cs = experiment["conditions"]

    if len(experiment["variables"]) == 0:
        ics = [("default", cs)]
    else:
        ics = [(name, expand(cs, vs[name])) for name in vs]

    results = {name: repeat(reps, c) for (name, c) in ics}

    if len(experiment["plots"]) == 0:
        return

    search = imp.find_module(experiment["name"], ["./experiments/"])
    m = imp.load_module(experiment["name"], *search)

    for p in experiment["plots"]:
        f = getattr(m, p)(plt, plot, results)
        f.savefig("plots/" + experiment["name"] + "-" + p, transparent=True)

if __name__ == '__main__':
    run(sim.load(sys.argv[1]))
