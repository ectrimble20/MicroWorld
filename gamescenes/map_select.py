import logging
from pygame import Rect
from pygame_gui.elements import UIPanel, UILabel, UIButton, UIDropDownMenu
from lib.base import GameScene
from lib.const import GUI_BUTTON_PRESSED, EVENT_CHANGE_GAME_SCENE
from lib.eventbus import *
from lib.config import get_param


class MapSelect(GameScene):

    def __init__(self, game_ref):
        super().__init__(game_ref, 'map_select')

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
        self.ui_elements['scene_label'] = UILabel(scene_label_rect, "Start New Game", self.gui,
                                                  self.ui_elements['panel'])

        l_side_rect = Rect(0, 0, 150, get_param('element_height'))
        l_side_rect.centerx = 125
        l_side_rect.y = scene_label_rect.bottom + get_param('element_padding')
        self.ui_elements['l_dd_label'] = UILabel(l_side_rect, "Map Type", self.gui, self.ui_elements['panel'])
        dd_rect = Rect(0, 0, 250, get_param('element_height'))
        dd_rect.y = l_side_rect.y
        dd_rect.centerx = 325
        self.ui_elements['l_dd_game_map'] = UIDropDownMenu(['Existing', 'Random'], 'Existing', dd_rect, self.gui,
                                                           self.ui_elements['panel'])
        btn_rect = Rect(0, 0, 200, get_param('element_height'))
        btn_rect.centerx = (panel_rect.w) // 2 - 100
        btn_rect.y = dd_rect.bottom + get_param('element_padding')
        self.ui_elements['btn_back'] = UIButton(btn_rect, "Back", self.gui, self.ui_elements['panel'])
        btn_rect = Rect(0, 0, 200, get_param('element_height'))
        btn_rect.centerx = (panel_rect.w // 2) + 100
        btn_rect.y = dd_rect.bottom + get_param('element_padding')
        self.ui_elements['btn_next'] = UIButton(btn_rect, "Next", self.gui, self.ui_elements['panel'])

    def on_button_click(self, event):
        if event.type == GUI_BUTTON_PRESSED:
            if event.ui_element == self.ui_elements['btn_back']:
                post_event(EVENT_CHANGE_GAME_SCENE, to_scene='menu')
            elif event.ui_element == self.ui_elements['btn_next']:
                print(f"Next: >{self.ui_elements['l_dd_game_map'].selected_option}")
                if self.ui_elements['l_dd_game_map'].selected_option == 'Existing':
                    post_event(EVENT_CHANGE_GAME_SCENE, to_scene='select_existing_map')
                elif self.ui_elements['l_dd_game_map'].selected_option == 'Random':
                    post_event(EVENT_CHANGE_GAME_SCENE, to_scene='generate_random_map')
