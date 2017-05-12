import numpy as np

import belief

def test_entropy():
    cases = [
        {
            "in": (np.array([0.5, 0.5])),
            "out": -np.log(0.5),
        },
    ]

    for case in cases:
        got = belief.entropy(case["in"])
        want = case["out"]

        if not (np.isclose(got, want)):
            raise Exception("test_entropy: got " + repr(got) + " want " + repr(want))

if __name__ == '__main__':
    test_entropy()

