def basic(plt, plot, results):
    results = results["low"]
    f, a = plt.subplots()
    plot.visualize(a,
        results["conditions"]["start"], results["conditions"]["goals"], trajectories=[results["trajectory"]], u_hs=[results["u_h"]])
    return f

