import pytest

from grid_2d import Grid, Coordinate


@pytest.mark.parametrize("minimum_percent, minimum_population_size", [
    (0.5, 50),
    (0.51, 51),
    (0.10, 10),
    (0.01, 1),
])
def test_randomly_place(minimum_percent, minimum_population_size):
    grid = Grid(10, 10)
    grid.randomly_place(minimum_percent, lambda: 'lol')
    assert grid.get_population() >= minimum_population_size


def test_center_of_3x3_has_8_neighbors():
    grid = Grid(3, 3)
    grid.randomly_place(1, lambda: 'lol')
    assert len(grid.get_neighbors(Coordinate(1, 1))) == 8


class TestNeighbors:

    def setup_method(self):
        self.grid = Grid(3, 3)
        self.grid._raw_grid = [
            [0, 0, 'lol'],
            [0, 0, 'lol'],
            [0, 0, 'lol'],
        ]

    @pytest.mark.parametrize("coordinate, expected_number_of_neighbors", [
        (Coordinate(0, 0), 0),
        (Coordinate(0, 1), 0),
        (Coordinate(0, 2), 0),
        (Coordinate(1, 0), 2),
        (Coordinate(1, 1), 3),
        (Coordinate(1, 2), 2),
        (Coordinate(2, 0), 1),
        (Coordinate(2, 1), 2),
        (Coordinate(2, 2), 1),
    ])
    def test_corner_has_1_neighbor(self, coordinate, expected_number_of_neighbors):
        assert len(self.grid.get_neighbors(coordinate)) == expected_number_of_neighbors
