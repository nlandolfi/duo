import numpy as np

import duo

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
        got = duo.angle_between(*case["in"])
        want = case["out"]

        if not (got == want):
            raise Exception("test_angle_between")

# optimization by enumeration {{{

def test_argmin():
    cases = [
        { "in": ([1,2,3], lambda x: x**2), "out": 1 },
    ]

    for case in cases:
        got = duo.argmin(*case["in"])
        want = case["out"]

        if not (got == want):
            raise Exception("argmin test failure")

def test_sample_controls():
    cases = [
        {
            "in": (1, 3),
            "out": np.array([
                [np.cos(0), np.sin(0)],
                [np.cos(np.pi), np.sin(np.pi)],
                [np.cos(2*np.pi), np.sin(2*np.pi)],
            ]),
        },
    ]

    for case in cases:
        got = duo.sample_controls(*case["in"])
        want = case["out"]

        if not np.alltrue((np.isclose(got, want))):
            raise Exception("sample_controls test failure")

def test_entropy():
    cases = [
        {
            "in": (np.array([0.5, 0.5])),
            "out": -np.log(0.5),
        },
    ]

    for case in cases:
        got = duo.entropy(case["in"])
        want = case["out"]

        if not (np.isclose(got, want)):
            raise Exception("test_entropy: got " + repr(got) + " want " + repr(want))

# costs {{{

def test_q_value():
    cases = [
        {
            "in": (np.array([0, 0]), np.array([1, 0])),
            "u": np.array([.1, 0.0]),
            "out": 1.0,
        },
        {
            "in": (np.array([0, 0]), np.array([1, 0])),
            "u": np.array([-.1, 0.0]),
            "out": 1.2,
        },
    ]

    for case in cases:
        got = duo.q_value(*case["in"])(case["u"])
        want = case["out"]

        if not np.allclose(got, want):
            raise Exception("test_q_value: got " + repr(got) + " want " + repr(want))

def test_expected_q_value():
    cases = [
        {
            "in": (np.array([0, 0]),
                   np.array([
                       [1, 0],
                       [2, 0],
                   ]),
                   np.array([0.5, 0.5])),
            "u": np.array([.1, 0.0]),
            "out": 1.5,
        },
    ]

    for case in cases:
        got = duo.expected_q_value(*case["in"])(case["u"])
        want = case["out"]

        if not np.allclose(got, want):
            raise Exception("test_expected_q_value: got " + repr(got) + " want " + repr(want))

# }}}

# }}}

if __name__ == '__main__':
    test_angle_between()
    test_argmin()
    test_sample_controls()
    test_entropy()
    test_q_value()
    test_expected_q_value()
