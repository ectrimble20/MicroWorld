"""
Module used to generate a random map.
"""
import random
import noise
from lib.structure import Grid


adjustment_table = {
    'water': {
        0: {0: -0.25, 1: -0.24},
        1: {0: -0.15, 1: -0.14},
        2: {},
        3: {0: 0.05, 1: 0.06, 2: 0.02, 3: 0.01},
        4: {0: 0.1, 1: 0.11, 2: 0.05, 3: 0.08}
    },
    'grass': {
        0: {},
        1: {},
        2: {},
        3: {},
        4: {}
    },
    'mountain': {
        0: {},
        1: {},
        2: {},
        3: {},
        4: {}
    },
}


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

# the current height map
_cur_height_map = _def_height_map.copy()

# used to calculate the level of adjustment to make to the height map prior to generation
_adjust_map = {
    0.0: 0, 25.0: 1, 50.0: 2, 75.0: 3, 100.0: 4
}


def reset_current_height_map():
    global _cur_height_map
    _cur_height_map = _def_height_map.copy()


def clamp_value_range(value: float) -> float:
    """
    Clamps the value range between 0.0 and 100.0
    :param value: float
    :return: float
    """
    return max(0.0, min(100.0, value))


def get_adjust_value(value: float) -> int:
    """
    Takes a value range and converts it to an adjustment value.  The adjustment value is passed into the adjustment
    functions which then take the int value and apply the 'level' of change to their height ranges to get the desired
    effect on the height map generation.
    :param value: float
    :return: int
    """
    value = clamp_value_range(value)
    r_value = 0
    for v_adj, new_v in _adjust_map.items():
        if value <= v_adj:
            r_value = new_v
    return r_value


# TODO
#
# For terrain level adjustments, I'm thinking rather then hard-setting values, we +/- amounts.  The issue with hard
# settings values is fairly obvious, if you adjust more than one, things get over-written.  So really, what we want to
# do is adjust the values by say +0.02, then we run some kind of normalizing function on the values in order to prevent
# heights from over-lapping each other, for instance height 3 = 0.55 and 4 = 0.54 as this would cause really weird
# terrain generation, effectively height 3 would disappear completely due to be over-written by height 4 since it's
# value is lower.
#
# Okay, just had an idea.  What if we made an editor option for this, like have 5 vertical sliders (if we can do that)
# where each one controls some height value.  Like slider 0 controls water, 1 grass, 2 plains, 3 mids, and 4 highs
# and we just adjust them based on a range?  I'll have to investigate that one a bit.
def set_water_level(value: float):
    """
    Takes a relative value (float[0.0 - 100.0]), adjusts it to a nominal value [0-4] and adjusts the height range for
    water, either increasing it (3 - 4), decreasing it (0 - 1) or doing nothing ( 2 ).
    Note, if set to 0, it's actually more like a 5-10% chance as it is decreased a lot.
    Adjusting water levels has the greatest effect on the over-all appearance of the map.  Adjusting the water level
    down will increase the area that grass, midlands and highlands fill by adjusting their ranges.  Adjusting the level
    upwards will have the opposite effect by pushing these values higher and causing less area to be filled by each.
    :param value: float
    :return: None
    """
    i_value = get_adjust_value(value)
    # bail early condition
    if i_value == 2:
        return None
    if i_value > 2:
        if i_value == 3:
            _cur_height_map[0] = 0.50
            _cur_height_map[1] = 0.51
            _cur_height_map[2] = 0.52
            _cur_height_map[3] = 0.57
            _cur_height_map[4] = 0.59
            _cur_height_map[5] = 0.61
        if i_value == 4:
            _cur_height_map[0] = 0.52
            _cur_height_map[1] = 0.53
            _cur_height_map[2] = 0.54
            _cur_height_map[3] = 0.58
            _cur_height_map[4] = 0.6
            _cur_height_map[5] = 0.63
    else:
        if i_value == 1:
            _cur_height_map[0] = 0.45
            _cur_height_map[1] = 0.46
            _cur_height_map[2] = 0.47
            _cur_height_map[3] = 0.54
            _cur_height_map[4] = 0.56
            _cur_height_map[5] = 0.59
        if i_value == 0:
            _cur_height_map[0] = 0.40
            _cur_height_map[1] = 0.41
            _cur_height_map[2] = 0.42
            _cur_height_map[3] = 0.52
            _cur_height_map[4] = 0.55
            _cur_height_map[5] = 0.59


