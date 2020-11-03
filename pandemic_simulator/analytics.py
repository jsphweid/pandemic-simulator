from typing import Any, List, NamedTuple

from pandemic_simulator.simulator import PandemicSimulationState


class Results(NamedTuple):
    number_recovered: int
    number_susceptible: int
    number_infected: int

    def print(self):
        print("Number Recovered:", self.number_recovered)
        print("Number Susceptible:", self.number_susceptible)
        print("Number Infected:", self.number_infected)


def get_results_for_state(state: PandemicSimulationState) -> Results:
    number_recovered = 0
    number_susceptible = 0
    number_infected = 0

    for row in state:
        for maybe_person in row:
            if maybe_person:
                if maybe_person.is_recovered:
                    number_recovered += 1
                elif maybe_person.is_susceptible:
                    number_susceptible += 1
                elif maybe_person.is_infected:
                    number_infected += 1

    return Results(number_recovered, number_susceptible, number_infected)


def run(states: List[PandemicSimulationState]) -> Any:
    if len(states) == 0:
        raise Exception("Can't run analytics on no states...")

    get_results_for_state(states[0]).print()
    get_results_for_state(states[-1]).print()


