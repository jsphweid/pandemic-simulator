import random
from typing import List, Optional

from grid_2d import Grid

import pandemic_simulator.constants as constants
from pandemic_simulator.person import Person

generation = 0

PandemicSimulationState = List[List[Optional[Person]]]


class PandemicSimulator:

    def __init__(self,
                 initial_population_percentage: float = constants.DEFAULT_INITIAL_POPULATION_PERCENTAGE,
                 initial_infection_percentage: float = constants.DEFAULT_INITIAL_INFECTION_PERCENTAGE,
                 spread_chance: float = constants.DEFAULT_SPREAD_CHANCE,
                 width: int = constants.DEFAULT_WIDTH,
                 height: int = constants.DEFAULT_HEIGHT):
        self._spread_chance = spread_chance

        self._grid: Grid[Person] = Grid(width, height)
        self._grid.randomly_place(initial_population_percentage,
                                  lambda coordinate: Person(coordinate.x,
                                                            coordinate.y,
                                                            is_initially_infected=random.random() < initial_infection_percentage))
        self._initial_randomized_grid_state = self._grid.export_current_grid_state()
        self._states = [self._initial_randomized_grid_state]

    @property
    def states(self) -> List[PandemicSimulationState]:
        return self._states

    def reset(self) -> None:
        self._grid.force_set_grid_state(self._initial_randomized_grid_state)
        self._states = [self._initial_randomized_grid_state]

    def run(self, number_of_steps: int) -> List[PandemicSimulationState]:
        for step in range(0, number_of_steps):

            def run_generation_on_people(person: Person):
                person.age(step)

                if person.is_infected:
                    for neighbor in self._grid.get_neighbors(person.position):
                        should_infect = random.random() < self._spread_chance
                        if should_infect:
                            neighbor.infect(step)

            self._grid.iterate_over_non_none_items(run_generation_on_people)
            self._states.append(self._grid.export_current_grid_state())

        return self._states