def set_grass_level(value: float):
    """
    Takes a relative value (float[0.0 - 100.0]), adjusts it to a nominal value [0-4] and adjusts the height range for
    grass, either increasing it (3 - 4), decreasing it (0 - 1) or doing nothing ( 2 ).
    The grass value can't ever really be zero, it can be decreased a lot, but there's always a band between shore and
    midlands/plains.  The lower the value for this the smaller this range is, but it is never actually zero.  When grass
    is adjusted, midlands, highlands, and high hills are adjusted down to fill in the areas.  Likewise, if the grass is
    increased, midlands, highlands, and high hills are adjusted up to give grass more area to fill.
    :param value: float
    :return: None
    """
    i_value = get_adjust_value(value)
    # bail early condition
    if i_value == 2:
        return None
    if i_value > 2:
        if i_value == 3:
            _cur_height_map[3] = 0.56
            _cur_height_map[4] = 0.58
            _cur_height_map[5] = 0.61
        if i_value == 4:
            _cur_height_map[3] = 0.58
            _cur_height_map[4] = 0.6
            _cur_height_map[5] = 0.62
    else:
        if i_value == 1:
            _cur_height_map[3] = 0.53
            _cur_height_map[4] = 0.56
            _cur_height_map[5] = 0.59
        if i_value == 0:
            _cur_height_map[3] = 0.51
            _cur_height_map[4] = 0.54
            _cur_height_map[5] = 0.58


def set_mountain_level(value: float):
    """
    Takes a relative value (float[0.0 - 100.0]), adjusts it to a nominal value [0-4] and adjusts the height range for
    water, either increasing it (3 - 4), decreasing it (0 - 1) or doing nothing ( 2 ).
    Note, if set to 0, it's actually more like a 5-10% chance as it is decreased a lot.
    For mountain, this also adjusts high hills as it will change the rate of mountains, with high hills reflecting the
    change.
    Changes to mountains can effectively remove them from the map as changes to this value effectively expand the height
    range for grass, midlands, highlands, and high hills.  Expanding mountains has the opposite effect except on grass,
    which will remain in it's value area, though midlands will encroach some.
    :param value: float
    :return: None
    """
    i_value = get_adjust_value(value)
    # bail early condition
    if i_value == 2:
        return None
    if i_value > 2:
        pass
    else:
        pass


def map_height_value(value: float) -> int:
    r_value = 0
    for h_value, h_range in _cur_height_map.items():
        # if the value is less than the height range
        if value < h_range:
            # check the the current height value is less than the currently set value
            if h_value < r_value:
                # if so, assign it as the new value as we always choose the lowest value
                r_value = h_value
    return r_value


def generate_map(width, height, gen_seed=None):
    if gen_seed is not None:
        random.seed(gen_seed)
    x_seed = random.randint(-1024, 1024)
    y_seed = random.randint(-1024, 1024)
    scale = 0.08
    world = Grid(width, height)
    for y in range(height):
        for x in range(width):
            val = noise.snoise2((x + x_seed) * scale, (y + y_seed) * scale, octaves=6, persistence=1.2, lacunarity=0.7,
                                base=1, repeaty=32, repeatx=32)
            val += 1.0
            val *= 0.5
            world[(x, y)] = map_height_value(val)
    # clean_water_edges(world)
    # clean_shore_edges(world)
    # clean_shore_outliers(world)
