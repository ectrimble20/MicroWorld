"""
Module used to generate a random map.

This isn't currently being used, working on making the generation code a bit more dynamic and flexible.
"""
import random
import noise
from lib.structure import Grid


# object oriented approach
class RandomMapGenerator(object):

    def __init__(self):
        self._def_height_map = {0: 0.48, 1: 0.49, 2: 0.5, 3: 0.55, 4: 0.57, 5: 0.6}
        self._cur_height_map = self._def_height_map.copy()

    def reset_height_map(self):
        self._cur_height_map = self._def_height_map.copy()

    def _convert_adjust_value(self, value):
        # clamp the value between 0 and 100
        value = max(0, min(100, value))
        if value < 20:
            return 0
        elif value < 40:
            return 1
        elif value < 60:
            return 2
        elif value < 80:
            return 3
        else:
            return 4

    def adjust_water(self, value: int, adjustments: dict):
        # skip case, if value is 2, we don't make any changes as that's the median level
        if value == 2:
            return None
        # {0: 0.48, 1: 0.49, 2: 0.5, 3: 0.55, 4: 0.57, 5: 0.6}
        if value == 0:      # Little to no water, water is replaced by grass, grass is dropped by a small amount
            pass
        elif value == 1:    # greatly reduced water
            pass
        elif value == 3:    # increased water
            pass
        elif value == 4:    # greatly increased water
            pass
        else:
            return None

    def apply_adjustments(self, water: int, grass: int, mountain: int):
        # this function receives a int value from 0 to 100, adjustments themselves are done to a 5 step scale ranging
        # from 0 to 4, therefore values are converted accordingly using 0=0-20, 1=21-40, 2=41-60 etc with 2 being the
        # baseline with which no change is made.
        adjustments = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0}
        water = self._convert_adjust_value(water)
        if water != 2:
            if water < 2:
                if water == 1:
                    pass
                else:
                    pass
            else:
                pass
        grass = self._convert_adjust_value(grass)
        if grass != 2:
            pass
        mountain = self._convert_adjust_value(mountain)
        if mountain != 2:
            pass
        pass


# the default height map, should not be directly adjusted
_def_height_map = {
    0: 0.48, 1: 0.49, 2: 0.5, 3: 0.55, 4: 0.57, 5: 0.6
}


def cleanup_map_shoreline(height_map: Grid):
    # First pass, we look for water tiles that have non-shore neighbors.  Any tile bordering water must be shore
    for y in range(height_map.height):
        for x in range(height_map.width):
            if height_map[(x, y)] == 0:
                for n_y in range(y-1, y+2):
                    for n_x in range(x-1, x+2):
                        try:
                            n_v = height_map[(n_x, n_y)]
                            if n_v != 0 and n_v != 1:
                                height_map[(n_x, n_y)] = 1
                        except IndexError:
                            pass
    # next we want to make sure any tiles bordering a shore tile are either water, shore or grass
    for y in range(height_map.height):
        for x in range(height_map.width):
            if height_map[(x, y)] == 1:
                for n_y in range(y-1, y+2):
                    for n_x in range(x-1, x+2):
                        try:
                            n_v = height_map[(n_x, n_y)]
                            if n_v != 0 and n_v != 1:
                                height_map[(n_x, n_y)] = 2
                        except IndexError:
                            pass
    # last, we want to make sure all shore tiles are within 4 tiles of a water tile
    for y in range(height_map.height):
        for x in range(height_map.width):
            # if tile is a shore tile, we want to make sure it's within 4 tiles of water, otherwise it needs to be
            # a grass tile
            if height_map[(x, y)] == 1:
                change_me = True
                for n_y in range(y-4, y+5):
                    for n_x in range(x-4, x+5):
                        try:
                            n_v = height_map[(n_x, n_y)]
                            if n_v == 0:
                                change_me = False
                        except IndexError:
                            pass
                        if not change_me:
                            continue
                    if not change_me:
                        continue
                if change_me:
                    height_map[(x, y)] = 2


def map_height_value(value: float, height_mapping: dict) -> int:
    r_value = 0
    for h_value, h_range in height_mapping.items():
        # if the value is less than the height range
        if value < h_range:
            # check the the current height value is less than the currently set value
            if h_value < r_value:
                # if so, assign it as the new value as we always choose the lowest value
                r_value = h_value
    return r_value


def generate_height_map(map_width: int, map_height: int, height_mapping: dict, gen_seed=None) -> Grid:
    if gen_seed is not None:
        random.seed(gen_seed)
    x_seed = random.randint(-1024, 1024)
    y_seed = random.randint(-1024, 1024)
    scale = 0.08
    world = Grid(map_width, map_height)
    for y in range(map_height):
        for x in range(map_width):
            val = noise.snoise2((x + x_seed) * scale, (y + y_seed) * scale, octaves=6, persistence=1.2, lacunarity=0.7,
                                base=1, repeaty=32, repeatx=32)
            val += 1.0
            val *= 0.5
            world[(x, y)] = map_height_value(val, height_mapping)
    cleanup_map_shoreline(world)
    return world
