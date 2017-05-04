import numpy as np
import matplotlib.pyplot as plt

norm = np.linalg.norm

# optimization by enumeration {{{

def argmin(options, cost):
    """
        cost should be a function of elements in options
    """
    return options[np.argmin([cost(op) for op in options])]

def sample_controls(alpha, n = 100):
    """
        sample n controls (equi-distant, angularly)
    """
    return [alpha*np.array([np.cos(a), np.sin(a)])
            for a in np.linspace(0, 2*np.pi, n)]

def entropy(beliefs):
    """
        the shannon entropy of a list of nums
    """
    if not np.isclose(sum(beliefs), 1):
        raise Exception("beliefs don't sum to 1!")

    return -sum([b*np.log(b) for b in beliefs])

# costs {{{

def expected_entropy(state, goals, beliefs, alpha):
    """
        generates a function that maps from a control
        to the expected entropy if that particular
        control were to be taken.

        use to compute H(b')
    """
    return lambda u: sum([
        b * entropy(
                update(state + u,
                       optimal(state + u, g, alpha),
                       goals, beliefs, alpha)
                )
        for (g, b) in zip(goals, beliefs)
    ])

def q_value(state, goal):
    return lambda u: norm(u) + norm(state + u - goal)

def expected_q_value(state, goals, beliefs):
    """
        expected q value to trade off between info gain

        cost here explicitly for the optimization by
        enumeration, use for that.
    """
    return lambda u: (sum([b*(norm(u) + norm(state + u - g))
                for (g, b) in zip(goals, beliefs)]))

# }}}

# }}}

# humans {{{

def optimal(state, goal, alpha):
    """
        optimal generates the optimal control given a
        particular goal.

        We can solve for this analytically, it is the
        vector in the direction of the goal, with norm
        alpha.

        use to get the control that an optimal agent
        acting with a particular goal would do.
    """
    return ((goal - state)/norm(goal - state))*alpha

def optimal_sampled(state, goal, alpha):
    return argmin(sample_controls(alpha, n = 1000), q_value(state, goal))

# }}}

# beliefs {{{

def update(state, u_h, goals, beliefs, alpha):
    """
        update performs a bayesian step update on
        beliefs given the observation: u_h.

        use to generate the belief update/what the belief
        update would be if you were in one state, saw u_h
        and had the passed in goals and beliefs.
    """
    beliefs = np.copy(beliefs)
    beliefs = [b*np.exp(
                    norm((state + optimal(state, g, alpha)) - g)
                    - norm((state + u_h) - g)
                )
                for (g, b) in zip(goals, beliefs)]

    # normalize!
    beliefs = beliefs/sum(beliefs)
    return beliefs

# }}}

# robots {{{

# This is the interface for the robot controllers, of which
# there are four:
#
#   - teleop (no inference + copy human)
#   - shared (inference + expected best control)
#   - info   (only care to collapse entropy)
#   - active (tradeoff between shared and info)
#
# def robot_control(state, u_h, goals, beliefs, alpha):
#   return (control, updated_beliefs)

def teleop(state, u_h, goals, beliefs, alpha):
    """
        teleop follows u_h exactly
    """

    return (u_h, beliefs)

def shared(state, u_h, goals, beliefs, alpha):
    """
        shared plans in expectation with respect
        to current beliefs.

        Note: we ASSUME analytical optimum is weighted
        sum of individual goal optima.
    """
    beliefs = update(state, u_h, goals, beliefs, alpha)

    u_R = np.array([0,0])
    for g, b in zip(goals, beliefs):
        u_R = u_R + b*optimal(state, g, alpha)

    return (u_R, beliefs)

def shared_sampled(state, u_h, goals, beliefs, alpha):
    """
        exactly shared, but instead of analytical, sampled
    """
    beliefs = update(state, u_h, goals, beliefs, alpha)

    u_R = argmin(
            sample_controls(alpha, n = 10000),
            expected_q_value(state, goals, beliefs),
          )

    return (u_R, beliefs)


