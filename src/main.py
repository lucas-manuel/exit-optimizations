from simulation import TokenSaleSimulation

def main():
    prices = [10, 20, 30]
    probabilities = [1.0, 0.8, 0.3]
    total_tokens = 1000
    initial_sell_percentages = [0.5, 0.3, 0.2]
    num_iterations = 100000
    capital_gains_rate = 0.25

    # Instantiate the simulation class
    simulation = TokenSaleSimulation(
        prices,
        probabilities,
        total_tokens,
        initial_sell_percentages,
        num_iterations,
        capital_gains_rate
    )

    # Call the simulate_sales method
    optimized_percentages = simulation.run_simulation()
    print(f"The optimized percentages are ${optimized_percentages}")

if __name__ == "__main__":
    main()
