from activity_py import Activity


def test_load_fit():
    with open("./tests/testfiles/Tuesday_Fartlek.fit", "rb") as f:
        a = Activity.load_fit(f)
        assert int(a.distance) == 8
        assert a.duration == 2400
        print(a.laps)


def test_load_gpx():
    with open("./tests/testfiles/Tuesday_Fartlek.gpx", "rb") as f:
        a = Activity.load_gpx(f)
        assert int(a.distance) == 8
        assert a.duration == 2400
