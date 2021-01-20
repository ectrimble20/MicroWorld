import pygame as pg
import logging
import gamescenes
from lib.config import get_param
from lib.eventbus import *
from lib.const import *
from startup import load_settings


class GameController(object):

    def __init__(self):
        logging.debug("Configuration loaded")
        self.display = pg.display.set_mode((get_param('display_width'), get_param('display_height')))
        logging.debug("Display initialized")
        self.scenes = {}  # dict of loaded scenes
        self.active_scene = ''
        self.change_scene_to = None  # if this is set, we need to change the scene
        self.running = False
        self.time_delta = 0.016
        self.clock = pg.time.Clock()
        logging.debug("GameController initialized")
        # initialize event handling
        bind_listener(self.quit_game, pg.QUIT)
        bind_listener(self.change_game_scene, EVENT_CHANGE_GAME_SCENE)

    @property
    def current_scene(self):
        return self.scenes[self.active_scene]

    def push_to_scene(self, scene, key, value):
        if scene in self.scenes.keys():
            self.scenes[scene].local_data[key] = value

    def run(self):
        self.load_scenes()
        self.running = True
        logging.debug("Game loop starting")
        while self.running:
            # handle the event queue processing
            process_event_queue()
            self.display.fill((0, 0, 0))
            self.current_scene.update()
            self.current_scene.render()
            self.time_delta = self.clock.tick(60) / 1000
            pg.display.flip()
            pg.display.set_caption(f"FPS<{int(self.clock.get_fps())}> - Scene: {self.active_scene}")
        self.unload_scenes()
        self.on_quit()
        logging.debug("Game loop has ended")

    def load_scenes(self):
        logging.debug("Loading Game Scenes")
        self.scenes['menu'] = gamescenes.MainMenu(self)
        self.scenes['map_select'] = gamescenes.MapSelect(self)
        self.scenes['select_existing_map'] = gamescenes.SelectExistingMap(self)
        self.scenes['generate_random_map'] = gamescenes.GenerateRandomMap(self)
        self.scenes['load'] = gamescenes.LoadSavedGame(self)
        self.scenes['settings'] = gamescenes.Settings(self)
        self.scenes['editor_menu'] = gamescenes.MapEditorMenu(self)
        self.scenes['editor_load'] = gamescenes.MapEditorLoadMap(self)
        # create all scenes
        for _, scene in self.scenes.items():
            scene.on_create()
        self.active_scene = 'menu'
        self.current_scene.on_enter()

    def reload_display(self):
        # nuke the old display
        self.display = None
        # reload settings
        load_settings()
        # re-initialize display
        self.display = pg.display.set_mode((get_param('display_width'), get_param('display_height')))
        # we need to rebuild all the scene GUI's
        for key, scene in self.scenes.items():
            scene.build_gui()
        # re-enter the current scene to reset the event system
        self.current_scene.on_enter()

    def unload_scenes(self):
        logging.debug("Unloading Game Scenes")
        for key, scene in self.scenes.items():
            scene.on_destroy()
        self.scenes.clear()

    def on_quit(self):
        unbind_listener(self.quit_game, pg.QUIT)
        unbind_listener(self.change_game_scene, EVENT_CHANGE_GAME_SCENE)

    def quit_game(self, e):
        if e.type == pg.QUIT:
            self.running = False

    def change_game_scene(self, e):
        if e.type == EVENT_CHANGE_GAME_SCENE:
            logging.debug(f"Changing scene from {self.active_scene} to {e.to_scene}")
            self.current_scene.on_exit()
            self.active_scene = e.to_scene
            self.change_scene_to = None
            self.current_scene.on_enter()
            logging.debug("Scene change completed")
