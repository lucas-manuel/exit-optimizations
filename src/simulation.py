import numpy as np
from scipy.stats import trim_mean

class TokenSaleSimulation:
    def __init__(
            self,
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
        ):

        self.cost_basis               = cost_basis
        self.prices                   = prices
        self.probabilities            = probabilities
        self.total_tokens             = total_tokens
        self.percentages              = initial_sell_percentages
        self.num_iterations           = num_iterations
        self.capital_gains_rate       = capital_gains_rate
        self.adjustment_rate_factor   = adjustment_rate_factor
        self.adjustment_number_factor = adjustment_number_factor
        self.num_simulations          = num_simulations

    def run_simulation(self):
        optimized_percentages, best_average_net_gain = self.optimize_percentages(self.num_iterations)
        return optimized_percentages, best_average_net_gain

    def determine_randomized_max_price(self):
        random_prob = np.random.rand()  # Generate a random number between 0 and 1
        index_of_max_price = 0  # Initialize with 0, assuming the first price is the minimum fallback
        for index, (price, prob) in enumerate(zip(self.prices, self.probabilities)):
            if random_prob <= prob:
                index_of_max_price = index
        # print(f"Random probability: {random_prob}, Index of max price: {index_of_max_price}, price: {self.prices[index_of_max_price]}")
        return index_of_max_price

    def optimize_percentages(self, num_iterations):
        best_percentages = self.percentages.copy()
        best_standard_deviation = np.inf

        best_net_gain = -np.inf

        for _ in range(num_iterations):
            # Create a new set of percentages by making a small adjustment
            new_percentages = self.adjust_percentages(best_percentages)

            # Temporarily update the percentages to the new percentages
            self.percentages = new_percentages

            simulation_results = self.run_all_simulations()

            # Evaluate the new percentages by running a simulation
            mean_net_gain = self.calculate_mean(simulation_results)
            median_net_gain = self.calculate_median(simulation_results)
            trimmed_mean_net_gain = self.calculate_trimmed_mean(simulation_results, 0.3)
            standard_deviation = self.calculate_standard_deviation(simulation_results)

            # # If the new percentages result in a better average net gain, keep them
            # if mean_net_gain > best_net_gain:
            #     best_percentages = new_percentages.copy()
            #     best_net_gain = mean_net_gain
            #     print(f"New best net gain: ${best_net_gain:,.2f} with percentages {[f'{p * 100:.2f}%' for p in best_percentages]}")
            #     print(f"Variance: {variance}")
            # else:
            #     # Revert to the best known percentages if no improvement
            #     self.percentages = best_percentages

            # # If the new percentages result in a better average net gain, keep them
            # if median_net_gain > best_net_gain:
            #     best_percentages = new_percentages.copy()
            #     best_net_gain = median_net_gain
            #     print(f"New best net gain: ${best_net_gain:,.2f} with percentages {[f'{p * 100:.2f}%' for p in best_percentages]}")
            # else:
            #     # Revert to the best known percentages if no improvement
            #     self.percentages = best_percentages

            # If the new percentages result in a better average net gain, keep them
            if trimmed_mean_net_gain > best_net_gain and (standard_deviation < best_standard_deviation or standard_deviation < 400_000):
                best_percentages = new_percentages.copy()
                best_net_gain = trimmed_mean_net_gain
                best_standard_deviation = standard_deviation
                print(f"New best net gain: ${best_net_gain:,.2f} with percentages {[f'{p * 100:.2f}%' for p in best_percentages]}")
                print(f"Standard deviation: ${best_standard_deviation:,.2f}")
                print()
            else:
                # Revert to the best known percentages if no improvement
                self.percentages = best_percentages

        # After optimization, set the percentages to the best found
        self.percentages = best_percentages
        return best_percentages, best_net_gain

    def adjust_percentages(self, percentages):
        new_percentages = percentages.copy()
        # More aggressive adjustment: modify a larger chunk of the percentages
        num_adjustments = int(len(new_percentages) * self.adjustment_number_factor * np.random.rand())
        # print(f"num_adjustments {num_adjustments}")

        for _ in range(num_adjustments):
            idx_from, idx_to = np.random.choice(len(new_percentages), 2, replace=False)
            adjustment = np.random.rand() * self.adjustment_rate_factor  # Larger adjustment

            # More aggressive checking to avoid negative percentages
            if new_percentages[idx_from] - adjustment > 0:
                new_percentages[idx_from] -= adjustment
                new_percentages[idx_to] += adjustment
            else:
                # If we can't make the desired adjustment without going negative, try a smaller adjustment
                smaller_adjustment = new_percentages[idx_from] * np.random.rand()
                new_percentages[idx_from] -= smaller_adjustment
                new_percentages[idx_to] += smaller_adjustment

        # Ensure the percentages still sum to 1 (or 100%) after adjustments
        total_percentage = sum(new_percentages)
        new_percentages = [p / total_percentage for p in new_percentages]

        return new_percentages

    def run_all_simulations(self):
        results = [self.simulate_once() for _ in range(self.num_simulations)]
        return results

    def calculate_trimmed_mean(self, values, proportion_to_trim):
        return trim_mean(values, proportion_to_trim)

    def calculate_mean(self, results):
        if not results:
            return 0
        return sum(results) / len(results)

    def calculate_median(self, results):
        if not results:
            return 0
        sorted_results = sorted(results)
        n = len(sorted_results)
        midpoint = n // 2
        if n % 2 == 1:
            # If odd, return the middle value
            return sorted_results[midpoint]
        else:
            # If even, return the average of the two middle values
            return (sorted_results[midpoint - 1] + sorted_results[midpoint]) / 2.0

    def calculate_standard_deviation(self, results):
        if not results:
            return 0
        # print(f"Results: {results}")
        return np.sqrt(np.var(results, ddof=1))

    def simulate_average_net_gain(self):
        average_net_gain = sum(self.simulate_once() for _ in range(self.num_simulations)) / self.num_simulations
        return average_net_gain

    def simulate_once(self):
        price_index = self.determine_randomized_max_price()

        # print(f"Price index: {price_index}, Price: {self.prices[price_index]}")

        total_net_gain = 0

        # Loop through each price point up to and including the price_index
        for i in range(price_index + 1):
            # Calculate the gain for this price point
            # Assuming you have an array called `self.net_gains` that corresponds to net gains at each price point

            gain_at_price = self.total_tokens * self.percentages[i] * (self.prices[i] - self.cost_basis) * (1 - self.capital_gains_rate)

            # print(f"Gain at price {self.prices[i]}: {gain_at_price}")
            # Add the gain from this price point to the total net gain
            total_net_gain += gain_at_price
            # print()
            # print(f"Total net gain:   {total_net_gain}")

            # print(f"self.total_tokens {self.total_tokens}")
            # print(f"self.percentages[i] {self.percentages[i]}")
            # print(f"self.prices[i] {self.prices[i]}")
            # print(f"self.self.cost_basis {self.cost_basis}")
            # print(f"self.capital_gains_rate {self.capital_gains_rate}")
            # print(f"self.gain_at_price {gain_at_price}")

        return total_net_gain
