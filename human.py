import numpy as np

import geo
import opt

# A human is a function:
#   H: (alpha, state, goal, u_r) -> (action)

def optimal(alpha, state, goal, _u_r=None):
    """
        optimal generates the optimal control given a
        particular goal.

        We can solve for this analytically, it is the
        vector in the direction of the goal, with norm
        alpha.

        use to get the control that an optimal agent
        acting with a particular goal would do.
    """
    return ((goal - state)/geo.norm(goal - state))*alpha

def optimal_sampled(n):
    """
        the optimal action for the human, via sampling

        e.g.,
            num_samples = 1000
            h = forget_u_r(optimal_sampled(num_samples))
    """
    def control(alpha, state, goal, _u_r):
        return opt.argmin(sample_controls(alpha, n), opt.q_value(state, goal))

def pull_back(alpha, state, goal, u_r):
    """
        given that the robot's action was not almost optimal,
        how should the human react?
    """
    center = - u_r + optimal(alpha, state, goal)
    return alpha*center/geo.norm(center)

def looks_almost_optimal(alpha, state, goal, past_u_r, threshold):
    """
        was the robot's action almost optimal according to the goal
    """
    return np.abs(geo.angle_between(past_u_r, optimal(alpha, state - past_u_r, goal))) < threshold

def lazy(threshold):
    """
        lazy models a human that will react only if the robot
        is making mistakes
    """

    def lazy(alpha, state, goal, past_u_r):
        if looks_almost_optimal(alpha, state, goal, past_u_r, threshold):
            return np.zeros(past_u_r.shape)
        else:
            return pull_back(alpha, state, goal, past_u_r)

    return lazy

def fuzz(u_h_function, variance):
    """
        fuzz adds gaussian noise to the u_h returned by the u_h_function

        e.g., fuzz(optimal, 0.1)
    """
    return lambda alpha, state, goal, past_u_r: np.random.normal(u_h_function(alpha, state, goal, past_u_r), variance)
