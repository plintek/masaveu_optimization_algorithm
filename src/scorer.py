class ScoreFunction:
    def __init__(self, name, func, weight=1):
        self.name = name
        self.func = func
        self.weight = weight

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs) * self.weight

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"ScoreFunction(name={self.name}, func={self.func}, weight={self.weight})"


def score_vehicles(order, vehicles, origin, destination):
    score_functions = [
        # ScoreFunction("national_international", national_international),
    ]

    for vehicle in vehicles:
        for score_function in score_functions:
            vehicle.add_score(score_function(order=order, vehicle=vehicle, origin=origin, destination=destination))

    return vehicles