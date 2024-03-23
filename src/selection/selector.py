from cromosome import Cromosome
from src.codification.coder import Coder
from src.base_class import BaseClass
from numpy import random

class Selector(BaseClass):
    def __init__(
            self: object, 
            population: list[Cromosome],
        ):
        self.population = population
        self.intervals = self.__get_probability_intervals()
        super().__init__()

    def select(self: object) -> list[Cromosome]:
        selected = []
        if self.should_print:
            print('Intervals:')
            for index, interval in enumerate(self.intervals):
                print(f'Interval {index}: {interval}')
        while len(selected) < len(self.population):
            selected.append(self.__select_cromozom())
        return selected
        
    def __get_total_fitness(self: object) -> float:
        return sum([c.fitness for c in self.population])

    def __get_probability_for_cromozom(self: object, c: Cromosome) -> float:
        return c.fitness / self.__get_total_fitness()

    def __get_probability_intervals(self: object) -> list[float]:
        probabilities = [self.__get_probability_for_cromozom(c) for c in self.population]
        intervals = [0]
        for i in range(len(probabilities)):
            intervals.append(intervals[i] + probabilities[i])
        return intervals
    
    def __generate_random_number(self: object) -> float:
        return random.uniform(0, 1)
    
    def __get_index_of_interval(self: object, number: float) -> int:
        for i in range(len(self.intervals) - 1):
            if self.intervals[i] <= number < self.intervals[i + 1]:
                return i
        return -1
        
    def __select_cromozom(self: object) -> Cromosome:
        number = self.__generate_random_number()
        index = self.__get_index_of_interval(number)
        if self.should_print:
            print(f'Selected index: {index}')
        return self.population[index]

