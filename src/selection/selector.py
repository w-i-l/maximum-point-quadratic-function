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
        selected = [self.__get_the_best_cromozom()]
        if self.should_print:
            self.__print_cromosomes_probabilities()
            print()
            self.__print_intervals()
            print()
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
        low = 0
        high = len(self.intervals) - 1

        while low <= high:
            mid = (low + high) // 2
            if self.intervals[mid] <= number < self.intervals[mid + 1]:
                return mid
            elif number < self.intervals[mid]:
                high = mid - 1
            else:
                low = mid + 1

        return -1
        
    def __select_cromozom(self: object) -> Cromosome:
        number = self.__generate_random_number()
        index = self.__get_index_of_interval(number)
        if self.should_print:
            print(f'u= {number} selected {self.population[index]}')
        return self.population[index]

    def __print_cromosomes_probabilities(self: object):
        print('Selection probabilities:')
        for c in self.population:
            print(f'Probability for {c}: {self.__get_probability_for_cromozom(c)}')
    
    def __print_intervals(self: object):
        print('Intervals:')
        for i in range(len(self.intervals) - 1):
            print(f'Interval {i}: {self.intervals[i]} - {self.intervals[i + 1]}')

    def __get_the_best_cromozom(self: object) -> Cromosome:
        return max(self.population, key=lambda c: c.fitness)