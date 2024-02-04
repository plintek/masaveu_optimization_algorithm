""" This module contains the scoring functions and the scoring logic. """
from .score_functions.distance import distance


class ScoreFunction:
    """
    Represents a scoring function with a name, function, and weight.
    """

    def __init__(self, name, func, weight=1):
        """
        Initializes a ScoreFunction object.

        Args:
            name (str): The name of the scoring function.
            func (function): The scoring function.
            weight (float, optional): The weight of the scoring function. Defaults to 1.
        """
        self.name = name
        self.func = func
        self.weight = weight

    def __call__(self, *args, **kwargs):
        """
        Calls the scoring function with the given arguments and returns the result multiplied by the weight.

        Returns:
            float: The weighted score.
        """
        return self.func(*args, **kwargs) * self.weight

    def __str__(self):
        """
        Returns a string representation of the scoring function.

        Returns:
            str: The name of the scoring function.
        """
        return self.name

    def __repr__(self):
        """
        Returns a string representation of the ScoreFunction object.

        Returns:
            str: The string representation of the ScoreFunction object.
        """
        return f"ScoreFunction(name={self.name}, func={self.func}, weight={self.weight})"


def score_vehicles(order, vehicles):
    """
    Scores the vehicles based on the given order.

    Args:
        order (Order): The order to be scored.
        vehicles (list): The list of vehicles to be scored.

    Returns:
        list: The list of vehicles with scores.
    """
    score_functions = [
        ScoreFunction("distance", distance, 0.2),
    ]

    for vehicle in vehicles:
        for score_function in score_functions:
            vehicle.add_score(score_function(order=order, vehicle=vehicle))

    print(f"DEBUG: Vehículos puntuados: {vehicles}")

    return vehicles
