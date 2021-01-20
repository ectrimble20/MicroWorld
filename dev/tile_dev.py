"""
Dev file for tile stuff
"""
from dataclasses import dataclass
from typing import Union

# constants
TILE_WATER = 0
TILE_SHORE = 1
TILE_LOWLAND = 2
TILE_MIDLAND = 3
TILE_HIGHLAND = 4
TILE_HILLS = 5
TILE_MOUNTAINS = 6

# Move/Build Types
TYPE_NONE = 0  # blocked, no movement allowed
TYPE_LAND = 1
TYPE_WATER = 2
TYPE_MIXED = 3  # land and water

# Base static tile entity Types
TILE_ENTITY_TREE = 0
TILE_ENTITY_BUSH = 1
TILE_ENTITY_ROAD = 2
TILE_ENTITY_HOUSE = 3
TILE_ENTITY_STONE_ROCK = 4
TILE_ENTITY_COPPER_ROCK = 5
TILE_ENTITY_TIN_ROCK = 6
TILE_ENTITY_FISH_SCHOOL = 7
TILE_ENTITY_FIELD = 8


_tile_defaults = {
    TILE_WATER: {
        'desc': 'Water',
        'movement_type': TYPE_WATER,
        'movement_speed': 2,
        'build_type': TYPE_WATER,
        'build_speed': -3,
        'allow_road': False,
        'fertility': 0.2
    },
    TILE_SHORE: {
        'desc': 'Shore',
        'movement_type': TYPE_MIXED,
        'movement_speed': 1,
        'build_type': TYPE_MIXED,
        'build_speed': 0,
        'allow_road': False,
        'fertility': 0.2
    },
    TILE_LOWLAND: {
        'desc': 'Lowlands',
        'movement_type': TYPE_LAND,
        'movement_speed': 3,
        'build_type': TYPE_LAND,
        'build_speed': 2,
        'allow_road': True,
        'fertility': 0.4
    },
    TILE_MIDLAND: {
        'desc': 'Midlands',
        'movement_type': TYPE_LAND,
        'movement_speed': 2,
        'build_type': TYPE_LAND,
        'build_speed': 1,
        'allow_road': True,
        'fertility': 0.6
    },
    TILE_HIGHLAND: {
        'desc': 'Highlands',
        'movement_type': TYPE_LAND,
        'movement_speed': -1,
        'build_type': TYPE_LAND,
        'build_speed': -2,
        'allow_road': True,
        'fertility': 0.2
    },
    TILE_HILLS: {
        'desc': 'Hills',
        'movement_type': TYPE_LAND,
        'movement_speed': -5,
        'build_type': TYPE_LAND,
        'build_speed': -6,
        'allow_road': True,
        'fertility': -0.2
    },
    TILE_MOUNTAINS: {
        'desc': 'Mountains',
        'movement_type': TYPE_NONE,
        'movement_speed': 0,
        'build_type': TYPE_NONE,
        'build_speed': 0,
        'allow_road': False,
        'fertility': 0.0
    }
}


class TypedWorldEntity(object):
    """
    Represents any entity that exists in the world.
    """

    def __init__(self, x: Union[(float, int)], y: Union[(float, int)], type_id: int):
        self._x, self._y, self._type_id = x, y, type_id

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def type_id(self):
        return self._type_id


class Tile(TypedWorldEntity):

    def __init__(self, x: Union[(float, int)], y: Union[(float, int)], type_id: int, **kwargs):
        super().__init__(x, y, type_id)
        # make sure our X/Y are integer values, we can accept floats, but we need ints to interact with the grid
        self._x = int(self._x)
        self._y = int(self._y)
        if TILE_WATER > self.type_id > TILE_MOUNTAINS:
            raise ValueError(f"Type ID {self._type_id} is not a valid Tile Type ID")
        self.movement_type = _tile_defaults[self._type_id]['movement_type']
        self.movement_speed = _tile_defaults[self._type_id]['movement_speed']
        self.build_type = _tile_defaults[self._type_id]['build_type']
        self.build_speed = _tile_defaults[self._type_id]['build_speed']
        self.allow_road = _tile_defaults[self._type_id]['allow_road']
        self.fertility = _tile_defaults[self._type_id]['fertility']
        # over-write values from kwargs if they're set
        for k, v in kwargs:
            if hasattr(self, k):
                self.k = v
