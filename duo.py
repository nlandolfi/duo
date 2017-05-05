import json

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

norm = np.linalg.norm

def angle_between(v1, v2):
    if norm(v1) == 0 or norm(v2) == 0:
        return np.pi
        #return 0.

    v1_u = v1 / norm(v1)
    v2_u = v2 / norm(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def gaussian(mu, var):
    return lambda x:  np.exp(-((x - mu)**2)/(2*var**2))/(np.sqrt(2 * np.pi) * var)

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

def sample_controls_in_ball(alpha, n = 100, m = 10):
    return np.array([
        control for a in np.linspace(alpha, 0, m) for control in sample_controls(a, n)
    ])

def entropy(beliefs):
    """
        the shannon entropy of a list of nums
    """
    if not np.isclose(sum(beliefs), 1):
        raise Exception("beliefs don't sum to 1!")

    return -sum([b*np.log(b) for b in beliefs])

# costs {{{

def expected_entropy(state, goals, beliefs, alpha, likelihood, human_model):
    """
        generates a function that maps from a control
        to the expected entropy if that particular
        control were to be taken.

        use to compute H(b')
    """
    return lambda u: sum([
        b * entropy(
                update(state + u,
                       human_model(state + u, g, u, alpha), u,
                       goals, beliefs, alpha, likelihood=likelihood)
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
    return lambda u: (sum([b*q_value(state, g)(u) for (g, b) in zip(goals, beliefs)]))

# }}}

# }}}

# humans {{{

def fuzz(u_h_function, variance=0.1):
    """
        fuzz adds gaussian noise to the u_h returned by the u_h_function
    """
    return lambda state, goal, alpha: np.random.normal(u_h_function(state, goal, alpha), variance)

def forget_u_r(u_h_function):
    return lambda state, goal, _past_u_r, alpha: u_h_function(state, goal, alpha)

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

def is_almost_optimal(past_u_r, state, goal, alpha, threshold=np.pi/4):
    """
        was the robot's action almost optimal according to the goal
    """
    return np.abs(angle_between(past_u_r, optimal(state - past_u_r, goal, alpha))) < threshold

def pull_back(past_u_r, state, goal, alpha):
    """
        given that the robot's action was not almost optimal,
        how should the human react?
    """
    center = - past_u_r + optimal(state - past_u_r, goal, alpha)
    return alpha*center/norm(center)

def lazy(threshold):
    def lazy(state, goal, past_u_r, alpha):
        if is_almost_optimal(past_u_r, state, goal, alpha, threshold=threshold):
            return np.zeros(past_u_r.shape)
        else:
            return pull_back(past_u_r, state, goal, alpha)
    return lazy

# }}}

# beliefs {{{

def boltzmann(beta=1.0):
    def likelihood(state, u_h, past_u_r, goal, alpha):
        return np.exp(beta*
                        (norm((state + optimal(state, goal, alpha)) - goal)
                        - norm((state + u_h) - goal))
                    )
    return likelihood

def lazylike(threshold):
    def lazylike(state, u_h, past_u_r, goal, alpha):
        if is_almost_optimal(past_u_r, state, goal, alpha, threshold=threshold):
            if np.alltrue(np.allclose(u_h, np.zeros(u_h.shape))):
                return 1.0 - 1e-10
            else:
                return 0.0 + 1e-10
        else:
            return gaussian(0, np.pi/4)(
                    angle_between(pull_back(past_u_r, state, goal, alpha), u_h)
            )
    return lazylike

def update(state, u_h, past_u_r, goals, beliefs, alpha, likelihood=boltzmann(1.0)):
    """
        update performs a bayesian step update on
        beliefs given the observation: u_h.

        use to generate the belief update/what the belief
        update would be if you were in one state, saw u_h
        and had the passed in goals and beliefs.
    """
    beliefs = np.copy(beliefs)
    beliefs = [b*likelihood(state, u_h, past_u_r, g, alpha)
                for (g, b) in zip(goals, beliefs)]

    # normalize!
    beliefs = beliefs/np.sum(beliefs)
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

def teleop(state, u_h, past_u_r, goals, beliefs, alpha):
    """
        teleop follows u_h exactly
    """

    return (u_h, beliefs)

def shared_analytical(state, u_h, goals, beliefs, alpha):
    """
        shared plans in expectation with respect
        to current beliefs.

        Note: we ASSUME analytical optimum is weighted
        sum of individual goal optima. TODO(not true?)
    """
    updated_beliefs = update(state, u_h, goals, beliefs, alpha)

    u_R = np.array([0,0])
    for g, b in zip(goals, updated_beliefs):
        u_R = u_R + b*optimal(state, g, alpha)

    return (u_R, updated_beliefs)

def shared_sampled(likelihood, human_model):
    def shared_sampled(state, u_h, past_u_r, goals, beliefs, alpha):
        """
            exactly shared, but instead of analytical, sampled
        """
        updated_beliefs = update(state, u_h, past_u_r, goals, beliefs, alpha, likelihood=likelihood)

        u_R = argmin(
                sample_controls(alpha, n = 100),
                expected_q_value(state, goals, updated_beliefs),
              )

        return (u_R, updated_beliefs)
    return shared_sampled

def info(state, u_h, goals, beliefs, alpha):
    """
        info takes actions which minimize H(b')
    """
    updated_beliefs = update(state, u_h, goals, beliefs, alpha)

    u_R = argmin(
            sample_controls(alpha),
            expected_entropy(state, goals, updated_beliefs, alpha)
          )

    return (u_R, updated_beliefs)

def active(likelihood, human_model, lam):
    """
        active curries the true active function
        with the likelihood and lam hyperparamter
    """
    def active(state, u_h, past_u_r, goals, beliefs, alpha):
        """
            active uses lam hyperparamter to trade off
            between shared shared autonomy expectation
            planning and entropy minimization
        """
        updated_beliefs = update(state, u_h, past_u_r, goals, beliefs, alpha, likelihood=likelihood)

        ee = expected_entropy(state, goals, updated_beliefs, alpha, likelihood, human_model)
        def cost(u):
            return (sum([b*(norm(u) + norm(state + u - g))
                        for (g, b) in zip(goals, updated_beliefs)])
                        + lam*ee(u))

        u_R = argmin(
                sample_controls(alpha),
                cost
              )

        return (u_R, updated_beliefs)

    return active

# }}}

# simulation {{{

# marshaling {{{

def save(filename, declaration):
    with open(filename, 'w') as f:
        json.dump(declaration, f, indent=4)

def load(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# }}}

HUMAN_OPTIMAL = "optimal"
HUMAN_LAZY    = "lazy"

ROBOT_TELEOP = "teleop"
ROBOT_SHARED = "shared"
ROBOT_ACTIVE = "active"

def likelihood_for(l):
    if l == "boltzmann":
        return boltzmann()

    if l == "lazy":
        return lazylike

    raise Exception()

def human_for(h):
    if h == HUMAN_OPTIMAL:
        return forget_u_r(optimal)

    if h == HUMAN_LAZY:
        return lazy

    raise Exception()

def robot_for(r, h, likelihood, robot_params):
    if r == ROBOT_TELEOP:
        return teleop

    if r == ROBOT_SHARED:
        return shared_sampled(likelihood, human_for(h))

    if r == ROBOT_ACTIVE:
        if "lambda" not in robot_params:
            raise Exception()

        return active(likelihood, human_for(h), robot_params["lambda"])

    raise Exception()

def run(ics):
    if "start" not in ics:
        raise Exception("initial conditions must specify 'start'")
    start = np.asarray(ics["start"])

    if "goals" not in ics:
        raise Exception("initial conditions must specify 'goals'")
    goals = np.asarray(ics["goals"])

    if "true_goal" not in ics:
        raise Exception("initial conditions must specify 'true_goal'")
    true_goal = ics["true_goal"]

    if "prior" not in ics:
        raise Exception("initial conditions must specify 'prior'")
    prior = np.asarray(ics["prior"])

    if "human" not in ics:
        raise Exception("initial conditions must specify 'human'")
    human = human_for(ics["human"])

    if "likelihood" not in ics:
        raise Exception()
    likelihood = likelihood_for(ics["likelihood"])

    robot_params = {}
    if "robot_params" in ics:
        robot_params = ics["robot_params"]

    if "robot" not in ics:
        raise Exception("initial conditions must specify 'robot'")
    robot = robot_for(ics["robot"], ics["human"], likelihood, robot_params)

    return simulate(start, goals, true_goal, human, robot, prior=prior)


# u_h: (x, theta) -> u
# u_r: (u_h, {theta_i}, b(theta)) -> u
def simulate(start, goals, true_goal, Fu_h, Fu_r, prior=None, alpha=0.1, maxiters=100):
    """
        run a simulation

        start and goals, true goal is an index

        Fu_h is a function generating the human control
        Fu_r is a function generating the robot control

        alpha is maximum norm of step size
        maxiters terminates if goal isn't reached in num of steps

        returns the traj taken and the history of beliefs
    """
    current = np.copy(start)
    goal = goals[true_goal]

    if prior is None:
        beliefs = np.array([0.5 for g in goals])
    else:
        beliefs = prior

    trajectory = [current]
    belief_hist = [beliefs]
    u_hs = []
    u_rs = [np.array([0.0, 0.0])]

    iters = 0
    while norm(current - goal) > alpha and iters < maxiters:
        u_h = Fu_h(current, goal, u_rs[-1], alpha)
        u_hs.append(u_h)
        (u_r, beliefs) = Fu_r(current, u_h, u_rs[-1], goals, beliefs, alpha)
        u_rs.append(u_r)

        if norm(u_r) > alpha + 1e-5:
            raise Exception("invalid u_r!")

        current = current + u_r
        trajectory.append(current)
        belief_hist.append(beliefs)
        iters += 1

    return trajectory, np.asarray(belief_hist), np.asarray(u_hs), np.asarray(u_rs[1:])

# }}}

# plotting {{{

palatino = fm.FontProperties(fname="./.Palatino-Roman.ttf")

def center(a, cx=0., cy=0., wx=2., wy=2.):
    """ centers an axis object """
    a.set_xlim(cx-wx/2., cx+wx/2.)
    a.set_ylim(cy-wy/2., cy+wy/2.)

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

def slick(a):
    a.spines['right'].set_visible(False)
    a.spines['top'].set_visible(False)
    a.xaxis.set_ticks_position('bottom')
    a.yaxis.set_ticks_position('left')
    a.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')

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

def compare_beliefs(a, belief_sets, goal=0, labels=None):
    slick(a)
    a.set_ylim([0, 1.05])
    a.set_ylabel("belief")
    for i in range(len(belief_sets)):
        if labels is None:
            label = "Belief " + repr(i)
        else:
            label = labels[i]

        a.plot(belief_sets[i][:,goal], label=label)
    a.legend(prop=palatino)

# }}}

# results {{{

def anca(start, goals):
    """ some simple examples """
    teleop = {
        "start": start.tolist(),
        "goals": goals.tolist(),
        "true_goal": 0,
        "prior": np.array([0.5, 0.5]).tolist(),
        "likelihood": "boltzmann",
        "human": "optimal",
        "robot": "teleop",
    }
    (traj, bs, uhs, urs) = run(teleop)
    f, a = plt.subplots(1)
    visualize(a, start, goals, trajectories=[traj], u_hs=[uhs])
    f.suptitle("Teleop", fontproperties=palatino)
    f.savefig("teleop_traj")

    shared = {
        "start": start.tolist(),
        "goals": goals.tolist(),
        "true_goal": 0,
        "prior": np.array([0.5, 0.5]).tolist(),
        "likelihood": "boltzmann",
        "human": "optimal",
        "robot": "shared",
    }
    (traj, bs, uhs, urs) = run(shared)
    f, a = plt.subplots(1)
    plot_beliefs(a, bs)
    f.suptitle("Shared Autonomy Beliefs")
    f.savefig("shared_beliefs")
    f, a = plt.subplots(1)
    visualize(a, start, goals, trajectories=[traj], u_hs=[uhs])
    f.suptitle("Shared Autonomy")
    f.savefig("shared_traj")

    for lam in [1,20,100]:
        conf = {
            "start": start.tolist(),
            "goals": goals.tolist(),
            "true_goal": 0,
            "prior": np.array([0.5, 0.5]).tolist(),
            "likelihood": "boltzmann",
            "human": "optimal",
            "robot": "active",
            "robot_params": {
                "lambda": lam,
            },
        }
        (traj, bs, uhs, urs) = run(conf)
        f, a = plt.subplots(1)
        plot_beliefs(a, bs)
        f.suptitle("Active Beliefs Lambda = " + repr(lam))
        f.savefig("active_beliefs_lambda="+repr(lam))
        f, a = plt.subplots(1)
        visualize(a, start, goals, trajectories=[traj], u_hs=[uhs])
        f.suptitle("Active Traj Lambda = " + repr(lam))
        f.savefig("active_traj_lambda="+repr(lam))

# }}}

def mean(l):
    longest = np.argmax(np.array([len(m) for m in l]))
    length = len(l[longest])
    n = []
    for i in range(length):
        n.append(np.mean(np.array([m[i] for m in l if i < len(m)]), axis=0))
    return np.array(n)

if __name__ == '__main__':
    goals = np.array([
        [1, 1],
        [1, 0],
    ])
    start = np.array([0, .5])

    #anca(start, goals)
    #plt.show()

    for thre in [np.pi/2, np.pi/4, np.pi/8]:
        f, (a1, a2) = plt.subplots(1, 2, sharex=False, sharey=False, figsize = (9, 4))
        (t, b, uh, ur) = simulate(start, goals, 0, lazy(thre), shared_sampled(lazylike(thre), lazy(thre)), prior=np.array([0.2, 0.8]))
        print(uh)
        visualize(a1, start, goals, trajectories=[t], u_hs=[uh], c="k")
        (t, b1, uh, ur) = simulate(start, goals, 0, lazy(thre), active(lazylike(thre), lazy(thre), 100), prior=np.array([0.2, 0.8]))
        print(uh)
        visualize(a2, start, goals, trajectories=[t], u_hs=[uh], c="r")
        f, a = plt.subplots(1)
        compare_beliefs(a, [b, b1], labels=["shared", "active"])
        plt.show()
        break
    """


    shared_ts = []
    active_ts = []
    shared_bs = []
    active_bs = []
    for i in range(20):
        print("iter " + repr(i))
        (t1, b1) = simulate(start, goals, 0, fuzz(optimal), shared_sampled)
        (t2, b2) = simulate(start, goals, 0, fuzz(optimal), active(100))

        shared_ts.append(t1)
        active_ts.append(t2)
        shared_bs.append(b1)
        active_bs.append(b2)

    f, (a1, a2) = plt.subplots(1, 2, sharex=False, sharey=False, figsize = (9, 4))
    visualize(a1, start, goals, trajectories=shared_ts, c="k")
    a1.set_title("Shared")
    visualize(a2, start, goals, trajectories=active_ts, c="r")
    a2.set_title("Active")
    f.suptitle("fuzzed human")
    f.savefig("fuzzed-human")

    print([len(t) for t in shared_ts])
    print([len(t) for t in active_ts])

    f, a = plt.subplots(1)
    compare_beliefs(a, [mean(shared_bs), mean(active_bs)], labels=["shared", "active"])
    f.savefig("fuzzed-beliefs")
    """



