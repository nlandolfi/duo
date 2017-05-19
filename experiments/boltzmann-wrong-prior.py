def compare01(plt, plot, results):
    f = plt.figure(figsize=(8, 6))

    a1 = f.add_subplot(221)
    a2 = f.add_subplot(222)

    plot.vis(a1, results["passive0.1"], c = plot.PASSIVE)
    plot.vis(a2, results["active0.1"], c = plot.ACTIVE)

    a3 = f.add_subplot(212)
    plot.compare_beliefs(a3,
            [results["passive0.1"]["beliefs"],
             results["active0.1"]["beliefs"]],
            goal = 0,
            labels=["Passive Inference", "Active Inference"],
            colors=[plot.PASSIVE, plot.ACTIVE])

    plt.tight_layout(h_pad=3.0)
    return f

def compare(plt, plot, results):
    f, a = plt.subplots(
            nrows=3,
            ncols=4,
            figsize=(16, 8),
            )
    for (j, base) in enumerate(["0.1", "0.2", "0.3", "0.4"]):
        rp = results["passive" + base]
        plot.vis(a[0,j], rp, c=plot.PASSIVE)
        #a[0,j].set_aspect('equal', 'datalim')
        ra = results["active" + base]
        plot.vis(a[1,j], ra, c=plot.ACTIVE)
        #a[1,j].set_aspect('equal', 'datalim')
        plot.compare_beliefs(a[2,j],
                [rp["beliefs"], ra["beliefs"]], goal=0, labels=["Passive Inference", "Active Inference"],
                colors=[plot.PASSIVE, plot.ACTIVE],
                legend=False)
    plt.tight_layout()
    return f

def compare3(plt, plot, results):
    f, a = plt.subplots(
            nrows=3,
            ncols=3,
            figsize=(8, 6.9),
            )
    for (j, base) in enumerate(["0.1", "0.2", "0.3"]):
        rp = results["passive" + base]
        plot.vis(a[0,j], rp, c=plot.PASSIVE)
        #a[0,j].set_aspect('equal', 'datalim')
        ra = results["active" + base]
        plot.vis(a[1,j], ra, c=plot.ACTIVE)
        #a[1,j].set_aspect('equal', 'datalim')
        plot.compare_beliefs(a[2,j],
                [rp["beliefs"], ra["beliefs"]], goal=0, labels=["Passive Inference", "Active Inference"],
                colors=[plot.PASSIVE, plot.ACTIVE],
                legend=False)
    plt.tight_layout(pad=0.0)
    return f

def passive01(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["passive0.1"], c=plot.PASSIVE)
    return f
def passive02(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["passive0.2"], c=plot.PASSIVE)
    return f
def passive03(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["passive0.3"], c=plot.PASSIVE)
    return f
def passive04(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["passive0.4"], c=plot.PASSIVE)
    return f

def active01(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["active0.1"], c=plot.ACTIVE)
    return f
def active02(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["active0.2"], c=plot.ACTIVE)
    return f
def active03(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["active0.3"], c=plot.ACTIVE)
    return f
def active04(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["active0.4"], c=plot.ACTIVE)
    return f

def beliefs01(plt, plot, results):
    f, a = plt.subplots()
    plot.compare_beliefs(a,
            [results["passive0.1"]["beliefs"],
             results["active0.1"]["beliefs"]],
            goal = 0,
            labels=["passive", "active"],
            colors=[plot.PASSIVE, plot.ACTIVE])
    return f
def beliefs04(plt, plot, results):
    f, a = plt.subplots()
    plot.compare_beliefs(a,
            [results["passive0.4"]["beliefs"],
             results["active0.4"]["beliefs"]],
            goal = 0,
            labels=["passive", "active"],
            colors=[plot.PASSIVE, plot.ACTIVE])
    return f
def beliefs03(plt, plot, results):
    f, a = plt.subplots()
    plot.compare_beliefs(a,
            [results["passive0.3"]["beliefs"],
             results["active0.3"]["beliefs"]],
            goal = 0,
            labels=["passive", "active"],
            colors=[plot.PASSIVE, plot.ACTIVE])
    return f
def beliefs02(plt, plot, results):
    f, a = plt.subplots()
    plot.compare_beliefs(a,
            [results["passive0.2"]["beliefs"],
             results["active0.2"]["beliefs"]],
            goal = 0,
            labels=["passive", "active"],
            colors=[plot.PASSIVE, plot.ACTIVE])
    return f
