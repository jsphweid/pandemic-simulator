from pandemic_simulator import input_helpers, PandemicSimulator, make_film, analytics

simulator = PandemicSimulator(
    initial_population_percentage=input_helpers.get_initial_population_percent(),
    initial_infection_percentage=input_helpers.get_intial_infection_percentage(),
    spread_chance=input_helpers.get_spread_chance()
)

simulator.run(40)

# make_film(simulator.states, "test.mpeg")

analytics.run(simulator.states)
