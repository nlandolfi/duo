import duo

def passive(plt, plot, results):
    f, a = plt.subplots()
    rs = results["passive"]
    plot.visualize(a,
            rs[0]["conditions"]["start"],
            rs[0]["conditions"]["goals"],
            trajectories=[r["trajectory"] for r in rs],
            #u_hs=[r["u_h"] for r in rs],
            c=plot.PASSIVE)
    return f

def active(plt, plot, results):
    f, a = plt.subplots()
    rs = results["active"]
    plot.visualize(a,
            rs[0]["conditions"]["start"],
            rs[0]["conditions"]["goals"],
            trajectories=[r["trajectory"] for r in rs],
            #u_hs=[r["u_h"] for r in rs],
            c=plot.ACTIVE)
    return f

def beliefs(plt, plot, results):
    f, a = plt.subplots()
    prs = results["passive"]
    ars = results["active"]
    plot.compare_beliefs(a,
            [[r["beliefs"] for r in prs],
             [r["beliefs"] for r in ars]],
            goal = 0,
            labels=["passive", "active"],
            colors=[plot.PASSIVE, plot.ACTIVE],
            multi=True)
    return f
