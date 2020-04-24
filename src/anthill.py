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

    def __str__(self):
        string = ""
        for ant in self.ants:
            string += str(ant.distance_traveled) + ":" + str(ant.path) + "\n"
        return string

    def reset_ants(self):
        for ant in self.ants:
            ant.has_found = False
            ant.path = []
            ant.distance_traveled = 0

    def get_best_ant(self):
        if not len(self.ants):
            return None
        best_ant = None
        i = 0
        while i < len(self.ants) and not self.ants[i].has_found:
            i += 1
        if i < len(self.ants):
            best_ant = self.ants[i]
        else:
            return Anthill.Ant()
        for j in range(i, len(self.ants)):
            if best_ant.distance_traveled > self.ants[j].distance_traveled and self.ants[i].has_found:
                best_ant = self.ants[j]
        return best_ant

    def get_worst_ant(self):
        if not len(self.ants):
            return None
        worst_ant = None
        i = 0
        while i < len(self.ants) and not self.ants[i].has_found:
            i += 1
        if i < len(self.ants):
            worst_ant = self.ants[i]
        else:
            return Anthill.Ant()
        for j in range(i, len(self.ants)):
            if worst_ant.distance_traveled < self.ants[j].distance_traveled and self.ants[j].has_found:
                worst_ant = self.ants[j]
        return worst_ant
