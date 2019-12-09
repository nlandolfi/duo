def compare(plt, plot, results):
    f = plt.figure(figsize=(8, 6))

    a1 = f.add_subplot(221)
    a2 = f.add_subplot(222)

    plot.vis(a1, results["passive"], c = plot.PASSIVE)
    plot.vis(a2, results["active"], c = plot.ACTIVE)

    a3 = f.add_subplot(212)
    plot.compare_beliefs(a3,
            [results["passive"]["beliefs"],
             results["active"]["beliefs"]],
            goal = 0,
            labels=["Passive Inference", "Active Inference"],
            colors=[plot.PASSIVE, plot.ACTIVE])

    plt.tight_layout(h_pad=3.0)
    return f


def beliefs(plt, plot, results):
    f, a = plt.subplots()
    plot.compare_beliefs(a,
            [results["passive"]["beliefs"],
             results["active"]["beliefs"]],
            goal = 0,
            labels=["Passive Inference", "Active Inference"],
            colors=[plot.PASSIVE, plot.ACTIVE])
    return f

def passive(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["passive"], c=plot.PASSIVE)
    return f

def active(plt, plot, results):
    f, a = plt.subplots()
    plot.vis(a, results["active"], c=plot.ACTIVE)
    return f
