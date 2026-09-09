from src.config import parse_config, validate


def test_defaults():
    cfg = parse_config(None)
    assert cfg["batch_size"] == 500


def test_validate_rejects_zero():
    cfg = parse_config(None)
    cfg["batch_size"] = 0
    try:
        validate(cfg)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
