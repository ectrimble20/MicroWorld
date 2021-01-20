from lib.eventbus import register_new_event, ui_event_map
from pygame_gui import UI_BUTTON_PRESSED, UI_BUTTON_DOUBLE_CLICKED, UI_SELECTION_LIST_NEW_SELECTION, \
    UI_DROP_DOWN_MENU_CHANGED, UI_SELECTION_LIST_DROPPED_SELECTION, UI_HORIZONTAL_SLIDER_MOVED


# Bug work around
# The first call to custom_event in the PyGame event module returns the same ID as USEREVENT.
# Note: this has been fixed in PyGame 2.0.12dev, but I'm leaving this in for a while.
_C_EVENT_FIX = register_new_event()

# custom event constants
EVENT_CHANGE_GAME_SCENE = register_new_event()
SET_SCENE_DATA = register_new_event()       # this is going to go away soon
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

# tile type constants
TILE_WATER = 0
TILE_SHORE = 1
TILE_LOWLAND = 2
TILE_MIDLAND = 3
TILE_HIGHLAND = 4
TILE_HILLS = 5
TILE_MOUNTAINS = 6

# movement type constants
MOVE_TYPE_NONE = 0  # blocked, no movement allowed
MOVE_TYPE_LAND = 1  # only movement on land tiles
MOVE_TYPE_WATER = 2  # only movement on water tiles
MOVE_TYPE_MIXED = 3  # movement on both land and water tiles

# entity types, this covers all types of entities
ENTITY_TREE = 0
ENTITY_BUSH = 1
ENTITY_ROAD = 2
ENTITY_HOUSE = 3
ENTITY_STONE_ROCK = 4
ENTITY_COPPER_ROCK = 5
ENTITY_TIN_ROCK = 6
ENTITY_FISH_SCHOOL = 7
ENTITY_FIELD = 8
ENTITY_MAN = 9
ENTITY_WOMAN = 10
ENTITY_CHILD_MALE = 11
ENTITY_CHILD_FEMALE = 12


__all__ = ['EVENT_CHANGE_GAME_SCENE',
           'GUI_BUTTON_PRESSED',
           'GUI_BUTTON_DOUBLE_PRESSED',
           'GUI_SELECT_CHANGED',
           'GUI_DROP_DOWN_CHANGED',
           'ui_event_map',
           'SET_SCENE_DATA',
           'GUI_SELECT_DROPPED',
           'TILE_WATER', 'TILE_HILLS', 'TILE_SHORE', 'TILE_MIDLAND', 'TILE_MOUNTAINS', 'TILE_HIGHLAND', 'TILE_LOWLAND',
           'MOVE_TYPE_LAND', 'MOVE_TYPE_NONE', 'MOVE_TYPE_WATER', 'MOVE_TYPE_MIXED',
           'ENTITY_MAN', 'ENTITY_BUSH', 'ENTITY_FIELD', 'ENTITY_HOUSE', 'ENTITY_ROAD', 'ENTITY_TREE', 'ENTITY_WOMAN',
           'ENTITY_TIN_ROCK', 'ENTITY_CHILD_MALE', 'ENTITY_CHILD_FEMALE', 'ENTITY_COPPER_ROCK', 'ENTITY_FISH_SCHOOL',
           'ENTITY_STONE_ROCK']
