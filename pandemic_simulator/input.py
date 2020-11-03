import pandemic_simulator.constants as constants


def _get_valid_input_percent_with_default(message: str, default: float) -> float:
    result = input(f"{message} (Default is {default}):") or str(default)
    num = float(result)
    assert 1 >= num >= 0
    return num


def get_initial_population_percent() -> float:
    return _get_valid_input_percent_with_default("Enter initial population percent",
                                                 constants.DEFAULT_INITIAL_POPULATION_PERCENTAGE)


def get_intial_infection_percentage() -> float:
    return _get_valid_input_percent_with_default("Enter initial infection percentage",
                                                 constants.DEFAULT_INITIAL_INFECTION_PERCENTAGE)


def get_spread_chance() -> float:
    return _get_valid_input_percent_with_default("Enter spread chance", constants.DEFAULT_SPREAD_CHANCE)
