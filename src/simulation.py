import numpy as np

class TokenSaleSimulation:
    def __init__(
            self,
            prices,
            probabilities,
            total_tokens,
            initial_sell_percentages,
            num_iterations,
            capital_gains_rate
        ):
        """
        Initialize the simulation parameters.

        Parameters:
        - prices: List[float], predetermined selling prices.
        - probabilities: List[float], probability of each price being the selling point.
        - total_tokens: int, total number of tokens available for sale.
        - initial_percentages: List[float], initial distribution percentages of tokens to sell at each price.
        """
        self.prices             = prices
        self.probabilities      = probabilities
        self.total_tokens       = total_tokens
        self.percentages        = initial_sell_percentages
        self.num_iterations     = num_iterations
        self.capital_gains_rate = capital_gains_rate

    def run_simulation(self):
        """
        Run the simulation to optimize the distribution of selling percentages.

        Parameters:
        - num_iterations: int, the number of iterations to perform for optimization.

        Returns:
        - optimized_percentages: List[float], optimized percentages for selling at each price point.
        """
        optimized_percentages = self.optimize_percentages(self.num_iterations)
        return optimized_percentages

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
        best_average_net_gain = -np.inf

        for _ in range(num_iterations):
            # Create a new set of percentages by making a small adjustment
            new_percentages = self.adjust_percentages(best_percentages)

            # Temporarily update the percentages to the new percentages
            self.percentages = new_percentages

            # Evaluate the new percentages by running a simulation
            average_net_gain = self.simulate_average_net_gain()

            # If the new percentages result in a better average net gain, keep them
            if average_net_gain > best_average_net_gain:
                best_percentages = new_percentages.copy()
                best_average_net_gain = average_net_gain
                print(f"New best net gain: {best_average_net_gain} with percentages {best_percentages}")
            else:
                # Revert to the best known percentages if no improvement
                self.percentages = best_percentages

        # After optimization, set the percentages to the best found
        self.percentages = best_percentages
        return best_percentages

    def adjust_percentages(self, percentages):
        """
        Adjust the percentages slightly to explore the solution space.

        Parameters:
        - percentages: List[float], the current distribution percentages of tokens to sell.

        Returns:
        - List[float], new adjusted percentages.
        """
        new_percentages = percentages.copy()
        # Example adjustment: randomly select two indices and transfer a small percentage from one to the other
        idx_from, idx_to = np.random.choice(len(new_percentages), 2, replace=False)
        adjustment = np.random.rand() * 0.01  # Up to 1% adjustment for simplicity
        if new_percentages[idx_from] > adjustment:  # Ensure we don't go negative
            new_percentages[idx_from] -= adjustment
            new_percentages[idx_to]   += adjustment
        return new_percentages

    def simulate_average_net_gain(self):
        """
        A helper method to calculate the average net gain for the current percentages
        by running multiple simulations and averaging the result.

        Returns:
        - float, the average average net gain from the simulations.
        """
        num_simulations = 100000  # Number of simulations to run for averaging
        average_net_gain = sum(self.simulate_once() for _ in range(num_simulations)) / num_simulations
        # print(f"Average net gain: {average_net_gain}")
        return average_net_gain

    def simulate_once(self):
        """
        Run a single simulation of selling tokens based on the current percentages.

        Returns:
        - total_net_gain: float, the total net gain from this simulation.
        """
        # Placeholder for a single simulation run
        price_index = self.determine_randomized_max_price()

        # Initialize total net gain
        total_net_gain = 0

        # Loop through each price point up to and including the price_index
        for i in range(price_index + 1):
            # Calculate the gain for this price point
            # Assuming you have an array called `self.net_gains` that corresponds to net gains at each price point
            gain_at_price = self.total_tokens * self.percentages[i] * self.prices[i] * (1 - self.capital_gains_rate)

            # print(f"Gain at price {self.prices[i]}: {gain_at_price}")
            # Add the gain from this price point to the total net gain
            total_net_gain += gain_at_price
            # print(f"Total net gain:   {total_net_gain}")

        return total_net_gain
