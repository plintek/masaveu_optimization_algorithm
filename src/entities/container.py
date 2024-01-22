class Container:
    def __init__(self, sacos, pales, fardos, fundas, laminas, bigBags):
        self.sacos = sacos
        self.pales = pales
        self.fardos = fardos
        self.fundas = fundas
        self.laminas = laminas
        self.bigBags = bigBags

    def __str__(self):
        return f'{self.sacos} {self.pales} {self.fardos} {self.fundas} {self.laminas} {self.bigBags}'

    def __repr__(self):
        return f'{self.sacos} {self.pales} {self.fardos} {self.fundas} {self.laminas} {self.bigBags}'

    @staticmethod
    def from_json(container):
        return Container(container['sacos'], container['pales'], container['fardos'], container['fundas'], container['laminas'], container['bigBags'])