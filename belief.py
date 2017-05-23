import numpy as np

import geo
import human

def gaussian(mu, var):
    return lambda x:  np.exp(-((x - mu)**2)/(2*var**2))/(np.sqrt(2 * np.pi) * var)

def entropy(beliefs):
    """
        the shannon entropy of a list of nums
    """
    if not np.isclose(sum(beliefs), 1):
        raise Exception("entropy: beliefs don't sum to 1!")

    return -sum([b*np.log(b) for b in beliefs])

# A likelihood is:
#
#  P(goal | u_r, u_h, state)
#
# Example:
#   >>> beta = 1.0
#   >>> alpha = 0.5
#   >>> l = boltzmann(beta)
#   ...
#   >>> p_u_h_given = l(alpha, state, u_h, u_r, goal)

def boltzmann(beta):
    """
        boltzmann is the boltzmann distribution observation
        model, where the human acts approximately optimal
        according to a cost function, here given by
        distance to go to goal.
    """
    def likelihood(alpha, state, u_h, past_u_r, goal):
        return np.exp(beta*
                        (geo.norm((state + human.optimal(alpha, state, goal)) - goal)
                        - geo.norm((state + u_h) - goal))
                    )
    return likelihood

def lazy(threshold):
    """
        lazy is an observation model based on the expectation
        that the human will not offer corrective controls if the
        robot is acting correctly, and will offer overly corrective
        controls if the robot is acting incorrectly.
    """
    def lazylike(alpha, state, u_h, past_u_r, goal):
        if human.looks_almost_optimal(alpha, state, goal, past_u_r, threshold):
            if np.alltrue(np.allclose(u_h, np.zeros(u_h.shape))):
                return 1.0 - 1e-10
            else:
                return 0.0 + 1e-10
        else:
            return gaussian(0, np.pi/4)(
                    geo.angle_between(human.pull_back(alpha, state, goal, past_u_r), u_h)
            )
    return lazylike

def update(alpha, state, u_h, past_u_r, goals, beliefs, likelihood):
    """
        update performs a bayesian step update on
        beliefs given the observation: u_h.

        use to generate the belief update/what the belief
        update would be if you were in one state, saw u_h
        and had the passed in goals and beliefs.
    """
    beliefs = np.copy(beliefs)
    beliefs = [b*likelihood(alpha, state, u_h, past_u_r, g)
                for (g, b) in zip(goals, beliefs)]

    # normalize!
    beliefs = beliefs/np.sum(beliefs)
    return beliefs
