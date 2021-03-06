import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches

import duo

palatino = fm.FontProperties(fname="./.Palatino-Roman.ttf")
palatino.set_size(20.0)

LIGHT_GRAY = (.6, .6, .6)
DARK_GRAY  = (.4, .4, .4)
ORANGE_RED = (1.0,0.27,0.)

PASSIVE = DARK_GRAY
ACTIVE  = ORANGE_RED

def center(a, cx=0., cy=0., wx=2., wy=2.):
    """
        centers an axis object, with particular width given
    """
    a.set_xlim(cx-wx/2., cx+wx/2.)
    a.set_ylim(cy-wy/2., cy+wy/2.)

def slick(a):
    a.spines['right'].set_visible(False)
    a.spines['top'].set_visible(False)
    a.spines['bottom'].set_visible(False)
    a.xaxis.set_ticks_position('bottom')
    a.yaxis.set_ticks_position('left')
    a.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')

def vis(a, result, **vargs):
    return visualize(a,
        result["conditions"]["start"],
        result["conditions"]["goals"],
        trajectories=[result["trajectory"]],
        u_hs=[result["u_h"]], **vargs)

def visualize(a, start, goals, trajectories=None, u_hs=None, c = "r", true_goal=0):
    """
        plots the start and goals and trajectory if provided
        on a 2D canvas

        use to visualize the results of simulate
    """
    a.axis('off')
    center(a, 0.5, 0.5, 1.1, 1.1)
    a.set_aspect('equal', 'datalim')

    a.plot(start[0], start[1], 'co', alpha=1.0,
            markeredgewidth=0, markersize=14.0)
    for (i,goal) in enumerate(goals):
        alpha = 1.0
        if i != true_goal:
            alpha = alpha / 3.0
        a.plot(goal[0], goal[1], 'go', alpha=alpha,
            markeredgewidth=0, markersize=14.0)

    if trajectories is not None:
        for trajectory in trajectories:
            for q in trajectory:
                a.plot(q[0], q[1],
                        'o', alpha=1.0/len(trajectories),
                        markeredgewidth=0, markersize=7.0, color=c)

    if u_hs is not None and trajectories is not None:
        for u_h, t in zip(u_hs, trajectories):
            for i in range(len(u_h)):
                if not np.allclose(u_h[i], np.zeros(u_h[i].shape)):
                    a.arrow(t[i][0], t[i][1], u_h[i][0], u_h[i][1], fc="k", alpha=1.0/len(u_hs))


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

def compare_beliefs(a, belief_sets, goal=0, labels=None, colors=None, legend=True, multi=False, fontsize=20):
    print("warning setting global palatino font size")
    # TODO: fix
    palatino.set_size(fontsize)
    slick(a)
    a.set_ylabel("$b(\\theta = \\theta^{top})$", fontproperties=palatino, fontsize=fontsize)
    a.set_ylim([-0.04, 1.04])

    patches = []

    for i in range(len(belief_sets)):
        if labels is None:
            label = "Belief " + repr(i)
        else:
            label = labels[i]

        if colors is not None:
            c = colors[i]
        else:
            c = None

        if colors is not None and labels is not None:
            patches.append(mpatches.Patch(color=c, label=label))

        if multi:
            data = [b[:, goal] for b in belief_sets[i]]

            l = np.min([len(b) for b in belief_sets[i]])
            data_trunc = [d[:l] for d in data]

            a.errorbar(
                    range(np.max([len(b) for b in belief_sets[i]])),
                    duo.mean(data),
                    yerr=np.std(data_trunc)/np.sqrt(len(data)),
                    label=label, c=c)
        else:
            a.plot(belief_sets[i][:,goal], label=label, c=c, linewidth=2.0)
    if legend:
        if len(patches) > 0:
            a.legend(handles=patches, prop=palatino, loc=4,
                    markerfirst=False,
                    framealpha=0,
                    fontsize=fontsize)
        else:
            a.legend(prop=palatino, loc=4, markerfirst=False)
