import random
from auto_genetic.population_initializer.chromosomes import Chromosome


class Darwinism:
    """
    Class that performs the reproduction over the whole population
    Attributes
    ----------
    population: list
                the list that contains all the Chromosomes that make up the population
    reproduction_rate: flaat
                       the rate at which the population reproduces itself, the number of children is equal to number
                       of chromosome in the generation * reproduction_rate
    Methods
    -------
    self.discard_worst_performers(): it eliminates the chromosomes with the worst fitness from the generation
    """
    def __init__(self, population: list, reproduction_rate: float) -> None:
        self.population = population
        self.reproduction_rate = reproduction_rate
        self.best_chromosome = None

    def discard_worst_performers(self) -> tuple[list, Chromosome]:
        """
        it eliminates the chromosomes with the worst fitness from the generation
        Returns
        -------
        tuple[list, Chromosome]
        a tuple that contains the population without the worst performers and the best_chromosome in the population
        """
        keep_number = int(len(self.population) * (1 - self.reproduction_rate))

        self.population.sort(key=lambda chromosome: chromosome.fitness, reverse=True)
        self.population = self.population[:keep_number]
        self.best_chromosome = self.population[0]
        random.shuffle(self.population)

        return self.population, self.best_chromosome
