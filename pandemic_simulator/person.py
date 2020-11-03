from enum import Enum
from typing import Optional

from grid_2d import Coordinate
import pandemic_simulator.constants as constants


class Health(Enum):
    SUSCEPTIBLE = 0
    RECOVERED = 1
    INFECTED = 2


class Person:
    def __init__(self, x, y, is_initially_infected: bool):
        self._coordinate = Coordinate(x, y)
        self._health = Health.INFECTED if is_initially_infected else Health.SUSCEPTIBLE
        self._day_infected: int = -1  # tattoo

    def __repr__(self):
        if self._health == Health.SUSCEPTIBLE:
            return " SS "
        elif self._health == Health.RECOVERED:
            return " RR "
        elif self._health == Health.INFECTED:
            return " II "
        else:
            raise Exception("You haven't yet handled how to represent this health state...")

    @property
    def position(self):
        return self._coordinate

    @property
    def is_infected(self):
        return self._health == Health.INFECTED

    @property
    def is_susceptible(self):
        return self._health == Health.SUSCEPTIBLE

    @property
    def is_recovered(self):
        return self._health == Health.RECOVERED

    @property
    def day_infected(self):
        return self._day_infected

    def recover(self):
        self._health = Health.RECOVERED

    def age(self, day: int):
        if self.is_infected:
            if day - self._day_infected > constants.RECOVERY_PERIOD:
                self.recover()

    def infect(self, day: int):
        if self.is_susceptible:
            self._day_infected = day
            self._health = Health.INFECTED
