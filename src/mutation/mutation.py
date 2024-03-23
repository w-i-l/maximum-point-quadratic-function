from src.cromosome import Cromosome
from src.base_class import BaseClass
from numpy import random

class Mutator(BaseClass):
    def __init__(
        self: object,
        population: list[Cromosome],
        mutation_rate: float,
    ):
        self.population = population
        self.mutation_rate = mutation_rate
        super().__init__()

    def mutate(self: object) -> list[Cromosome]:
        for c in self.population:
            if self.__should_mutate():
                if self.should_print:
                    print(f'Mutating {c.id}')
                self.__mutate_cromozom(c)
        return self.population
    
    def __generate_random_number(self: object) -> float:
        return random.uniform(0, 1)
    
    def __should_mutate(self: object) -> bool:
        return self.__generate_random_number() < self.mutation_rate
    
    def __mutate_cromozom(self: object, c: Cromosome) -> None:
        point = random.randint(0, len(c.binary) - 1)
        changed_bit = '0' if c.binary[point] == '1' else '1'
        new_c = c.binary[:point] + changed_bit + c.binary[point + 1:]
        c.update_binary(new_c)
        if self.should_print:
            print(f'Mutated {c.id} at point {point}')
