import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
from src.cromosome import Cromosome
from src.codification import coder
from src.selection.selector import Selector
from src.combination.combination import Combinator
from src.mutation.mutation import Mutator
from src.gui.GUI import GUI
import random

if __name__ == '__main__':
    population_size = 20
    generations = 100
    lower_bound = -1
    upper_bound = 2
    precision = 6
    f = lambda x: -(x ** 2) + x + 2
    combination_rate = 0.25
    mutation_rate = 0.05

    values = [round(random.uniform(lower_bound, upper_bound), precision) for _ in range(population_size)]
    coder = coder.Coder(lower_bound, upper_bound, precision)
    binaries = [coder.encoder.encode(x)for x in values]
    fitnesses = [f(x) for x in values]
    Cromosome.init(coder, f)
    population = [Cromosome(values[i], binaries[i], fitnesses[i]) for i in range(len(values))]

    selector = Selector(population)
    combinator = Combinator(population, combination_rate)
    mutator = Mutator(population, mutation_rate)

    SEPARATOR = '----------------------------------------\n'

    print('Initial population:\n')
    for c in population:
        c.show()
    print(SEPARATOR)

    population = selector.select()
    print('\nSelected population:\n')
    for c in population:
        c.show()
    print(SEPARATOR)

    print(f'Combination rate: {combination_rate}\n')
    population = combinator.combine()

    print('\nAfter combination:\n')
    for c in population:
        c.show()
    print(SEPARATOR)

    print(f'Mutation rate: {mutation_rate}\n')
    population = mutator.mutate()

    print('\nAfter mutation:\n')
    for c in population:
        c.show()
    print(SEPARATOR)

    coder.should_print = False
    selector.should_print = False
    combinator.should_print = False
    mutator.should_print = False

    print('\n\n\n')
    for i in range(generations):
        selected = selector.select()
        population = combinator.combine()
        population = mutator.mutate()
        print(max([c.fitness for c in population]))

