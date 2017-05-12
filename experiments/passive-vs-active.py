
def compare(plt, plot, results):
    f, (a1, a2) = plt.subplots(1, 2)
    a1.set_aspect('equal', 'datalim')
    a2.set_aspect('equal', 'datalim')
    plot.vis(a1, results["passive"])
    plot.vis(a2, results["active"])
    f.suptitle("Passive vs. Active")
    return f
