from src.cromosome import Cromosome
from numpy import random
from src.base_class import BaseClass
import random

class Combinator(BaseClass):
    def __init__(
        self: object,
        population: list[Cromosome],
        combination_rate: float,
    ):
        self.population = population
        self.combination_rate = combination_rate
        super().__init__()

    def combine(self: object) -> list[Cromosome]:
        for c1, c2 in self.__get_possible_combinations():
            self.__mix_cromozoms(c1, c2)
        return self.population

    def __mix_cromozoms(self: object, c1: Cromosome, c2: Cromosome) -> None:
        point = random.randint(0, len(c1.binary) - 1)
        new_c1 = c1.binary[:point] + c2.binary[point:]
        new_c2 = c2.binary[:point] + c1.binary[point:]
        c1.update_binary(new_c1)
        c2.update_binary(new_c2)
        if self.should_print:
            print(f'Combined {c1.id} with {c2.id} at point {point}')
            print(f'Result: {new_c1} {new_c2}')

    def __get_cromosomes_for_combination(self: object) -> list[Cromosome]:
        return [c for c in self.population if self.__should_combine()]
    
    def __generate_random_number(self: object) -> float:
        return random.uniform(0, 1)
    
    def __should_combine(self: object) -> bool:
        return self.__generate_random_number() < self.combination_rate
    
    def __get_possible_combinations(self: object) -> list[tuple[Cromosome, Cromosome]]:
        cromosomes = self.__get_cromosomes_for_combination()
        if len(cromosomes) % 2 != 0:
            cromosomes.pop()
        random.shuffle(cromosomes)

        result = []
        while cromosomes:
            first = cromosomes.pop()
            second = cromosomes.pop()
            result.append((first, second))
        return result
