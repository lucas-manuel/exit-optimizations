from simulation import TokenSaleSimulation

def main():
    cost_basis    = 4.22
    # prices        = [20,  30,   40,  50,   60,  70,  80,  90,  100]
    # probabilities = [1.0, 0.95, 0.8, 0.75, 0.7, 0.6, 0.5, 0.3, 0.2]
    prices        = [20,  40,  60,  80,  100, 150, 200]
    probabilities = [1.0, 0.9, 0.8, 0.6, 0.4, 0.2, 0.1]
    total_tokens = 1000
    initial_sell_percentages = [0.1] * len(prices)
    num_iterations = 1_000_000
    capital_gains_rate = 0.25
    adjustment_rate_factor = 0.10
    adjustment_number_factor = 1.00  # 20% of positions
    num_simulations = 100_000

    # Perform an initial simulation with high iterations and low simulations
    # with a high adjustment factor to get a rough estimate of the optimized percentages
    initial_simulation = TokenSaleSimulation(
        cost_basis,
        prices,
        probabilities,
        total_tokens,
        initial_sell_percentages,
        num_iterations,
        capital_gains_rate,
        adjustment_rate_factor,
        adjustment_number_factor,
        num_simulations
    )

    # Call the simulate_sales method
    optimized_percentages, best_average_net_gain = initial_simulation.run_simulation()
    total_value = best_average_net_gain + (total_tokens * cost_basis)
    print()
    print()
    print(f"The initial optimized percentages are {[f'{p * 100:.2f}%' for p in optimized_percentages]}")
    print(f"The best average net gain is ${best_average_net_gain:,.2f}")
    print(f"The total value is ${total_value:,.2f}")
    print()

    # adjustment_rate_factor   = 0.05
    # adjustment_number_factor = 0.10  # 10% of positions
    # num_simulations          = 100_000

    # # Perform a final simulation with the optimized percentages
    # final_simulation = TokenSaleSimulation(
    #     cost_basis,
    #     prices,
    #     probabilities,
    #     total_tokens,
    #     optimized_percentages,
    #     num_iterations,
    #     capital_gains_rate,
    #     adjustment_rate_factor,
    #     adjustment_number_factor,
    #     num_simulations
    # )

    # # Call the simulate_sales method
    # optimized_percentages, best_average_net_gain = final_simulation.run_simulation()
    # total_value = best_average_net_gain + (total_tokens * cost_basis)
    # print()
    # print()
    # print(f"The final optimized percentages are {[f'{p * 100:.2f}%' for p in optimized_percentages]}")
    # print(f"The best average net gain is ${best_average_net_gain:,.2f}")
    # print(f"The total value is ${total_value:,.2f}")
    # print(f"The total value in CAD is ${total_value * 1.36:,.2f}")


if __name__ == "__main__":
    main()
