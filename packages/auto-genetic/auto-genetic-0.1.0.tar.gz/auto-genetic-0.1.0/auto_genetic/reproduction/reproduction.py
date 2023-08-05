import numpy as np
from auto_genetic.reproduction.crossover import CrossOver
from auto_genetic.reproduction.mutation import Mutation
from auto_genetic.reproduction.translation import Translation
from auto_genetic.reproduction.selection import Selection
from auto_genetic.population_initializer.chromosomes import Chromosome


class Reproduction:
    """
    Class that performs the reproduction over the whole population
    Attributes
    ----------
    population: list
                the list that contains all the Chromosomes that make up the population
    crossover_method: str
                      the methods that we can use to perform the crossover, it can be "single_point_split",
                      "two_point_split" or "uniform"
    prob_crossover: float
                    the probability that the crossover is performed, by default it's equal to 1, so the crossover
                    will always be applied
    hyperparams_types: dict
                       a dictionary that has the names of the hyperparameters as keys and the hyperparameter types as
                       values, this can either be "continuous" or "categorical"
    mutation_method: str
                      the methods that we can use to perform the mutation, it can be "bit_flip", "random",
                      "swap", "scramble" or "inversion"
    prob_mutation: float
                    the probability that the mutation is performed
    prob_translation: float
                      the probability that the translation is performed
    selection_method: str
                      the method that we can use to perform the selection of the parents, it can be "roulette_wheel",
                      "stochastic_universal_sampling", "tournament", "rank" or "random"
    reproduction_rate: flaat
                       the rate at which the population reproduces itself, the number of children is equal to number
                       of chromosome in the generation * reproduction_rate
    tournament_size: int
                     the size of the tournament that we use for the "tournament" selection
    Methods
    -------
    self.crossover(parent_1, parent_2): it uses the Crossover class on 2 Chromosomes and performs the crossover
    self.mutation(child): it uses the Mutation class on a Chromosome and performs the mutation
    self.translation(child): it uses the Translation class on a Chromosome and performs the translation
    self.selection(): it uses the Selection class on the population and it selects the parents for the next generation
    self.reproduction(): it puts together all the steps necessary for the reproduction and generates the children that
                         will be added to the population
    """
    def __init__(self, population: np.array = None, crossover_method: str = "single_point_split",
                 prob_crossover: float = 1, hyperparams_types: dict = None, mutation_method: str = "bit_flip",
                 prob_mutation: float = 0.3,
                 prob_translation: float = 0.1, selection_method: str = "roulette_wheel",
                 reproduction_rate: float = 0.2, tournament_size: int = 4) -> None:
        self.prob_crossover = prob_crossover
        self.crossover_method = crossover_method
        self.prob_mutation = prob_mutation
        self.prob_translation = prob_translation
        self.reproduction_rate = reproduction_rate
        self.hyperparams_types = hyperparams_types
        self.population = population
        self.selection_method = selection_method
        self.tournament_size = tournament_size
        self.mutation_method = mutation_method

    def crossover(self, parent_1: Chromosome, parent_2: Chromosome) -> tuple[Chromosome, Chromosome]:
        """
        it uses the Crossover class on 2 Chromosomes and performs the crossover
        Parameters
        ----------
        parent_1: Chromosome
                  one of the chromosomes selected to become parents by the selection algorithm
        parent_2: Chromosome
                  one of the chromosomes selected to become parents by the selection algorithm

        Returns
        -------
        tuple[Chromosome, Chromosome]
        a tuple containing the 2 children, obtained by performing crossover
        """
        child1, child2 = CrossOver(self.crossover_method).perform_crossover(parent_1=parent_1, parent_2=parent_2)

        return child1, child2

    def mutation(self, child: Chromosome) -> Chromosome:
        """
        it uses the Mutation class on a Chromosome and performs the mutation
        Parameters
        ----------
        child: Chromosome
                the chromosome that contains the sequence over which to apply the mutation

        Returns
        -------
        Chromosome
        the previous chromosome but with a mutated sequence
        """
        mutated_child = Mutation(self.mutation_method, self.hyperparams_types,
                                 self.prob_mutation).perform_mutation(child)

        return mutated_child

    def translation(self, child: Chromosome) -> Chromosome:
        """
        it uses the Translation class on a Chromosome and performs the translation
        Parameters
        ----------
        child: Chromosome
               the chromosome that contains the sequence over which to apply the translation


        Returns
        -------
        Chromosome
        the previous chromosome but with a translated sequence
        """
        translated_child = Translation(self.prob_translation).perform_translation(child)

        return translated_child

    def selection(self) -> np.array:
        """
        it uses the Selection class on the population and it selects the parents for the next generation
        Returns
        -------
        np.array
        an array that contains the selected parents for the reproduction
        """
        parents = Selection(self.selection_method, self.population,
                            self.reproduction_rate).perform_selection(tournament_size=self.tournament_size)

        return parents

    def reproduction(self) -> list:
        """
        it puts together all the steps necessary for the reproduction and generates the children that
        will be added to the population
        Returns
        -------
        list
        the list of all the children that have been created during the reproduction
        """
        parents = self.selection()
        children = []

        for i in range(0, len(parents), 2):
            parent_1, parent_2 = parents[i], parents[i + 1]
            child_1, child_2 = self.crossover(parent_1, parent_2)
            child_1, child_2 = self.mutation(child_1), self.mutation(child_2)
            child_1, child_2 = self.translation(child_1), self.translation(child_2)
            children.append(child_1)
            children.append(child_2)

        return children
