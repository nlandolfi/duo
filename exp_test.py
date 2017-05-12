import exp

def test_replace():
    cases = [
        {
            "start": {"robot": "$robot"},
            "vars": {"$robot": "active" },
            "end": {"robot": "active" },
        },
        {
            "start": {"robot": u'$robot'},
            "vars": {"$robot": u'active' },
            "end": {"robot": "active" },
        }
    ]

    for (i, case) in enumerate(cases):
        try:
            exp.replace(case["start"], case["vars"])
            if not case["start"] == case["end"]:
                raise Exception("got " + repr(case["start"]) + " want: " + repr(case["end"]))
        except Exception as e:
            print("exp_test.test_replace: case: " + repr(i) + ": " + repr(e))


if __name__ == "__main__":
    test_replace()
