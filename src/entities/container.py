"""Container module"""


class Container:
    """Container entity"""

    def __init__(self, sacos, pales, fardos, fundas, laminas, big_bags):
        self.sacos = sacos
        self.pales = pales
        self.fardos = fardos
        self.fundas = fundas
        self.laminas = laminas
        self.big_bags = big_bags

    def __str__(self):
        return f"{self.sacos} {self.pales} {self.fardos} {self.fundas} {self.laminas} {self.big_bags}"

    def __repr__(self):
        return f"{self.sacos} {self.pales} {self.fardos} {self.fundas} {self.laminas} {self.big_bags}"

    @staticmethod
    def from_json(container):
        """Create a Container object from a JSON dictionary."""
        return Container(
            container["sacos"],
            container["pales"],
            container["fardos"],
            container["fundas"],
            container["laminas"],
            container["big_bags"],
        )
