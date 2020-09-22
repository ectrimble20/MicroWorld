import logging
from pygame import Rect, Surface
from pygame_gui.elements import UIPanel, UILabel, UIButton, UIDropDownMenu, UITextEntryLine, UIImage, UIHorizontalSlider
from lib.base import GameScene
from lib.const import GUI_BUTTON_PRESSED, CHANGE_GAME_SCENE
from lib.eventbus import *
from lib.config import get_param
from lib.generate import gen_int_string
from lib.mapbuilder import generate_noise_grid, generate_height_grid


class GenerateRandomMap(GameScene):

    def __init__(self, game_ref):
        super().__init__(game_ref, 'generate_random_map')
        self.pv_img = None
        self.map_grid = None
        # colors for representing terrain types
        self._c_map = {
            0: (40, 53, 147), 1: (255, 204, 128), 2: (43, 175, 43), 3: (85, 139, 47), 4: (158, 157, 36),
            5: (141, 110, 99), 6: (66, 66, 66)
        }

    def on_enter(self):
        super().on_enter()
        bind_listener(self.on_button_click, GUI_BUTTON_PRESSED)

    def on_exit(self):
        super().on_exit()
        unbind_listener(self.on_button_click, GUI_BUTTON_PRESSED)

    def on_create(self):
        self.pv_img = Surface((256, 256)).convert()
        self.pv_img.fill((255, 255, 255))
        super().on_create()

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
        self.ui_elements['scene_label'] = UILabel(scene_label_rect, "Generate Random Map", self.gui,
                                                  self.ui_elements['panel'])
        # map size
        label_rect = Rect(0, 0, 150, get_param('element_height'))
        label_rect.y += scene_label_rect.bottom + get_param('element_padding')
        dd_rect = Rect(0, 0, 250, get_param('element_height'))
        dd_rect.y = label_rect.y
        label_rect.centerx = 125
        dd_rect.centerx = 325
        self.ui_elements['d_size_label'] = UILabel(label_rect, "Map Size", self.gui, self.ui_elements['panel'])
        self.ui_elements['dd_map_size'] = UIDropDownMenu(['64', '128', '256'], '64', dd_rect, self.gui,
                                                         self.ui_elements['panel'])
        # Seed
        label_rect.y += get_param('element_height') + get_param('element_padding')
        ip_rect = Rect(0, 0, 180, get_param('element_height'))
        ip_rect.centerx = (panel_rect.w // 2) + 30
        ip_rect.y = label_rect.y
        s_btn_rect = Rect(0, 0, 60, get_param('element_height'))
        s_btn_rect.x = ip_rect.right + get_param('element_padding')
        s_btn_rect.y = ip_rect.y
        self.ui_elements['seed_label'] = UILabel(label_rect, 'Map Seed', self.gui, self.ui_elements['panel'])
        self.ui_elements['input_seed'] = UITextEntryLine(ip_rect, self.gui, self.ui_elements['panel'])
        self.ui_elements['btn_rnd_seed'] = UIButton(s_btn_rect, 'Random', self.gui, self.ui_elements['panel'])
        # I want to add two sliders, 1 for mountains and 1 for water, these would be used to control the upper
        # and lower limits of the height mapping.
        h_sl_ops = (0, 100)
        h_sl_sel = 50
        label_rect.y += get_param('element_height') + get_param('element_padding')
        h_sl_rect = Rect(0, 0, 200, get_param('element_height'))
        h_sl_rect.centerx = (panel_rect.w // 2) + get_param('element_padding') + 30
        h_sl_rect.y = label_rect.y
        self.ui_elements['hsl_grass'] = UILabel(label_rect, 'Grass', self.gui, self.ui_elements['panel'])
        self.ui_elements['hs_grass'] = UIHorizontalSlider(h_sl_rect, h_sl_sel, h_sl_ops, self.gui,
                                                          self.ui_elements['panel'])

        label_rect.y += get_param('element_height') + get_param('element_padding')
        h_sl_rect.y = label_rect.y
        self.ui_elements['hsl_water'] = UILabel(label_rect, 'Water', self.gui, self.ui_elements['panel'])
        self.ui_elements['hs_water'] = UIHorizontalSlider(h_sl_rect, h_sl_sel, h_sl_ops, self.gui,
                                                          self.ui_elements['panel'])

        label_rect.y += get_param('element_height') + get_param('element_padding')
        h_sl_rect.y = label_rect.y
        self.ui_elements['hsl_mountain'] = UILabel(label_rect, 'Mountain', self.gui, self.ui_elements['panel'])
        self.ui_elements['hs_mountain'] = UIHorizontalSlider(h_sl_rect, h_sl_sel, h_sl_ops, self.gui,
                                                             self.ui_elements['panel'])

        # buttons
        button_rect = Rect(0, 0, 200, get_param('element_height'))
        button_rect.centerx = panel_rect.w // 2
        button_rect.y = label_rect.bottom + get_param('element_padding')
        self.ui_elements['btn_preview'] = UIButton(button_rect, "Generate Preview", self.gui, self.ui_elements['panel'])
        button_rect.w = 200
        button_rect.y += get_param('element_height') + get_param('element_padding')
        button_rect.centerx = (panel_rect.w // 2) - 100
        self.ui_elements['btn_back'] = UIButton(button_rect, "Back", self.gui, self.ui_elements['panel'])
        # the apply button always starts off disabled
        button_rect.centerx = (panel_rect.w // 2) + 100
        self.ui_elements['btn_next'] = UIButton(button_rect, "Next", self.gui, self.ui_elements['panel'])
        pv_rect = Rect(0, 0, 300, 300)
        pv_rect.centerx = panel_rect.w // 2
        pv_rect.y = button_rect.bottom + get_param('element_padding')
        self.ui_elements['pv_image'] = UIImage(pv_rect, self.pv_img, self.gui, self.ui_elements['panel'])

    def on_button_click(self, event):
        if event.type == GUI_BUTTON_PRESSED:
            if event.ui_element == self.ui_elements['btn_back']:
                post_event(CHANGE_GAME_SCENE, to_scene='map_select')
            elif event.ui_element == self.ui_elements['btn_rnd_seed']:
                self.ui_elements['input_seed'].set_text("")  # clear anything in there
                self.ui_elements['input_seed'].set_text(gen_int_string(10))
            elif event.ui_element == self.ui_elements['btn_preview']:
                self.generate_map_preview()

    def generate_map_preview(self):
        map_seed = self.ui_elements['input_seed'].get_text()
        # just sneaking in some random debug info here
        print(f"HS Grass Value: {self.ui_elements['hs_grass'].get_current_value()}")
        print(f"HS Water Value: {self.ui_elements['hs_water'].get_current_value()}")
        print(f"HS Mountain Value: {self.ui_elements['hs_mountain'].get_current_value()}")
        # convert to an int if we have a numeric string
        if type(map_seed) is not int and map_seed.isnumeric():
            map_seed = int(map_seed)
        map_size = self.ui_elements['dd_map_size'].selected_option
        # this should always be numeric, but lets be proper and check it
        if type(map_size) is not int and map_size.isnumeric():
            map_size = int(map_size)
        else:
            raise TypeError(f"Got a non-numeric map size: {map_size}")
        self.map_grid = generate_height_grid(generate_noise_grid(map_size, map_size, map_seed))
        self.pv_img.fill((255, 255, 255))
        # okay, should have a height grid now, let's make the image
        for y in range(self.map_grid.height):
            for x in range(self.map_grid.width):
                self.pv_img.set_at((x, y), self._c_map[self.map_grid[(x, y)]])
        # reload PV image element
        pv_rect = self.ui_elements['pv_image'].relative_rect
        self.ui_elements['pv_image'] = UIImage(pv_rect, self.pv_img, self.gui, self.ui_elements['panel'])
