from lib.eventbus import register_new_event, ui_event_map
from pygame_gui import UI_BUTTON_PRESSED, UI_BUTTON_DOUBLE_CLICKED, UI_SELECTION_LIST_NEW_SELECTION, \
    UI_DROP_DOWN_MENU_CHANGED, UI_SELECTION_LIST_DROPPED_SELECTION, UI_HORIZONTAL_SLIDER_MOVED


__all__ = ['CHANGE_GAME_SCENE', 'GUI_BUTTON_PRESSED', 'GUI_BUTTON_DOUBLE_PRESSED', 'GUI_SELECT_CHANGED',
           'GUI_DROP_DOWN_CHANGED', 'ui_event_map', 'SET_SCENE_DATA', 'GUI_SELECT_DROPPED']


# Bug work around
# The first call to custom_event in the PyGame event module returns the same ID as USEREVENT.
_C_EVENT_FIX = register_new_event()

# custom event constants
CHANGE_GAME_SCENE = register_new_event()
SET_SCENE_DATA = register_new_event()
GUI_BUTTON_PRESSED = register_new_event()
GUI_BUTTON_DOUBLE_PRESSED = register_new_event()
GUI_SELECT_CHANGED = register_new_event()
GUI_SELECT_DROPPED = register_new_event()
GUI_DROP_DOWN_CHANGED = register_new_event()
GUI_H_SLIDER_CHANGED = register_new_event()

# push events to the event systems map for PyGameGUI events.
ui_event_map[UI_BUTTON_PRESSED] = GUI_BUTTON_PRESSED
ui_event_map[UI_BUTTON_DOUBLE_CLICKED] = GUI_BUTTON_DOUBLE_PRESSED
ui_event_map[UI_SELECTION_LIST_NEW_SELECTION] = GUI_SELECT_CHANGED
ui_event_map[UI_SELECTION_LIST_DROPPED_SELECTION] = GUI_SELECT_DROPPED
ui_event_map[UI_DROP_DOWN_MENU_CHANGED] = GUI_DROP_DOWN_CHANGED
ui_event_map[UI_HORIZONTAL_SLIDER_MOVED] = GUI_H_SLIDER_CHANGED
