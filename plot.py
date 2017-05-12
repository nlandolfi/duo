import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

palatino = fm.FontProperties(fname="./.Palatino-Roman.ttf")

def center(a, cx=0., cy=0., wx=2., wy=2.):
    """
        centers an axis object, with particular width given
    """
    a.set_xlim(cx-wx/2., cx+wx/2.)
    a.set_ylim(cy-wy/2., cy+wy/2.)

def slick(a):
    a.spines['right'].set_visible(False)
    a.spines['top'].set_visible(False)
    a.xaxis.set_ticks_position('bottom')
    a.yaxis.set_ticks_position('left')
    a.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')

def vis(a, result):
    return visualize(a,
        result["conditions"]["start"],
        result["conditions"]["goals"],
        trajectories=[result["trajectory"]],
        u_hs=[result["u_h"]])

def visualize(a, start, goals, trajectories=None, u_hs=None, c = "r"):
    """
        plots the start and goals and trajectory if provided
        on a 2D canvas

        use to visualize the results of simulate
    """
    a.axis('off')
    center(a, 0.5, 0.5, 1.1, 1.1)

    a.plot(start[0], start[1], 'co', alpha=0.5,
            markeredgewidth=0, markersize=14.0)
    for goal in goals:
        a.plot(goal[0], goal[1], 'go', alpha=0.5,
            markeredgewidth=0, markersize=14.0)

    if trajectories is not None:
        for trajectory in trajectories:
            for q in trajectory:
                a.plot(q[0], q[1],
                        c+'o', alpha=1.0/len(trajectories),
                        markeredgewidth=0, markersize=7.0)

    if u_hs is not None and trajectories is not None:
        for u_h, t in zip(u_hs, trajectories):
            for i in range(len(u_h)):
                if not np.allclose(u_h[i], np.zeros(u_h[i].shape)):
                    a.arrow(t[i][0], t[i][1], u_h[i][0], u_h[i][1], fc="k")


def plot_beliefs(a, beliefs, labels=None):
    """
        plot beliefs over time, use to visualize
        beliefs returned by simulate

        labels are "Goal i" if they aren't provided
    """
    slick(a)
    a.set_ylim([0, 1.05])
    for i in range(beliefs.shape[1]):
        if labels is None:
            label = "Goal " + repr(i)
        else:
            label = labels[i]

        a.plot(beliefs[:,i], label=label)
    a.legend(prop=palatino)

def compare_beliefs(a, belief_sets, goal=0, labels=None, colors=None, legend=True):
    slick(a)
    a.set_ylim([0, 1.05])
    a.set_ylabel("belief", fontproperties=palatino)
    for i in range(len(belief_sets)):
        if labels is None:
            label = "Belief " + repr(i)
        else:
            label = labels[i]

        if colors is not None:
            c = colors[i]
        else:
            c = None
        a.plot(belief_sets[i][:,goal], label=label, c=c)
    if legend:
        a.legend(prop=palatino)
