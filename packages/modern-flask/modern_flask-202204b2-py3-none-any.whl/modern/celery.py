from celery import Celery
from flask import Flask


def modern_celery(app: Flask, *args, **kwargs) -> Celery:
    cfg = app.config.get_namespace("CELERY_")
    cfg.update(**kwargs)
    return Celery(*args, **cfg)
