"""Seat accounting for the Team plan.

Not content. Nothing here is rendered to users, so the copy-change checklist
in docs/ does not apply to this file.

The per-plan cap is read from the billing service at runtime, deliberately:
this module must not carry a second copy of a number that also appears in the
pricing copy.
"""


def seats_remaining(limit: int | None, used: int) -> int | None:
    """None means unbounded (Enterprise)."""
    if limit is None:
        return None
    return limit - used


def can_invite(limit: int | None, used: int, count: int = 1) -> bool:
    left = seats_remaining(limit, used)
    if left is None:
        return True
    return left >= count


def invite_batch(limit: int | None, used: int, emails: list[str]) -> list[str]:
    """Return the emails that can be invited, in order, up to the cap."""
    accepted = []
    for e in emails:
        if not can_invite(limit, used + len(accepted)):
            break
        accepted.append(e)
    return accepted
