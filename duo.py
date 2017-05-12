import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import sim

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

    for thre in [np.pi/4, np.pi/4, np.pi/8]:
        f, (a1, a2) = plt.subplots(1, 2, sharex=False, sharey=False, figsize = (9, 4))
        (t, b, uh, ur) = sim.simulate(start, goals, 0, lazy(thre), shared_sampled(lazylike(thre), lazy(thre)), prior=np.array([0.5, 0.5]))
        print(uh)
        visualize(a1, start, goals, trajectories=[t], u_hs=[uh], c="k")
        (t, b1, uh, ur) = sim.simulate(start, goals, 0, lazy(thre), active(lazylike(thre), lazy(thre), 100), prior=np.array([0.2, 0.8]))
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
