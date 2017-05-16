def compare(plt, plot, results):
    f, a = plt.subplots(3, 2)
    for (j, base) in enumerate(["lo", "hi"]):
        rp = results["passive" + base]
        plot.vis(a[0,j], rp)
        a[0,j].set_aspect('equal', 'datalim')
        ra = results["active" + base]
        plot.vis(a[1,j], ra)
        a[1,j].set_aspect('equal', 'datalim')
        plot.compare_beliefs(a[2,j], [rp["beliefs"], ra["beliefs"]], goal=0, labels=["passive", "active"], colors=["k", "r"], legend=False)
    f.suptitle("Boltzmann Different Temperature")
    return f