def info(state, u_h, goals, beliefs, alpha):
    """
        info takes actions which minimize H(b')
    """
    beliefs = update(state, u_h, goals, beliefs, alpha)

    u_R = argmin(
            sample_controls(alpha),
            expected_entropy(state, goals, beliefs, alpha)
          )

    return (u_R, beliefs)

def active(lam):
    """
        active curries the true active function
        with the lam hyperparamter
    """
    def active(state, u_h, goals, beliefs, alpha):
        """
            active uses lam hyperparamter to trade off
            between shared shared autonomy expectation
            planning and entropy minimization
        """
        beliefs = update(state, u_h, goals, beliefs, alpha)

        ee = expected_entropy(state, goals, beliefs, alpha)
        def cost(u):
            return (sum([b*(norm(u) + norm(state + u - g))
                        for (g, b) in zip(goals, beliefs)])
                        + lam*ee(u))

        u_R = argmin(
                sample_controls(alpha),
                cost
              )

        return (u_R, beliefs)

    return active

# }}}

# Simulation {{{

# u_h: (x, theta) -> u
# u_r: (u_h, {theta_i}, b(theta)) -> u
def simulate(start, goals, true_goal, Fu_h, Fu_r, alpha=0.1, maxiters=100):
    current = np.copy(start)
    goal = goals[true_goal]
    beliefs = np.array([0.5 for g in goals])

    trajectory = [current]
    belief_hist = [beliefs]

    iters = 0
    while norm(current - goal) > alpha and iters < maxiters:
        u_h = Fu_h(current, goal, alpha)
        (u_r, beliefs) = Fu_r(current, u_h, goals, beliefs, alpha)

        if norm(u_r) > alpha:
            raise Exception("invalid u_r!")

        current = current + u_r
        trajectory.append(current)
        belief_hist.append(beliefs)
        iters += 1

    return trajectory, np.asarray(belief_hist)

# }}}

# Plotting {{{

def center(a, cx=0., cy=0., wx=2., wy=2.):
    a.set_xlim(cx-wx/2., cx+wx/2.)
    a.set_ylim(cy-wy/2., cy+wy/2.)

def visualize(start, goals, trajectory=None):
    f, a = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(7,7))
    center(a, 0.25, 0.25)
    plt.plot(start[0], start[1], 'bo')
    for goal in goals:
        plt.plot(goal[0], goal[1], 'go')

    if trajectory is not None:
        for q in trajectory:
            plt.plot(q[0], q[1], 'ro')

    return f

def plot_beliefs(beliefs):
    fig = plt.figure()
    for i in range(beliefs.shape[1]):
        plt.plot(beliefs[:,i], label="Goal " + repr(i))
    plt.legend()
    return fig

# }}}

# Results {{{

def generate_panel_for_anca(start, goals):
    (traj, bs) = simulate(start, goals, 0, optimal, teleop)
    f = visualize(start, goals, trajectory=traj)
    f.suptitle("Teleop")
    f.savefig("teleop_traj")

    (traj, bs) = simulate(start, goals, 0, optimal, shared)
    f = plot_beliefs(bs)
    f.suptitle("Shared Autonomy Beliefs")
    f.savefig("shared_beliefs")
    f = visualize(start, goals, trajectory=traj)
    f.suptitle("Shared Autonomy")
    f.savefig("shared_traj")

    for lam in [1,20,100]:
        (traj, bs) = simulate(start, goals, 0, optimal, active(lam))
        f = plot_beliefs(bs)
        f.suptitle("Active Beliefs Lambda = " + repr(lam))
        f.savefig("active_beliefs_lambda="+repr(lam))
        f = visualize(start, goals, trajectory=traj)
        f.suptitle("Active Traj Lambda = " + repr(lam))
        f.savefig("active_traj_lambda="+repr(lam))

# }}}

if __name__ == '__main__':
    goals = np.array([
        [1, 1],
        [1, 0],
    ])
    start = np.array([0, 0.5])

    (t, b) = simulate(start, goals, 0, optimal, shared)
    (t1, b1) = simulate(start, goals, 0, optimal, shared_sampled)

    visualize(start, goals, t)
    visualize(start, goals, t1)
    plt.show()

    print(t)
    print(t1)

