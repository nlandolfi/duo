
def compare(plt, plot, results):
    f, a = plt.subplots(1, 3, figsize=(11, 8))


    plot.vis(a[0], results["active30"], c = plot.ACTIVE)
    plot.vis(a[1], results["active60"], c = plot.ACTIVE)
    plot.vis(a[2], results["active90"], c = plot.ACTIVE)

    plt.tight_layout()
    return f

