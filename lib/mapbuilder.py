"""
Map Builder Module

Contains functions for building game maps.
"""
import logging
import random
import noise
from lib.structure import Grid


def map_height_value(value: float) -> int:
    """
    Takes a height value, returned from a noise function and maps it to a numeric key for the tile heights
    :param value: float
    :return: int
    """
    if value < 0.48:
        return 0    # water
    elif value < 0.49:
        return 1    # shore
    elif value < 0.5:
        return 2    # grass/lowlands
    elif value < 0.53:
        return 3    # midlands/plains
    elif value < 0.56:
        return 4    # highlands
    elif value < 0.58:
        return 5    # high hills
    else:
        return 6    # mountains


def get_noise(x: float, y: float, octs=8, per=1.0, lac=0.5, repeat_x=1024, repeat_y=1024) -> float:
    """
    Run a Perlin2D noise function for the given parameters

    Note.  This version does not pass a base (left default) and does not take a scale.  You should apply the scale to
    the X/Y values prior to calling this function.  All other noise parameters are accepted as arguments.
    :param x: float
    :param y: float
    :param octs: octaves
    :param per: persistence
    :param lac: lacunarity
    :param repeat_x: repeat on X axis
    :param repeat_y: repeat on Y axis
    :return: float
    """
    return noise.pnoise2(x, y, octaves=octs, persistence=per, lacunarity=lac, repeatx=repeat_x, repeaty=repeat_y, base=1)


def scale_noise(noise_value: float) -> float:
    """
    Scale noise values to be between 0.0 and 1.0

    The default return from Perlin noise is -1.0 to 1.0, this function is designed to take that value, shift it by 1.0
    and then divide it by 2 to give us a value between 0.0 and 1.0
    :param noise_value: float
    :return: float
    """
    return (noise_value + 1.0) * 0.5


def generate_noise_grid(width: int, height: int, seed=None) -> Grid:
    """
    Generates a Grid that contains a noise map generated either using a random seed or a given seed.  The seed controls
    the offset that is applied to the X/Y axis and the noise is scaled to be between 0.0 and 1.0 prior to being added
    to the grid.

    :param width: int, width of the map
    :param height: int, height of the map
    :param seed: Any, a seed used for the randomization
    :return: Grid
    """
    # setup seed for RNG
    rng = random.Random()
    if seed is not None:
        rng.seed(seed)
    # setup map seed, this is used as a randomizer for the X/Y offsets, it's basically an offset by the X/Y repeat value
    # but it can go negative, positive or anywhere in between
    map_seed = rng.randint(-1024, 1024)
    # log some stuff here
    logging.debug(f"Generating {width}x{height} map with seed {map_seed}")
    # build the grid to hold the values
    n_grid = Grid(width, height)
    # let's begin filling the grid
    # we'll go ahead and scale the noise as we generate it too so we return a grid with values 0.0 - 1.0
    for y in range(height):
        for x in range(width):
            n_x = (x + map_seed) * 0.2
            n_y = (y + map_seed) * 0.2
            n_grid[(x, y)] = scale_noise(get_noise(n_x, n_y))
    logging.debug(f"Map generated")
    return n_grid


def generate_height_grid(grid: Grid):
    logging.debug("Generating height grid from existing noise grid")
    height_grid = Grid(grid.width, grid.height)
    for y in range(grid.width):
        for x in range(grid.height):
            height_grid[(x, y)] = map_height_value(grid[(x, y)])
    logging.debug("Height grid generated")
    return height_grid
