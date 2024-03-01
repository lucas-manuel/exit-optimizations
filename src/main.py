from simulation import TokenSaleSimulation

def main():
    prices = [10, 20, 30]
    probabilities = [1.0, 0.8, 0.3]  # Inverse probabilities

    # Instantiate the simulation class
    simulation = TokenSaleSimulation(prices, probabilities, 0, 0)

    # Call the simulate_sales method
    price_index = simulation.determine_max_price()
    print(f"The determined max price is ${simulation.prices[price_index]}")

if __name__ == "__main__":
    main()
