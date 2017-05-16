def compare(plt, plot, results):
    f, a = plt.subplots(3, 4)
    for (j, base) in enumerate(["0.1", "0.2", "0.3", "0.4"]):
        rp = results["passive" + base]
        plot.vis(a[0,j], rp)
        a[0,j].set_aspect('equal', 'datalim')
        ra = results["active" + base]
        plot.vis(a[1,j], ra)
        a[1,j].set_aspect('equal', 'datalim')
        plot.compare_beliefs(a[2,j], [rp["beliefs"], ra["beliefs"]], goal=0, labels=["passive", "active"], colors=["k", "r"], legend=False)
    f.suptitle("Boltzmann Wrong Prior")
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
