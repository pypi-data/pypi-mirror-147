import numpy as np
import random
from auto_genetic.population_initializer.chromosomes import Chromosome
from copy import deepcopy


class Mutation:
    """
    Class that performs the crossover on the parents to get the children
    Attributes
    ----------
    mutation_method: str
                      the methods that we can use to perform the mutation, it can be "bit_flip", "random",
                      "swap", "scramble" or "inversion"
    prob_mutation: float
                    the probability that the mutation is performed
    hyperparams_types: dict
                       a dictionary that has the names of the hyperparameters as keys and the hyperparameter types as
                       values, this can either be "continuous" or "categorical"
    Methods
    -------
    Private:
        self._bit_flip_mutation(chromosome): it performs the bit flip mutation on the selected chromosome
        self._random_resetting_mutation(chromosome): it performs the random resetting mutation on the selected
                                                     chromosome
        self._swap_mutation(chromosome): it performs the swap mutation on the selected chromosome
        self._scramble_mutation(chromosome): it performs the scramble mutation on the selected chromosome
        self._inversion_mutation(chromosome): it performs the inversion mutation on the selected chromosome
        self._random_categorical(chromosome): it chooses a new random value for the value that needs to be mutated
                                              amongst the possible one for the specified categorical parameter
        self._random_continuous(chromosome): it chooses a new random value for the value that needs to be mutated
                                             amongst the possible one for the specified continuous parameter

    Public:
        self.perform_mutation(chromosome): it performs the mutation by feeding the chromosome to the
                                            previously specified mutation method
    """
    def __init__(self, mutation_method: str, hyperparams_types: dict, prob_mutation: float) -> None:
        self.mutation_method = mutation_method
        self.prob_mutation = prob_mutation
        self.hyperparams_types = hyperparams_types
        self.hyperparams_map = None

    def perform_mutation(self, chromosome: Chromosome) -> Chromosome:
        """
        it performs the mutation by feeding the chromosome to the previously specified mutation method
        Parameters
        ----------
        chromosome: Chromosome
                    the chromosome that contains the sequence over which to apply the mutation

        Returns
        -------
        Chromosome
        the previous chromosome but with a mutated sequence
        """
        self.hyperparams_map = deepcopy(chromosome.hyperparams_map)
        if self.mutation_method == "bit_flip":
            mutated_gene = self._bit_flip_mutation(chromosome)

        elif self.mutation_method == "random":
            mutated_gene = self._random_resetting_mutation(chromosome)

        elif self.mutation_method == "swap":
            mutated_gene = self._swap_mutation(chromosome)

        elif self.mutation_method == "scramble":
            mutated_gene = self._scramble_mutation(chromosome)

        elif self.mutation_method == "inversion":
            mutated_gene = self._inversion_mutation(chromosome)

        else:
            raise ValueError("the mutation method specified is not implemented")

        mutated_gene.fitness = None

        return mutated_gene

    def _bit_flip_mutation(self, chromosome: Chromosome) -> np.array:
        """
        it performs the bit flip mutation on the selected chromosome
        Parameters
        ----------
        chromosome: Chromosome
                    the chromosome that contains the sequence over which to apply the bit flip mutation

        Returns
        -------
        Chromosome
        the previous chromosome but with a mutated sequence
        """
        to_be_mutated = np.random.rand(*chromosome.sequence.shape) <= self.prob_mutation
        mutation_index = np.argwhere(to_be_mutated)
        mutated_gene = deepcopy(chromosome)

        for i in mutation_index:
            if mutated_gene.sequence[i] == 0:
                mutated_gene.sequence[i] = 1
            else:
                mutated_gene.sequence[i] = 1

        return mutated_gene

    def _random_resetting_mutation(self, chromosome: Chromosome) -> Chromosome:
        """
        it performs the random resetting mutation on the selected chromosome
        Parameters
        ----------
        chromosome: Chromosome
                    the chromosome that contains the sequence over which to apply the random resetting mutation

        Returns
        -------
        Chromosome
        the previous chromosome but with a mutated sequence
        """
        to_be_mutated = np.random.rand(*chromosome.sequence.shape) <= self.prob_mutation
        mutation_index = np.argwhere(to_be_mutated).flatten()
        mutated_gene = deepcopy(chromosome)

        for i in mutation_index:
            param = list(self.hyperparams_map.keys())[i]
            if self.hyperparams_types[param] == "continuous":
                choice = self._random_continuous(param)

            else:
                choice = self._random_categorical(param)

            mutated_gene.sequence[i] = choice

        return mutated_gene

    def _swap_mutation(self, chromosome: Chromosome) -> Chromosome:
        """
        it performs the swap mutation on the selected chromosome
        Parameters
        ----------
        chromosome: Chromosome
                    the chromosome that contains the sequence over which to apply the swap mutation

        Returns
        -------
        Chromosome
        the previous chromosome but with a mutated sequence
        """
        to_be_swapped = np.random.rand(*chromosome.sequence.shape) <= self.prob_mutation
        swapped_index = np.argwhere(to_be_swapped)
        if swapped_index % 2 == 1:
            swapped_index = np.random.choice(swapped_index, size=len(swapped_index)-1, replace=False)

        mutated_gene = deepcopy(chromosome)

        for i in range(0, len(swapped_index), 2):
            mutated_gene.sequence[swapped_index[i]], mutated_gene.sequence[swapped_index[i + 1]] = \
                mutated_gene.sequence[swapped_index[i]], mutated_gene.sequence[swapped_index[i + 1]]

        return mutated_gene

    def _scramble_mutation(self, chromosome: Chromosome) -> Chromosome:
        """
        it performs the scramble mutation on the selected chromosome
        Parameters
        ----------
        chromosome: Chromosome
                    the chromosome that contains the sequence over which to apply the scramble mutation

        Returns
        -------
        Chromosome
        the previous chromosome but with a mutated sequence
        """
        prob = np.random.rand()
        mutated_child = deepcopy(chromosome)
        if prob <= self.prob_mutation:
            index_1 = random.randint(0, len(chromosome.sequence))
            index_2 = random.randint(index_1, len(chromosome.sequence))

            mutated_child.sequence = np.hstack([mutated_child.sequence[:index_1],
                                               random.shuffle(mutated_child.sequence[index_1:index_2]),
                                               mutated_child.sequence[index_2:]])

        return mutated_child

    def _inversion_mutation(self, chromosome: Chromosome) -> Chromosome:
        """
        it performs the inversion mutation on the selected chromosome
        Parameters
        ----------
        chromosome: Chromosome
                    the chromosome that contains the sequence over which to apply the inversion mutation

        Returns
        -------
        Chromosome
        the previous chromosome but with a mutated sequence
        """
        prob = np.random.rand()
        mutated_child = deepcopy(chromosome)
        if prob <= self.prob_mutation:
            index_1 = random.randint(0, len(chromosome.sequence))
            index_2 = random.randint(index_1, len(chromosome.sequence))

            mutated_child.sequence = np.hstack([mutated_child.sequence[:index_1],
                                               mutated_child.sequence[index_1:index_2][::-1],
                                               mutated_child.sequence[index_2:]])

        return mutated_child

    def _random_categorical(self, param: str) -> int:
        """
        it chooses a new random value for the value that needs to be mutated amongst the possible one for the
        specified categorical parameter
        Parameters
        ----------
        param: str
               the name of the parameter that we will choose a random value for

        Returns
        -------
        int
        the new value for the parameter chosen
        """
        values = self.hyperparams_map[param][0]
        choice = np.random.choice(values)

        return choice

    def _random_continuous(self, param: str) -> float:
        """
        it chooses a new random value for the value that needs to be mutated amongst the possible one for the
        specified continuous parameter
        Parameters
        ----------
        param: str
               the name of the parameter that we will choose a random value for

        Returns
        -------
        float
        the new value for the parameter chosen
        """
        values = self.hyperparams_map[param]
        choice = random.uniform(values[0], values[1])

        return choice
