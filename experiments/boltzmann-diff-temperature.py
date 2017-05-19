def compare(plt, plot, results):
    f, a = plt.subplots(3, 2,
            figsize=(8, 9))
    for (j, base) in enumerate(["lo", "hi"]):
        rp = results["passive" + base]
        plot.vis(a[0,j], rp, c = plot.PASSIVE)
        ra = results["active" + base]
        plot.vis(a[1,j], ra, c = plot.ACTIVE)
        plot.compare_beliefs(
                a[2,j],
                [rp["beliefs"], ra["beliefs"]],
                goal=0,
                labels=["Passive Inference", "Active Inference"],
                colors=[plot.PASSIVE, plot.ACTIVE],
                legend=False)
    plt.tight_layout(pad=0)
    return f

def comparestack(plt, plot, results):
    f, a = plt.subplots(2, 3,
            figsize=(11, 8))
    for (j, base) in enumerate(["lo", "hi"]):
        rp = results["passive" + base]
        plot.vis(a[j,0], rp, c = plot.PASSIVE)
        ra = results["active" + base]
        plot.vis(a[j,1], ra, c = plot.ACTIVE)
        plot.compare_beliefs(
                a[j,2],
                [rp["beliefs"], ra["beliefs"]],
                goal=0,
                labels=["Passive Inference", "Active Inference"],
                colors=[plot.PASSIVE, plot.ACTIVE],
                legend=True,
                fontsize=16)
    plt.tight_layout(h_pad=7.0)
    return f
