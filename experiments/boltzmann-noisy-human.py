def compare(plt, plot, results):
    f = plt.figure(figsize=(8, 6))

    a1 = f.add_subplot(221)
    a2 = f.add_subplot(222)

    ps = results["passive"]
    plot.visualize(a1,
            ps[0]["conditions"]["start"],
            ps[0]["conditions"]["goals"],
            trajectories=[r["trajectory"] for r in ps],
            #u_hs=[r["u_h"] for r in ps],
            c=plot.PASSIVE)
    ar = results["active"]
    plot.visualize(a2,
            ar[0]["conditions"]["start"],
            ar[0]["conditions"]["goals"],
            trajectories=[r["trajectory"] for r in ar],
            #u_hs=[r["u_h"] for r in ar],
            c=plot.ACTIVE)

    a3 = f.add_subplot(212)

    prs = results["passive"]
    ars = results["active"]
    plot.compare_beliefs(a3,
            [[r["beliefs"] for r in prs],
             [r["beliefs"] for r in ars]],
            goal = 0,
            labels=["Passive Inference", "Active Inference"],
            colors=[plot.PASSIVE, plot.ACTIVE],
            multi=True)

    plt.tight_layout(h_pad=3.0)
    return f


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
