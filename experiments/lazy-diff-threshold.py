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
