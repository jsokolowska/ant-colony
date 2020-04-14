from src.anthill import Anthill
from src.pheromone_update import pheromone_update


def local_search(anthill: Anthill, percentage=0.5):
    if percentage < 0 or percentage > 1:
        raise ValueError("Percentage must be between 0 and 1")
    if anthill is None:
        raise TypeError("No anthill given")
