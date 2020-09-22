from os import path


__all__ = ['ROOT_DIR', 'RES_DIR', 'THEME_DIR', 'SETTINGS_FILE', 'LOG_FILE', 'SAVE_DIR', 'MAPS_DIR', 'IMG_DIR',
           'GUI_THEME_FILE', 'MASTER_MAP_FILE', 'SYSTEM_INFO_FILE']


# build root path from our files path, as this file should always be in the root directory
ROOT_DIR = path.dirname(__file__)
RES_DIR = path.join(ROOT_DIR, 'assets')
THEME_DIR = path.join(RES_DIR, 'themes')
SETTINGS_FILE = path.join(RES_DIR, 'settings.json')
LOG_FILE = path.join(RES_DIR, 'game.log')
SAVE_DIR = path.join(RES_DIR, 'saves')
MAPS_DIR = path.join(RES_DIR, 'maps')
IMG_DIR = path.join(RES_DIR, 'images')
GUI_THEME_FILE = path.join(THEME_DIR, 'default.json')
MASTER_MAP_FILE = path.join(MAPS_DIR, 'master.json')
SYSTEM_INFO_FILE = path.join(RES_DIR, 'system.json')
