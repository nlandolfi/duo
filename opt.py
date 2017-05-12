import numpy as np

import belief
import geo

def argmin(options, cost):
    """
        cost should be a function of elements in options
    """
    return options[np.argmin([cost(op) for op in options])]

def sample_controls(alpha, n):
    """
        sample n controls (equi-distant, angularly) on the
        surface of an alpha-ball ||u|| = alpha
    """
    return [alpha*np.array([np.cos(a), np.sin(a)])
            for a in np.linspace(0, 2*np.pi, n)]

def sample_controls_in_ball(alpha, n, m):
    """
        sample controls (equidistant, angularly and in
        magnitude in an alpha-ball ||u|| <= alpha

        n is the dimension splitting the angle
        m is the dimension splitting magnitude
    """
    return np.array([
        control for a in np.linspace(alpha, 0, m) for control in sample_controls(a, n)
    ])

# costs {{{

def expected_entropy(state, goals, beliefs, alpha, likelihood, human_model):
    """
        generates a function that maps from a control
        to the expected entropy if that particular
        control were to be taken.

        use to compute H(b')
    """
    return lambda u: sum([
        b * belief.entropy(
                belief.update(alpha, state + u,
                       human_model(alpha, state + u, g, u), u,
                       goals, beliefs, likelihood)
                )
        for (g, b) in zip(goals, beliefs)
    ])

def q_value(state, goal):
    return lambda u: geo.norm(u) + geo.norm(state + u - goal)

def expected_q_value(state, goals, beliefs):
    """
        expected q value to trade off between info gain

        cost here explicitly for the optimization by
        enumeration, use for that.
    """
    return lambda u: (sum([b*q_value(state, g)(u) for (g, b) in zip(goals, beliefs)]))

# }}}
