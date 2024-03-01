import numpy as np

class TokenSaleSimulation:
    def __init__(
            self,
            prices,
            probabilities,
            total_tokens,
            initial_sell_percentages,
            capital_gains_rate=0.25
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
        self.capital_gains_rate = capital_gains_rate

    def run_simulation(self, num_iterations):
        """
        Run the simulation to optimize the distribution of selling percentages.

        Parameters:
        - num_iterations: int, the number of iterations to perform for optimization.

        Returns:
        - optimized_percentages: List[float], optimized percentages for selling at each price point.
        """
        # Placeholder for optimization logic
        optimized_percentages = self.optimize_percentages(num_iterations)
        return optimized_percentages

    def determine_max_price(self):
        random_prob = np.random.rand()  # Generate a random number between 0 and 1
        index_of_max_price = 0  # Initialize with 0, assuming the first price is the minimum fallback
        for index, (price, prob) in enumerate(zip(self.prices, self.probabilities)):
            if random_prob <= prob:
                index_of_max_price = index
        print(f"Random probability: {random_prob}, Index of max price: {index_of_max_price}, price: {self.prices[index_of_max_price]}")
        return index_of_max_price

    def optimize_percentages(self, num_iterations):
        """
        Optimize the selling percentages for maximum expected total net gain.

        This is a placeholder for the optimization algorithm.

        Parameters:
        - num_iterations: int, the number of iterations for the optimization process.

        Returns:
        - optimized_percentages: List[float], optimized selling percentages.
        """
        # Placeholder for the optimization algorithm
        # This should adjust self.percentages based on simulation results
        optimized_percentages = self.percentages  # Placeholder return
        return optimized_percentages

    def simulate_once(self):
        """
        Run a single simulation of selling tokens based on the current percentages.

        Returns:
        - total_net_gain: float, the total net gain from this simulation.
        """
        # Placeholder for a single simulation run
        price_index = self.determine_max_price()

        # Initialize total net gain
        total_net_gain = 0

        # Loop through each price point up to and including the price_index
        for i in range(price_index + 1):
            # Calculate the gain for this price point
            # Assuming you have an array called `self.net_gains` that corresponds to net gains at each price point
            gain_at_price = self.total_tokens * self.percentages[i] * self.prices[i] * (1 - self.capital_gains_rate)

            print(f"Gain at price {self.prices[i]}: {gain_at_price}")
            # Add the gain from this price point to the total net gain
            total_net_gain += gain_at_price
            print(f"Total net gain:   {total_net_gain}")

        return total_net_gain
