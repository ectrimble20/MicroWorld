class Grid(object):
    """
    Grid
    @version 1.0

    Grid represents an area using a 2D array.  It provides utility functions for accessing and storing data and can be
    used to represent points in space (2D space that is) by utilizing it's coordinate system.  The Grid itself does not
    directly store any global location, but it does store data using X/Y coordinates that can then be converted into
    global locations.

    While the Grid itself is basically just a wrapper for a 2D array, it provides access via over-riding the
    functionality provided by getitem and setitem data model methods.  This allows Grid coordinates to be accessed a bit
    more fluidly, for example:
    g = Grid(30, 30)
    point = g[(10, 10)]

    It also implements the contains methods to allow for testing of points:
    if (10, 10) in g:
        # do something

    As well as implementing a context manager for iterating the entire grid:
    with grid as g:
        for (x, y), point in g:
            # do stuff

    While these aren't the most necessary functions to have for the primary uses of the grid, it does provide the
    functionality if it is required for niche cases.
    """

    def __init__(self, width, height):
        self._w, self._h = width, height
        self._grid = [
            [
                None for _ in range(self._w)
            ] for _ in range(self._h)
        ]

    @property
    def width(self):
        return self._w

    @property
    def height(self):
        return self._h

    def __contains__(self, point):
        """
        Implements the 'in' statement to allow for points to be checked using '(1, 1) in grid' syntax
        :param point: tuple[int, int]
        :return: boolean
        """
        return 0 <= point[0] < self._w and 0 <= point[1] < self._h

    def __getitem__(self, point):
        """
        Retrieve a value stored at a point.  If the point is invalid, None is returned.
        :param point: tuple[int, int]
        :return: any|None
        """
        if point in self:
            return self._grid[point[1]][point[0]]
        else:
            return None

    def __setitem__(self, point, value):
        """
        Sets a value at a point.  If the point is invalid, no action is taken.
        :param point: tuple[int, int]
        :param value: any
        :return: None
        """
        if point in self:
            self._grid[point[1]][point[0]] = value

    def __delitem__(self, point):
        """
        Deletes a value at a point, it does not remove the coordinate, it simply sets it's value to None
        :param point: tuple[int, int]
        :return: None
        """
        if point in self:
            self._grid[point[1]][point[0]] = None

    def __enter__(self):
        """
        Implements context manager syntax to allow for the Grid to be iterated on.  Example 'with grid as (x, y), value'
        :return: tuple[int, int], any
        """
        for y in range(self._h):
            for x in range(self._w):
                yield (x, y), self[(x, y)]

    def __exit__(self, *args):
        """
        Required for context manager support, this doesn't do anything special.
        :param args: any
        :return: boolean
        """
        return True


class TileEntityTransferObject(object):
    """
    TileEntityTransferObject
    @version 1.0

    This is just a skeleton right now, but it's purpose will be to store tile entities for a map or saved game.  These
    entities will be tracked here and this object should be used to inject tile entities into a game map.
    """

    def __init__(self, tile_entities: dict):
        pass


class MapTransferObject(object):
    """
    MapTransferObject
    @version 1.0

    Used to load and save data to and from Map utilities.
    """

    def __init__(self, map_data: dict):
        self.name = map_data['name']
        self.desc = map_data.get('desc', 'No Description')
        self.size = map_data['size']
        self.tile_grid = Grid(*self.size)
        for x, y, tile_type in map_data['tiles']:
            # TODO we'll want to make this a tile object of some sort
            self.tile_grid[(x, y)] = tile_type
        self.tile_entities = TileEntityTransferObject(map_data['tile_entities'])
