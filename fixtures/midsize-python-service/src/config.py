"""Configuration loading."""
import json
import os

DEFAULTS = {
    "queue_url": "amqp://localhost/ingest",
    "warehouse_dsn": "postgres://localhost/wh",
    "batch_size": 500,
    "retry_ceiling": 8,
}


def parse_config(path=None):
    cfg = dict(DEFAULTS)
    path = path or os.environ.get("INGEST_CONFIG")
    if path and os.path.exists(path):
        with open(path) as fh:
            cfg.update(json.load(fh))
    return cfg


def validate(cfg):
    if cfg["batch_size"] < 1:
        raise ValueError("batch_size must be positive")
    return cfg
