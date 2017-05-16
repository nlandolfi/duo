
def compare(plt, plot, results):
    f, (a1, a2) = plt.subplots(1, 2)
    a1.set_aspect('equal', 'datalim')
    a2.set_aspect('equal', 'datalim')
    plot.vis(a1, results["passive"])
    plot.vis(a2, results["active"])
    f.suptitle("Passive vs. Active")
    return f

def passive(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["passive"], c=plot.PASSIVE)
    return f

def active(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["active"], c=plot.ACTIVE)
    return f

def beliefs(plt, plot, results):
    f, a = plt.subplots()
    plot.compare_beliefs(a,
            [results["passive"]["beliefs"],
             results["active"]["beliefs"]],
            goal = 0,
            labels=["passive", "active"],
            colors=[plot.PASSIVE, plot.ACTIVE])
    return f
