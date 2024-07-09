""" This module contains the scoring functions and the scoring logic. """
from .score_functions.last_trimester_orders import last_trimester_orders
from .score_functions.last_trimester_mileage import last_trimester_mileage


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


def normalize_scores(scores):
    min_score = min(scores)
    max_score = max(scores)
    if max_score == min_score:
        return [0.5] * len(scores)  # Return 0.5 if all scores are the same
    return [(score - min_score) / (max_score - min_score) for score in scores]

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
        ScoreFunction("last_trimester_orders", last_trimester_orders, 0.5),
        ScoreFunction("last_trimester_mileage", last_trimester_mileage, 0.5),
    ]

    for vehicle in vehicles:
        for score_function in score_functions:
            score_base = score_function(order=order, vehicle=vehicle)
            for compare_vehicle in vehicles:
                if compare_vehicle.uid == vehicle.uid:
                    continue

                score_compare = score_function(order=order, vehicle=compare_vehicle)
                score = score_base - score_compare
                vehicle.add_score(score)

     # Gather all scores for normalization
    scores = [vehicle.score for vehicle in vehicles]

    if len(scores) > 0:
        normalized_scores = normalize_scores(scores)

        for vehicle, norm_score in zip(vehicles, normalized_scores):
            vehicle.score = norm_score

    return vehicles