import numpy as np

import geo

def test_angle_between():
    cases = [
        {
            "in": (np.array([1, 0, 0]), np.array([1, 0, 0])),
            "out": 0.0,
        },
        {
            "in": (np.array([-1, 0, 0]), np.array([1, 0, 0])),
            "out": np.pi,
        },
        {
            "in": (np.array([1, 0]), np.array([0, 1])),
            "out": np.pi/2,
        },
    ]

    for case in cases:
        got = geo.angle_between(*case["in"])
        want = case["out"]

        if not (got == want):
            raise Exception("test_angle_between")

if __name__ == '__main__':
    test_angle_between()
