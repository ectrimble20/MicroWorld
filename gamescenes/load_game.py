import logging
from pygame import Rect
from pygame_gui.elements import UIPanel, UILabel, UIButton, UISelectionList
from lib.base import GameScene
from lib.const import GUI_BUTTON_PRESSED
from lib.eventbus import *
from lib.const import EVENT_CHANGE_GAME_SCENE, GUI_SELECT_CHANGED, GUI_SELECT_DROPPED
from lib.config import get_param


class LoadSavedGame(GameScene):

    def __init__(self, game_ref):
        super().__init__(game_ref, 'load_game')

    def on_enter(self):
        super().on_enter()
        bind_listener(self.on_button_click, GUI_BUTTON_PRESSED)
        bind_listener(self.on_select_changed, GUI_SELECT_CHANGED, GUI_SELECT_DROPPED)

    def on_exit(self):
        super().on_exit()
        unbind_listener(self.on_button_click, GUI_BUTTON_PRESSED)
        unbind_listener(self.on_select_changed, GUI_SELECT_CHANGED, GUI_SELECT_DROPPED)

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
        self.ui_elements['scene_label'] = UILabel(scene_label_rect, "Load Saved Game", self.gui,
                                                  self.ui_elements['panel'])
        # buttons
        select_rect = Rect(0, 0, 400, get_param('element_height') * 3)
        select_rect.y = scene_label_rect.bottom + get_param('element_padding')
        select_rect.centerx = panel_rect.w // 2
        self.ui_elements['game_select'] = UISelectionList(select_rect, [f"Game {n}" for n in range(5)], self.gui,
                                                          container=self.ui_elements['panel'])
        button_rect = Rect(0, 0, 200, get_param('element_height'))
        button_rect.y = select_rect.bottom + get_param('element_padding')
        button_rect.centerx = (panel_rect.w // 2) - 100
        self.ui_elements['btn_load'] = UIButton(button_rect, "Load Save", self.gui, self.ui_elements['panel'])
        self.ui_elements['btn_load'].disable()
        button_rect.centerx = (panel_rect.w // 2 + 100)
        self.ui_elements['btn_delete'] = UIButton(button_rect, "Delete Save", self.gui, self.ui_elements['panel'])
        self.ui_elements['btn_delete'].disable()
        button_rect.w = 400
        button_rect.centerx = panel_rect.w // 2
        button_rect.y += get_param('element_height') + get_param('element_padding')
        self.ui_elements['btn_back'] = UIButton(button_rect, "Back", self.gui, self.ui_elements['panel'])

    def on_button_click(self, event):
        if event.type == GUI_BUTTON_PRESSED:
            if event.ui_element == self.ui_elements['btn_back']:
                post_event(EVENT_CHANGE_GAME_SCENE, to_scene='menu')
            elif event.ui_element == self.ui_elements['btn_delete']:
                if self.ui_elements['game_select'].get_single_selection() is not None:
                    # TODO we need to have some kind of "Are you sure?" option in here
                    pass
            elif event.ui_element == self.ui_elements['btn_load']:
                if self.ui_elements['game_select'].get_single_selection() is not None:
                    # TODO load the map and move to the editor
                    pass

    def on_select_changed(self, event):
        if event.type == GUI_SELECT_CHANGED:
            if self.ui_elements['game_select'].get_single_selection() is not None:
                self.ui_elements['btn_load'].enable()
                self.ui_elements['btn_delete'].enable()
            else:
                self.ui_elements['btn_load'].disable()
                self.ui_elements['btn_delete'].disable()
        elif event.type == GUI_SELECT_DROPPED:
            self.ui_elements['btn_load'].disable()
            self.ui_elements['btn_delete'].disable()
