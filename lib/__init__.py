def ordinal(n) -> str:
    """
    Convert a number to it's ordinal form (e.g 21 -> 21st, 22 -> 22nd)
    :param n: str|int
    :return: str
    """
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix


def is_iterable(test_iter) -> bool:
    """
    Tests if an object is iterable (can be iterated over)
    :param test_iter: any
    :return: bool
    """
    try:
        iter(test_iter)
    except TypeError:
        return False
    return True

