"""
This module contains functionality for random generation of numbers, noise maps, and other functions that require
random (well, pseudo random) generation of data.
"""
import random


# static top-level RNG that always uses the same seed
_global_rng = random.Random()
_global_rng.seed('023242342340823492')

# dynamic RNG that uses random seeding
_rng = random.Random()


def set_seed(seed) -> None:
    """
    Set the seed that the random object uses.
    :param seed: Any
    :return: None
    """
    _rng.seed(seed)


def gen_int_string(length=10) -> str:
    """
    Generate a integer (numeric) string of N length
    :param length: int, length of the string to return
    :return: str
    """
    i = []
    for _ in range(length):
        i.append(_rng.randint(0, 9))
    return ''.join(map(str, i))


def gen_int_in_range(low: int, high: int) -> int:
    """
    Wrapper for randint function of the random module
    :param low: int
    :param high: int
    :return: int
    """
    return _rng.randint(low, high)


def random_chance(percent_of_occurring: int) -> bool:
    """
    Brute force, but fairly accurate random_chance method design to give a True/False answer N percent of the time when
    passed a given value.

    While this isn't 100% accurate, it does give a +/- 5% range of accuracy when tested over 100 iterations.
    :param percent_of_occurring: int
    :return: bool
    """
    # if the percent is >= 100%, always return true
    if percent_of_occurring >= 100:
        return True
    # likewise, if the percent is <= 0%, always return false
    if percent_of_occurring <= 0:
        return False
    return _rng.randint(0, 100) < percent_of_occurring
