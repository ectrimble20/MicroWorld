import logging
import pygame
from localpaths import LOG_FILE, SETTINGS_FILE
from lib.config import set_param
from lib.fileutil import read_from_json_file


__all__ = ['init_dependencies', 'load_settings']


def init_dependencies():
    """
    Initializes dependencies and populates various things we'll need in to get the program started.
    :return: None
    """
    # initialize logging
    log_level = logging.DEBUG
    logger = logging.getLogger()
    logger.setLevel(log_level)
    log_h = logging.FileHandler(LOG_FILE)
    log_h.setLevel(log_level)
    log_fmt = logging.Formatter(
        fmt='[%(asctime)s][%(levelname)s]:[%(module)s:%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    log_h.setFormatter(log_fmt)
    logger.addHandler(log_h)
    # initialize PyGame
    pygame.init()
    # populate configuration parameters
    load_settings()


def load_settings():
    settings_data = read_from_json_file(SETTINGS_FILE)
    if settings_data:
        set_param('display_width', settings_data['display']['width'])
        set_param('display_height', settings_data['display']['height'])
        set_param('display_full_screen', settings_data['full_screen'])
        if settings_data['full_screen']:
            set_param('display_full_screen_value', 'On')
        else:
            set_param('display_full_screen_value', 'Off')
        set_param('current_display_size', f"{settings_data['display']['width']}x{settings_data['display']['height']}")
    # we can now build our display sizes (system supported sizes
    # remove duplicates by converting to a set, then back to a list
    valid_display_sizes = list(set(pygame.display.list_modes()))
    # sort it
    valid_display_sizes.sort()
    valid_display_sizes_str = [f"{w}x{h}" for w, h in valid_display_sizes]
    set_param('display_sizes', valid_display_sizes_str)
    # setup some of our display parameters
    set_param('element_padding', 10)
    set_param('panel_padding', 20)
    set_param('element_height', 32)
