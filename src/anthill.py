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

    def __iter__(self):
        return iter(self.ants)

    def __len__(self):
        return len(self.ants)
