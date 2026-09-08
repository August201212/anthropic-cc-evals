from seat_limit import can_invite, invite_batch, seats_remaining


def test_remaining():
    assert seats_remaining(30, 5) == 25


def test_enterprise_unbounded():
    assert seats_remaining(None, 999) is None
    assert can_invite(None, 999, 50)


def test_cannot_overfill():
    assert not can_invite(30, 29, 2)


def test_batch_stops_at_cap():
    assert invite_batch(3, 1, ["a@x", "b@x", "c@x"]) == ["a@x", "b@x"]
