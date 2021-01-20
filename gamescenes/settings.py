import logging
from pygame import Rect
from pygame_gui.elements import UIPanel, UILabel, UIButton, UIDropDownMenu
from localpaths import SETTINGS_FILE
from lib.base import GameScene
from lib.const import GUI_BUTTON_PRESSED, GUI_DROP_DOWN_CHANGED, EVENT_CHANGE_GAME_SCENE
from lib.eventbus import *
from lib.config import get_param
from lib.fileutil import write_json_to_file, read_from_json_file


class Settings(GameScene):

    def __init__(self, game_ref):
        super().__init__(game_ref, 'settings')
        self._check_screen_size = None
        self._check_full_screen = None

    def on_enter(self):
        super().on_enter()
        bind_listener(self.on_button_click, GUI_BUTTON_PRESSED)
        bind_listener(self.on_drop_down_change, GUI_DROP_DOWN_CHANGED)

    def on_exit(self):
        super().on_exit()
        unbind_listener(self.on_button_click, GUI_BUTTON_PRESSED)
        unbind_listener(self.on_drop_down_change, GUI_DROP_DOWN_CHANGED)

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
        self.ui_elements['scene_label'] = UILabel(scene_label_rect, "Settings", self.gui, self.ui_elements['panel'])
        # screen size
        label_rect = Rect(0, 0, 150, get_param('element_height'))
        label_rect.y += scene_label_rect.bottom + get_param('element_padding')
        dd_rect = Rect(0, 0, 250, get_param('element_height'))
        dd_rect.y = label_rect.y
        label_rect.centerx = 125
        dd_rect.centerx = 325
        self.ui_elements['d_size_label'] = UILabel(label_rect, "Display Size", self.gui, self.ui_elements['panel'])
        self.ui_elements['dd_d_size'] = UIDropDownMenu(get_param('display_sizes'), get_param('current_display_size'),
                                                       dd_rect, self.gui, self.ui_elements['panel'])
        # full screen
        label_rect.y += get_param('element_height') + get_param('element_padding')
        dd_rect.y = label_rect.y
        self.ui_elements['fs_label'] = UILabel(label_rect, "Full Screen", self.gui, self.ui_elements['panel'])
        self.ui_elements['dd_fs'] = UIDropDownMenu(["On", "Off"], get_param('display_full_screen_value'), dd_rect,
                                                   self.gui, self.ui_elements['panel'])
        # buttons
        button_rect = Rect(0, 0, 200, get_param('element_height'))
        button_rect.y = label_rect.bottom + get_param('element_padding')
        button_rect.centerx = (panel_rect.w // 2) - 100
        self.ui_elements['btn_back'] = UIButton(button_rect, "Back", self.gui, self.ui_elements['panel'])
        # the apply button always starts off disabled
        button_rect.centerx = (panel_rect.w // 2) + 100
        self.ui_elements['btn_apply'] = UIButton(button_rect, "Apply", self.gui, self.ui_elements['panel'])
        self.ui_elements['btn_apply'].disable()
        # re-assign values for our check parameters, this is to control the apply buttons state
        self._check_screen_size = get_param('current_display_size')
        self._check_full_screen = get_param('display_full_screen_value')

    def on_button_click(self, event):
        if event.type == GUI_BUTTON_PRESSED:
            if event.ui_element == self.ui_elements['btn_back']:
                post_event(EVENT_CHANGE_GAME_SCENE, to_scene='menu')
            elif event.ui_element == self.ui_elements['btn_apply']:
                self.save_settings()
                self.game.reload_display()

    def on_drop_down_change(self, event):
        if event.type == GUI_DROP_DOWN_CHANGED:
            # on any change, check the elements for value and enable or disable the apply button
            apply_on = False
            if self.ui_elements['dd_d_size'].selected_option != self._check_screen_size:
                apply_on = True
            if self.ui_elements['dd_fs'].selected_option != self._check_full_screen:
                apply_on = True
            if apply_on:
                self.ui_elements['btn_apply'].enable()
            else:
                self.ui_elements['btn_apply'].disable()

    def save_settings(self):
        settings_data = read_from_json_file(SETTINGS_FILE)
        # get the currently selected display string
        display_str = self.ui_elements['dd_d_size'].selected_option
        sel_width, sel_height = map(int, display_str.split("x"))
        full_screen_str = self.ui_elements['dd_fs'].selected_option
        if full_screen_str == 'On':
            sel_full_screen = True
        else:
            sel_full_screen = False
        settings_data['display']['width'] = sel_width
        settings_data['display']['height'] = sel_height
        settings_data['full_screen'] = sel_full_screen
        write_json_to_file(settings_data, SETTINGS_FILE)


