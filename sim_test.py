import traceback

import numpy as np
import matplotlib.pyplot as plt

import sim
import duo

def test_run():
    cases = [ "teleop", "shared", "active=1", "active=20", "active=100" ]
    for case in cases:
        ics  = sim.load("./.test_examples/" + case + ".json")
        want = np.load("./.test_examples/" + case + ".npy")

        try:
            got  = sim.run(ics)
        except Exception as e:
            print("sim_test.test_run: while running " + repr(case) + " got exception: " + repr(e))
            traceback.print_exc()
            break


        # f, (a1, a2) = plt.subplots(2)
        # duo.visualize(a1, got["conditions"]["start"], got["conditions"]["goals"], trajectories=[got["trajectory"]], u_hs=[got["u_h"]])
        # duo.visualize(a2, got["conditions"]["start"], got["conditions"]["goals"], trajectories=[want[0]], u_hs=[want[2]])
        # plt.show()
        got = (got["trajectory"], got["beliefs"], got["u_h"], got["u_r"])

        try:
            if not (len(want) == 4 and len(got) == 4):
                raise Exception("test_run expect len(got) = len(want) = 4")

            if (len(got[0]) != len(want[0])):
                raise Exception("trajectory lengths don't match: got: " +
                        repr(len(got[0])) + " want: " + repr(len(want[0])))

            if not np.allclose(want[0], got[0]):
                print(want[0])
                print(got[0])
                raise Exception("trajectory isn't matching")

            if not np.allclose(want[1], got[1]):
                raise Exception("belief isn't matching")

            if not np.allclose(want[2], got[2]):
                raise Exception("u_h isn't matching")

            if not np.allclose(want[3], got[3]):
                raise Exception("u_r isn't matching")
        except Exception as e:
            print("sim_test.test_run: while running " + repr(case) + ", " + repr(e))


if __name__ == '__main__':
    test_run()
