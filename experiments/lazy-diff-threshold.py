def compare(plt, plot, results):
    f, a = plt.subplots(3, 2,
            figsize=(8, 9))
    for (j, base) in enumerate(["piby8", "piby2"]):
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

def compareshort(plt, plot, results):
    f, a = plt.subplots(3, 2,
            figsize=(8, 6))
    for (j, base) in enumerate(["piby8", "piby2"]):
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
    for (j, base) in enumerate(["piby8", "piby2"]):
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

def passivepiby8(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["passivepiby8"], c=plot.PASSIVE)
    return f
def activepiby8(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["activepiby8"], c=plot.PASSIVE)
    return f
def passivepiby2(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["passivepiby2"], c=plot.PASSIVE)
    return f
def activepiby2(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["activepiby2"], c=plot.PASSIVE)
    return f

def beliefspiby8(plt, plot, results):
    f, a = plt.subplots()
    plot.compare_beliefs(a,
            [results["passivepiby8"]["beliefs"],
             results["activepiby8"]["beliefs"]],
            goal = 0,
            labels=["passive", "active"],
            colors=[plot.PASSIVE, plot.ACTIVE])
    return f

def beliefspiby2(plt, plot, results):
    f, a = plt.subplots()
    plot.compare_beliefs(a,
            [results["passivepiby2"]["beliefs"],
             results["activepiby2"]["beliefs"]],
            goal = 0,
            labels=["passive", "active"],
            colors=[plot.PASSIVE, plot.ACTIVE])
    return f
