import numpy as np
import matplotlib.pyplot as plt

norm = np.linalg.norm

# humans {{{

def optimal(state, goal, alpha):
    return ((goal - state)/norm(goal - state))*alpha

# }}}

# beliefs {{{
def update(state, u_h, goals, beliefs, alpha):
    beliefs = np.copy(beliefs)
    beliefs = [b*np.exp(
                    norm((state + optimal(state, g, alpha)) - g)
                    - norm((state + u_h) - g)
                )
                for (g, b) in zip(goals, beliefs)]

    # normalize !
    beliefs = beliefs/sum(beliefs)
    return beliefs

# }}}

# robots {{{
#
# def robot_control(state, u_h, goals, beliefs):
#   return (control, updated_beliefs)

def teleop(state, u_h, goals, beliefs, alpha):
    return (u_h, beliefs)

def shared(state, u_h, goals, beliefs, alpha):
    beliefs = update(state, u_h, goals, beliefs, alpha)

    u_R = np.array([0,0])
    for g, b in zip(goals, beliefs):
        u_R = u_R + b*optimal(state, g, alpha)

    return u_R, beliefs

# optimization by enumeration {{{

def argmin(options, cost):
    return options[np.argmin([cost(op) for op in options])]

def sample_controls(alpha, n = 100):
    return [alpha*np.array([np.cos(a), np.sin(a)])
            for a in np.linspace(0, 2*np.pi, n)]

# costs {{{

def entropy(beliefs):
    return -sum([b*np.log(b) for b in beliefs])

def expected_entropy(state, goals, beliefs, alpha):
    cost = lambda u: sum([
        b * entropy(
                update(state + u,
                       optimal(state + u, g, alpha),
                       goals, beliefs, alpha)
                )
        for (g, b) in zip(goals, beliefs)])

    return cost

def expected_q_value(state, goals, beliefs):
    return (sum([b*(norm(u) + norm(state + u - g))
                for (g, b) in zip(goals, beliefs)]))

# }}}

# }}}

def info(state, u_h, goals, beliefs, alpha):
    beliefs = update(state, u_h, goals, beliefs, alpha)


    u_R = argmin(
            sample_controls(alpha),
            expected_entropy(state, goals, beliefs, alpha)
          )

    return (u_R, beliefs)

def active(lam):
    def active(state, u_h, goals, beliefs, alpha):
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

    (t, b) = simulate(start, goals, 0, optimal, info)
    visualize(start, goals, trajectory=t)
    plt.show()
