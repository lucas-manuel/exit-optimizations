from simulation import TokenSaleSimulation

def main():
    prices = [10, 20, 30]
    probabilities = [1.0, 0.8, 0.3]
    total_tokens = 1000
    initial_sell_percentages = [0.5, 0.3, 0.2]
    capital_gains_rate = 0.25

    # Instantiate the simulation class
    simulation = TokenSaleSimulation(prices, probabilities, total_tokens, initial_sell_percentages)

    # Call the simulate_sales method
    total_gain = simulation.simulate_once()
    print(f"The determined gain is ${total_gain}")

if __name__ == "__main__":
    main()
