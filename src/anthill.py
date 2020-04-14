"""
    Created by: Rafal Uzarowicz
    Date of creation: 31.03.2020
    Github: https://github.com/RafalUzarowicz
"""


class Anthill:
    class Ant:
        def __init__(self):
            self.path = []
            self.distance_traveled = 0
            self.has_found = False

    def __init__(self, ants_num: int):
        if ants_num <= 0:
            raise ValueError
        self.ants = [self.Ant() for i in range(ants_num)]
        self.ants_num = ants_num

    def __iter__(self):
        return iter(self.ants)

    def __len__(self):
        return len(self.ants)

    def reset_ants(self):
        for ant in self.ants:
            ant.has_found = False
            ant.path = []
            ant.distance_traveled = 0

    def get_best_ant(self):
        if not len(self.ants):
            return None
        best_ant = self.ants[0]
        for ant in self.ants:
            if best_ant.distance_traveled > ant.distance_traveled:
                best_ant = ant
        return best_ant

    def get_worst_ant(self):
        if not len(self.ants):
            return None
        worst_ant = self.ants[0]
        for ant in self.ants:
            if worst_ant.distance_traveled < ant.distance_traveled:
                worst_ant = ant
        return worst_ant
