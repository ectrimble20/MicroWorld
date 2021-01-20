import logging
from pygame import Rect, QUIT
from pygame_gui.elements import UIPanel, UILabel, UIButton
from lib.base import GameScene
from lib.const import GUI_BUTTON_PRESSED
from lib.eventbus import *
from lib.const import EVENT_CHANGE_GAME_SCENE
from lib.config import get_param


class MainMenu(GameScene):

    def __init__(self, game_ref):
        super().__init__(game_ref, 'main_menu')

    def on_enter(self):
        super().on_enter()
        bind_listener(self.on_button_click, GUI_BUTTON_PRESSED)

    def on_exit(self):
        super().on_exit()
        unbind_listener(self.on_button_click, GUI_BUTTON_PRESSED)

    def build_gui(self):
        super().build_gui()
        panel_rect = Rect(0, 0, 500, self.display.get_rect().height - (get_param('panel_padding') * 2))
        panel_rect.centerx = self.display.get_rect().centerx
        panel_rect.y = get_param('panel_padding')
        self.ui_elements['panel'] = UIPanel(panel_rect, 1, self.gui)
        # all other elements are relative
        scene_label_rect = Rect(0, 0, 400, get_param('element_height'))
        scene_label_rect.y = get_param('element_padding')
        scene_label_rect.centerx = panel_rect.w // 2  # midpoint of the panel
        self.ui_elements['scene_label'] = UILabel(scene_label_rect, "Main Menu", self.gui, self.ui_elements['panel'])
        # buttons
        button_rect = Rect(0, 0, 400, get_param('element_height'))
        button_rect.y = scene_label_rect.bottom + get_param('element_padding')
        button_rect.centerx = panel_rect.w // 2
        self.ui_elements['btn_new'] = UIButton(button_rect, "New Game", self.gui, self.ui_elements['panel'])
        button_rect.y += get_param('element_height') + get_param('element_padding')
        self.ui_elements['btn_load'] = UIButton(button_rect, "Load Game", self.gui, self.ui_elements['panel'])
        button_rect.y += get_param('element_height') + get_param('element_padding')
        self.ui_elements['btn_editor'] = UIButton(button_rect, "Map Editor", self.gui, self.ui_elements['panel'])
        button_rect.y += get_param('element_height') + get_param('element_padding')
        self.ui_elements['btn_settings'] = UIButton(button_rect, "Settings", self.gui, self.ui_elements['panel'])
        button_rect.y += get_param('element_height') + get_param('element_padding')
        self.ui_elements['btn_quit'] = UIButton(button_rect, "Quit Game", self.gui, self.ui_elements['panel'])

    def on_button_click(self, event):
        if event.type == GUI_BUTTON_PRESSED:
            if event.ui_element == self.ui_elements['btn_quit']:
                post_event(QUIT)
            elif event.ui_element == self.ui_elements['btn_new']:
                post_event(EVENT_CHANGE_GAME_SCENE, to_scene='map_select')
            elif event.ui_element == self.ui_elements['btn_load']:
                post_event(EVENT_CHANGE_GAME_SCENE, to_scene='load')
            elif event.ui_element == self.ui_elements['btn_editor']:
                post_event(EVENT_CHANGE_GAME_SCENE, to_scene='editor_menu')
            elif event.ui_element == self.ui_elements['btn_settings']:
                post_event(EVENT_CHANGE_GAME_SCENE, to_scene='settings')

