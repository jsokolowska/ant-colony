"""
    Created by: Rafal Uzarowicz
    Date of creation: 31.03.2020
    Github: https://github.com/RafalUzarowicz
"""


class Anthill:
    class Ant:
        def __init__(self):
            self.path = []

    def __init__(self, ants_num: int):
        if ants_num <= 0:
            raise ValueError
        self.ants = [self.Ant() for i in range(ants_num)]
