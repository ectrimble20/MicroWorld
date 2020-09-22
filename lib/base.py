import logging
from pygame_gui import UIManager
from lib.eventbus import *
from localpaths import GUI_THEME_FILE


class GameScene(object):
    """
    Base GameScene object.

    Version 2.0.1

    This version adds a lot of build in functionality accessible via super calls.  The purpose of these changes over the
    bare bones approach of 1.X is to reduce the amount of boiler plate noise when setting up a scene.

    2.0.0
    - added in a UIManager setup to on_create as well as ui_element and local_data dicts for storage of data.
    - added in calls for on_create, on_destroy, render, and logic to handle GUI calls.

    2.0.1
    - added in scene step logging.
    - broke out GUI building from create, it is called by on_create but can also be called independently as well, this
    is to support scene reloading when settings change.
    - gui, ui_elements, and local_data removed as class properties and set as object properties.
    - added shared_data as a class variable to more easily allow things to be shared between scenes.
    """

    # public class variable for all scenes to pass data around
    shared_data = {}

    def __init__(self, game_ref, scene_name: str):
        logging.debug(f"Scene<{scene_name}> Initializing")
        self.game = game_ref
        self.scene_name = scene_name
        self.gui = None
        self.ui_elements = {}
        self.local_data = {}

    @property
    def display(self):
        return self.game.display

    @property
    def time_delta(self):
        return self.game.time_delta

    def on_create(self):
        logging.debug(f"Scene<{self.scene_name}> Is Being Created")
        self.build_gui()

    def on_destroy(self):
        logging.debug(f"Scene<{self.scene_name}> Is Being Destroyed")
        self.gui.clear_and_reset()
        self.gui = None
        self.ui_elements.clear()
        self.local_data.clear()

    def update(self):
        self.gui.update(self.time_delta)

    def render(self):
        self.gui.draw_ui(self.display)

    def on_enter(self):
        logging.debug(f"Scene<{self.scene_name}> Being Entered")
        if self.gui is not None:
            set_current_ui(self.gui)

    def on_exit(self):
        logging.debug(f"Scene<{self.scene_name}> Being Exited")
        if self.gui is not None:
            unset_current_ui()

    def build_gui(self):
        logging.debug(f"Scene<{self.scene_name}> Is Building GUI")
        if self.gui is not None:
            logging.debug(f"Scene<{self.scene_name}> UIManager is present, clearing current values for rebuild")
            self.gui = None
            self.ui_elements.clear()
            self.gui = UIManager(self.display.get_size(), GUI_THEME_FILE)
        else:
            logging.debug(f"Scene<{self.scene_name}> UIManager not present, creating new manager")
            self.gui = UIManager(self.display.get_size(), GUI_THEME_FILE)
