import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
from src.cromosome import Cromosome
from src.codification import coder
from src.selection.selector import Selector
from src.combination.combination import Combinator
from src.mutation.mutation import Mutator

if __name__ == '__main__':
    values = [
        -0.914592,
        -0.516787,
        -0.246207,
        1.480791,
        0.835307,
        1.229633,
        0.133068,
        -0.897179,
        0.100578,
        -0.311975,
        1.411980,
        0.404924,
        1.954865,
        0.359503,
        1.255452,
        1.124764,
        1.527482,
        1.573845,
        -0.562311,
        1.191435
    ]
    lower_bound = -1
    upper_bound = 2
    precision = 6
    f = lambda x: -(x ** 2) + x + 2
    combination_rate = 0.25
    mutation_rate = 0.1
    coder = coder.Coder(lower_bound, upper_bound, precision)
    binaries = [coder.encoder.encode(x)for x in values]
    fitnesses = [f(x) for x in values]
    Cromosome.init(coder, f)
    population = [Cromosome(values[i], binaries[i], fitnesses[i]) for i in range(len(values))]

    selector = Selector(population)
    combinator = Combinator(population, combination_rate)
    mutator = Mutator(population, mutation_rate)

    print('Initial population:')
    for c in population:
        c.show()
    
    selected = selector.select()

    print('\nSelected population:')
    for c in selected:
        c.show()
    population = selected

    print(f'Combination rate: {combination_rate}')
    population = combinator.combine()

    print('\nAfter combination:')
    for c in population:
        c.show()

    print(f'Mutation rate: {mutation_rate}')
    population = mutator.mutate()

    print('\nAfter mutation:')
    for c in population:
        c.show()

    print('\n\n\n')
    for i in range(49):
        selected = selector.select()
        population = combinator.combine()
        population = mutator.mutate()
        print(max([c.fitness for c in population]))