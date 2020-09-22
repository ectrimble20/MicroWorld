from dataclasses import dataclass

# Types
# water, shore, grass, plains, hills, highlands and mountains.
TILE_WATER = 0
TILE_SHORE = 1
TILE_GRASS = 2
TILE_PLAINS = 3
TILE_HILLS = 4
TILE_HIGHLANDS = 5
TILE_MOUNTAINS = 6


# Movement Types
MOVE_BLOCKED = 0
MOVE_WATER = 1
MOVE_LAND = 2
MOVE_LAND_AND_WATER = 3


# Default properties
tile_def = {
    TILE_WATER: {
        'desc': 'water', 'move_type': MOVE_WATER, 'move_bonus': 2
    },
    TILE_SHORE: {
        'desc': 'shore', 'move_type': MOVE_LAND_AND_WATER, 'move_bonus': 2, 'can_build': True, 'build_bonus': -3
    },
    TILE_GRASS: {
        'desc': 'grass', 'move_type': MOVE_LAND, 'move_bonus': 4, 'can_build': True, 'build_bonus': 2, 'can_grow': True
    },
    TILE_PLAINS: {
        'desc': 'plains', 'move_type': MOVE_LAND, 'move_bonus': 6, 'can_build': True, 'build_bonus': 5, 'can_grow': True
    },
    TILE_HILLS: {
        'desc': 'hills', 'move_type': MOVE_LAND, 'move_bonus': -3, 'can_build': True, 'build_bonus': -2,
        'can_grow': True
    },
    TILE_HIGHLANDS: {
        'desc': 'highlands', 'move_type': MOVE_LAND, 'move_bonus': -4, 'can_build': True, 'build_bonus': -6,
        'can_grow': True
    },
    TILE_MOUNTAINS: {
        'desc': 'mountains', 'move_type': MOVE_BLOCKED, 'can_grow': True
    }
}


# Tile object
class Tile(object):
    """
    The tile object is the basic space unit of the world.  Each tile is 32x32 pixels in size (graphically) and are
    considered 1 unit of in-game distance.

    Tiles are constructed using a tile type ID, these is an int value that is used to construct the object with a set
    of default values defined in the tile_def dictionary.  These values can be over-written by passing keyword arguments
    to the constructor.  Example:

    tile_default = Tile(1, 10, 10)

    This will return a default populated tile of type 1, or SHORE.  To overwrite a value, for instance we want to change
    this particular shore to disable building, we can pass the keyword with a value to the constructor

    tile_modded = Tile(1, 10, 10, can_build=False)
    """

    def __init__(self, type_id, x, y, **kwargs):
        self._type_id = type_id
        self._x, self._y = x, y
        self.move_type = kwargs.get('move_type', tile_def[type_id].get('move_type', MOVE_LAND))
        self.move_bonus = kwargs.get('move_bonus', tile_def[type_id].get('move_bonus', 0))
        self.can_build = kwargs.get('can_build', tile_def[type_id].get('can_build', False))
        self.build_bonus = kwargs.get('build_bonus', tile_def[type_id].get('build_bonus', 0))
        self.road_level = kwargs.get('road_level', 0)
        self.river_level = kwargs.get('river_level', 0)
        self.can_grow = kwargs.get('can_grow', tile_def[type_id].get('can_grow', False))

    def get_type(self):
        return tile_def[self._type_id].get('desc', 'undefined')

    def get_type_id(self):
        return self._type_id

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class TileManager(object):

    def __init__(self):
        pass
