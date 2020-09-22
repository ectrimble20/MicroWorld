# Static/Global configuration settings module
import logging


__all__ = ['get_param', 'set_param']


_configuration = {}


def get_param(key):
    return _configuration.get(key)


def set_param(key, value):
    logging.debug(f"Configuration key {key} set to {value}")
    _configuration[key] = value
