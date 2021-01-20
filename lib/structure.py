from pygame import Rect
from typing import Union, Any, Tuple


class Grid(object):
    """
    Grid - version 1.0

    Basic Grid class.  Essentially a wrapper for a 2D array.  Provides get/set functionality to allow you to treat the
    Grid class as an array.

    Attributes
    ----------
    _w : int
        private width value of the Grid
    _h : int
        private height value of the Grid
    _grid : List[List[Any]]
        private 2D array

    Properties
    ----------
    width : int
        returns the value of _w for the width
    height : int
        returns the value of _h for the height

    Methods:
    --------
    __len__
        supports len() call and returns the total length of the 2D array
    __getitem__(Tuple[int, int]) : Any
        returns the value at a given index
    __setitem__(Tuple[int, int], Union[None, Any]) : None
        sets the value at a given index
    __delitem__(Tuple[int, int]) : None
        removes the value at a given index, value is set to None
    """

    def __init__(self, width: int, height: int):
        self._w, self._h = width, height
        self._grid = [
            [
                None for _ in range(self._w)
            ] for _ in range(self._h)
        ]

    @property
    def width(self) -> int:
        return self._w

    @property
    def height(self) -> int:
        return self._h

    def __len__(self):
        return self._w * self._h

    def __getitem__(self, coord: Tuple[int, int]) -> Union[None, Any]:
        return self._grid[coord[1]][coord[0]]

    def __setitem__(self, coord: Tuple[int, int], value: Union[None, Any]):
        self._grid[coord[1]][coord[0]] = value

    def __delitem__(self, coord: Tuple[int, int]):
        self._grid[coord[1]][coord[0]] = None


class SafeGrid(Grid):
    """
    SafeGrid - version 1.0
    Subclass of Grid

    Safe version of the Grid class, performs a try/catch to prevent index errors but otherwise is identical in function
    to the Grid class.

    Attributes & Methods
    --------------------
    Inherited from Grid

    """

    def __getitem__(self, coord: Tuple[int, int]) -> Union[None, Any]:
        try:
            return self._grid[coord[1]][coord[0]]
        except IndexError:
            return None

    def __setitem__(self, coord: Tuple[int, int], value: Union[None, Any]):
        try:
            self._grid[coord[1]][coord[0]] = value
        except IndexError:
            return None

    def __delitem__(self, coord: Tuple[int, int]):
        try:
            del self._grid[coord[1]][coord[0]]
        except IndexError:
            return None


class RectGrid(Grid):
    """
    RectGrid - version 1.0
    Subclass of Grid

    Builds a Grid of Rect objects to cover an area.  Takes extra cell size parameters and constructs a Rect for each
    cell that represents the area of the cell.

    Attributes
    ----------
    _cw : int
        private width of each individual cell
    _ch : int
        private height of each individual cell

    Methods
    -------
    Note, inherits the same methods as the Grid class, however, set and del item methods are disabled and will throw
    NotImplemented errors.  This is to prevent deleting or overwriting of Rect data at a Cell.
    """

    def __init__(self, width: int, height: int, cell_width: int, cell_height: int):
        super().__init__(width, height)
        self._cw, self._ch = cell_width, cell_height
        for y in range(self.height):
            for x in range(self.width):
                r = Rect(x * cell_width, y * cell_height, cell_width, cell_height)
                self[(x, y)] = r

    @property
    def cell_width(self) -> int:
        return self._cw

    @property
    def cell_height(self) -> int:
        return self._ch

    def __setitem__(self, coord: Tuple[int, int], value: Union[None, Any]):
        raise NotImplemented("RectGrid does not support assignment")

    def __delitem__(self, coord: Tuple[int, int]):
        raise NotImplemented("RectGrid does not support deletion")
