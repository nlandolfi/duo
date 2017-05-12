import json

import numpy as np

import geo
import human
import robot
import belief

HUMAN_OPTIMAL = "optimal"
HUMAN_LAZY    = "lazy"

ROBOT_TELEOP = "teleop"
ROBOT_SHARED = "shared"
ROBOT_INFO   = "info"
ROBOT_ACTIVE = "active"

LIKELIHOOD_BOLTZMANN = "boltzmann"
LIKELIHOOD_LAZY      = "lazy"

def likelihood_for(l, params):
    """
        likelihood_for constructs a likelihood function
        for a particular model

        use to get a function corresponding to a particular
        declared likelihood

        >>> likelihood_for(LIKELIHOOD_BOLTZMANN, {'temperature': 1})
    """
    if l == LIKELIHOOD_BOLTZMANN:
        if "temperature" not in params:
            raise Exception("sim.likelihood_for: " + repr(LIKELIHOOD_BOLTZMANN) + ": 'temperature' not in params")

        return belief.boltzmann(params["temperature"])

    if l == LIKELIHOOD_LAZY:
        if "threshold" not in params:
            raise Exception("sim.likelihood_for: " + repr(LIKELIHOOD_LAZY) + ": threshold' not in params")

        return belief.lazy(params["threshold"])

    raise Exception("sim.likelihood_for: likelihood model " + repr(l) + " not recognized")

def human_for(h, params):
    """
        human_for constructs a human function for a particular model

        use to get a function corresponding to a particular human

        >>> import numpy as np
        >>> human_for(HUMAN_LAZY, {'threshold': np.pi/4})
    """

    if h == HUMAN_OPTIMAL:
        return human.optimal

    if h == HUMAN_LAZY:
        if "threshold" not in params:
            raise Exception("sim.human_for: " + repr(HUMAN_LAZY) + ": 'threshold' not in params")

        return human.lazy(params["threshold"])

    raise Exception("sim.human_for: human model " + repr(h) + " not recognized")

def robot_for(r, h, likelihood, robot_params, human_params):
    """
        robot_for constructs a robot function for a particular model

        use to get a function corresponding to a particular robot

        >>> import numpy as np
        >>> human_for(HUMAN_LAZY, {'threshold': np.pi/4})
    """
    if r == ROBOT_TELEOP:
        return robot.teleop

    if r == ROBOT_SHARED:
        return robot.shared_sampled(likelihood, human_for(h, human_params))

    if r == ROBOT_INFO:
        return robot.info(likelihood, human_for(h, human_params))

    if r == ROBOT_ACTIVE:
        if "lambda" not in robot_params:
            raise Exception("sim.robot_for: " + repr(ROBOT_ACTIVE) + ": 'lambda' not in params")

        return robot.active(likelihood, human_for(h, human_params), robot_params["lambda"])

    raise Exception("sim.robot_for: robot model " + repr(r) + " not recognized")

def save(filename, dictionary):
    with open(filename, 'w') as f:
        json.dump(dictionary, f, indent=4)

def load(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def run(ics):
    if "start" not in ics:
        raise Exception("sim.run: initial conditions must specify 'start'")
    start = np.asarray(ics["start"])

    if "goals" not in ics:
        raise Exception("sim.run: initial conditions must specify 'goals'")
    goals = np.asarray(ics["goals"])

    if "true_goal" not in ics:
        raise Exception("sim.run: initial conditions must specify 'true_goal'")
    true_goal = ics["true_goal"]

    if "prior" not in ics:
        raise Exception("sim.run: initial conditions must specify 'prior'")
    prior = np.asarray(ics["prior"])

    if "human" not in ics:
        raise Exception("sim.run: initial conditions must specify 'human'")
    human_params = {}
    if "human_params" in ics:
        human_params = ics["human_params"]
    human = human_for(ics["human"], human_params)

    if "likelihood" not in ics:
        raise Exception("sim.run: initial conditions must specify 'likelihood'")
    likelihood_params = {}
    if "likelihood_params" in ics:
        likelihood_params = ics["likelihood_params"]
    likelihood = likelihood_for(ics["likelihood"], likelihood_params)

    if "robot" not in ics:
        raise Exception("initial conditions must specify 'robot'")
    robot_params = {}
    if "robot_params" in ics:
        robot_params = ics["robot_params"]
    robot = robot_for(ics["robot"], ics["human"], likelihood, robot_params, human_params)

    (traj, bs, u_h, u_r) = simulate(start, goals, true_goal, human, robot, prior)
    return result(ics, traj, bs, u_h, u_r)

def result(ics, traj, beliefs, u_h, u_r):
    return {
        "conditions": ics,
        "trajectory": traj,
        "beliefs": beliefs,
        "u_h": u_h,
        "u_r": u_r,
    }

def simulate(start, goals, true_goal, Fu_h, Fu_r, prior, alpha=0.1, maxiters=100):
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
    beliefs = prior
    trajectory = [current]
    belief_hist = [beliefs]
    u_hs = []
    u_rs = [np.array([0.0, 0.0])]

    iters = 0
    while geo.norm(current - goal) > alpha and iters < maxiters:
        u_h = Fu_h(alpha, current, goal, u_rs[-1])
        u_hs.append(u_h)
        (u_r, beliefs) = Fu_r(alpha, current, goals, beliefs, u_rs[-1], u_h)
        u_rs.append(u_r)
        belief_hist.append(beliefs)

        if geo.norm(u_r) > alpha + 1e-5:
            raise Exception("sim.simulate: invalid u_r! u_r = " + repr(u_r) + "with norm = " + repr(geo.norm(u_r)))

        current = current + u_r
        trajectory.append(current)
        iters += 1

    return (trajectory, np.asarray(belief_hist), np.asarray(u_hs), np.asarray(u_rs[1:]))
