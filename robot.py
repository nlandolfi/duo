import numpy as np

import opt
import geo
import belief

# A robot is a function
#   R: (alpha, state, goals, beliefs, past_u_r, u_h) -> (action, new_beliefs)

# four main robot controllers:
#   1. teleop (no inference, copy human)
#   2. shared (inference, expecation planning)
#   3. info   (inference, entropy planning)
#   4. active (inference, expecation + lam*entropy planning)

def teleop(alpha, state, goals, beliefs, past_u_r, u_h):
    """
        teleop follows u_h exactly.
    """
    return (u_h, beliefs)

def shared_sampled(likelihood, human_model):
    def controller(alpha, state, goals, beliefs, past_u_r, u_h):
        """
            shared plans in expectation with respect
            to current beliefs.
        """
        new_beliefs = belief.update(alpha, state, u_h, past_u_r, goals, beliefs, likelihood)

        u_R = opt.argmin(
                opt.sample_controls(alpha, 100),
                opt.expected_q_value(state, goals, new_beliefs),
              )

        return (u_R, new_beliefs)

    return controller

def info(likelihood, human_model):
    """
        info takes actions which minimize H(b')
    """

    def controller(alpha, state, goals, beliefs, past_u_r, u_h):
        new_beliefs = belief.update(alpha, state, u_h, past_u_r, goals, beliefs, likelihood)

        u_R = opt.argmin(
                opt.sample_controls(alpha, 100),
                opt.expected_entropy(state, goals, new_beliefs, alpha)
              )

        return (u_R, new_beliefs)

    return controller

def active(likelihood, human_model, lam):
    """
        active curries the true active function
        with the likelihood and lam hyperparamter
    """
    def controller(alpha, state, goals, beliefs, past_u_r, u_h):
        """
            active uses lam hyperparamter to trade off
            between shared shared autonomy expectation
            planning and entropy minimization
        """
        new_beliefs = belief.update(alpha, state, u_h, past_u_r, goals, beliefs, likelihood)

        ee = opt.expected_entropy(state, goals, new_beliefs, alpha, likelihood, human_model)
        def cost(u):
            return (sum([b*(geo.norm(u) + geo.norm(state + u - g))
                        for (g, b) in zip(goals, new_beliefs)])
                        + lam*ee(u))

        u_R = opt.argmin(
                opt.sample_controls(alpha, 100),
                cost
              )

        return (u_R, new_beliefs)

    return controller
