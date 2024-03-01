from simulation import MonteCarloSimulation

def main():
    # Create an instance of the MonteCarloSimulation class
    simulation = MonteCarloSimulation()

    # Specify the number of simulations to run
    num_simulations = 1000  # Example number

    # Run the simulation
    results = simulation.run_simulation(num_simulations)

    # Process the results (This part depends on how you've implemented your simulation)
    print(results)

if __name__ == "__main__":
    main()
