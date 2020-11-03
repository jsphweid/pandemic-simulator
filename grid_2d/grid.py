import random
from copy import deepcopy
from typing import Callable, TypeVar, List, Optional, Generic, Union

from grid_2d.structs import Coordinate

T = TypeVar('T')
GridState = List[List[Optional[T]]]


class Grid(Generic[T]):
    """
    A 2-dimensional grid that assumes each item is either None or T
    """

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

        # initialize with None's
        self._raw_grid: GridState = []
        for i in range(height):
            row = [None] * width
            self._raw_grid.append(row)

    def _is_valid_coordinate(self, coordinate: Coordinate) -> bool:
        return 0 <= coordinate.x < self._width and 0 <= coordinate.y < self._height

    def randomly_place(self, minimum_percent: float, handler: Union[Callable[[], T], Callable[[Coordinate], T]]) -> None:
        current_filled_percent = 0
        increment = 1 / (self._width * self._height)
        while current_filled_percent < minimum_percent:
            x = random.randrange(0, self._width)
            y = random.randrange(0, self._height)
            if self._raw_grid[y][x] is None:
                self._raw_grid[y][x] = handler(Coordinate(x, y)) if handler.__code__.co_argcount == 1 else handler()
                current_filled_percent += increment

    def get_neighbors(self, coordinate: Coordinate) -> List[T]:
        # TODO: this can be optimized by doing the gathering/filtering in one step
        neighbors = []
        x = coordinate.x
        y = coordinate.y

        top = Coordinate(x, y + 1)
        top_right = Coordinate(x + 1, y + 1)
        top_left = Coordinate(x - 1, y + 1)
        bottom = Coordinate(x, y - 1)
        bottom_right = Coordinate(x + 1, y - 1)
        bottom_left = Coordinate(x - 1, y - 1)
        left = Coordinate(x - 1, y)
        right = Coordinate(x + 1, y)

        for coordinate in [top, bottom, left, right, top_right, top_left, bottom_right, bottom_left]:
            if self._is_valid_coordinate(coordinate):
                possible_neighbor = self._raw_grid[coordinate.y][coordinate.x]
                if possible_neighbor:
                    neighbors.append(possible_neighbor)

        return neighbors

    def iterate_over_non_none_items(self, handler: Callable[[T], Optional[T]]) -> None:
        for i in range(self._height):
            for j in range(self._width):
                item = self._raw_grid[i][j]

                if item:
                    return_item = handler(item)

                    if return_item:
                        self._raw_grid[i][j] = return_item

    def pretty_print_current_state(self, additional_text="") -> None:
        print(f'------------ {additional_text}')
        for row in self._raw_grid:
            print(row)

    def export_current_grid_state(self) -> GridState:
        return deepcopy(self._raw_grid)

    def force_set_grid_state(self, grid_state: GridState) -> None:
        self._raw_grid = grid_state

    def get_population(self) -> int:
        total = 0
        for row in self._raw_grid:
            for item in row:
                if item:
                    total += 1
        return total
