import numpy as np
import random
import warnings


class Selection:
    """
        Class that performs the selection over the whole population
        Attributes
        ----------
        population: list
                    the list that contains all the Chromosomes that make up the population
        selection_method: str
                          the method that we can use to perform the selection of the parents, it can be "roulette_wheel",
                          "stochastic_universal_sampling", "tournament", "rank" or "random"
        reproduction_rate: flaat
                           the rate at which the population reproduces itself, the number of children is equal to number
                           of chromosome in the generation * reproduction_rate
        Methods
        -------
        Private:
        self._roulette_wheel_selection(): it performs the roulette wheel selection on the population to get the parents
        self._stochastic_universal_sampling(): it performs the stochastic universal sampling selection on the
                                               population to get the parents
        self._tournament_selection(tournament_size): it performs the tournament selection on the population
                                                     to get the parents
        self._rank_selection(): it performs the rank selection on the population to get the parents
        self._random_selection(): it performs the random selection on the population to get the parents
        self._get_subset_sum(gene_num): it adds up the total fitness of the population up to the gene_num specified
        Public:
            self.perform_selection(tournament_size): it performs the selection by feeding the parents to the
                                                    previously specified selection method
    """

    def __init__(self, selection_method: str, population: list, reproduction_rate: float) -> None:
        self.selection_method = selection_method
        self.population = population
        self.reproduction_rate = reproduction_rate
        self.n_parents: int = int(len(self.population) * self.reproduction_rate)

    def perform_selection(self, tournament_size: int = None) -> np.array:
        """
        it performs the selection by feeding the parents to the previously specified selection method
        Parameters
        ----------
        tournament_size: int
                         the size of the tournament that we use for the "tournament" selection
        Returns
        -------
        np.array
        an array that contains the selected parents for the reproduction
        """
        if self.selection_method == "roulette_wheel":
            parents = self._roulette_wheel_selection()
        elif self.selection_method == "stochastic_universal_sampling":
            parents = self._stochastic_universal_sampling()
        elif self.selection_method == "tournament":
            if tournament_size is None:
                raise ValueError("We need a valid tournament_size for this method")
            parents = self._tournament_selection(tournament_size=tournament_size)
        elif self.selection_method == "rank":
            parents = self._rank_selection()
        elif self.selection_method == "random":
            parents = self._random_selection()
        else:
            raise ValueError("The selection method specified is not implemented \n"
                             "Please specify a valid selection method ")

        return parents

    def _roulette_wheel_selection(self) -> np.array:
        """
        it performs the roulette wheel selection on the population to get the parents
        Returns
        -------
        np.array
        an array that contains the selected parents for the reproduction
        """
        all_parents = []
        while len(all_parents) < self.n_parents:

            population_fitness = sum([chromosome.fitness for chromosome in self.population])

            chromosome_probabilities = [chromosome.fitness / population_fitness for chromosome in self.population]

            all_parents.append(np.random.choice(self.population, p=chromosome_probabilities))

        return np.array(all_parents)

    def _stochastic_universal_sampling(self) -> np.array:
        """
        it performs the stochastic universal sampling selection on the population to get the parents
        Returns
        -------
        np.array
        an array that contains the selected parents for the reproduction
        """
        total_fitness = sum([chromosome.fitness for chromosome in self.population])
        point_distance = total_fitness / self.n_parents
        start_point = random.uniform(0, point_distance)
        points = [start_point + i * point_distance for i in range(self.n_parents)]

        parents = set()
        while len(parents) < self.n_parents:
            random.shuffle(self.population)
            n_rounds = 0
            while n_rounds < len(points) and len(parents) < self.n_parents:
                for gene_num in range(len(self.population)):
                    if self._get_subset_sum(gene_num) > points[n_rounds]:
                        parents.add(self.population[gene_num])
                        break
                n_rounds += 1

        return np.array(parents)

    def _get_subset_sum(self, gene_num: int) -> float:
        """
        it adds up the total fitness of the population up to the gene_num specified
        Parameters
        ----------
        gene_num: the position up to which to sum the fitness for the population

        Returns
        -------
        float
        the total fitness for the population up to gene num
        """
        subset_sum = 0.0
        i = 0

        while i <= gene_num:
            subset_sum += self.population[i].fitness
            i += 1
        return subset_sum

    def _tournament_selection(self, tournament_size=4):
        """
        it performs the tournament selection on the population to get the parents
        Parameters
        ----------
        tournament_size: int
                         the size of the tournament that we use for the tournament selection

        Returns
        -------
        np.array
        an array that contains the selected parents for the reproduction
        """
        all_parents = []
        while len(all_parents) < self.n_parents:
            parents = random.choices(self.population, k=tournament_size)
            parents = sorted(parents, key=lambda gene: gene.fitness, reverse=True)
            all_parents.append(parents[0])

        return np.array(all_parents)

    def _rank_selection(self):
        """
        it performs the rank selection on the population to get the parents
        Returns
        -------
        np.array
        an array that contains the selected parents for the reproduction
        """
        parents = sorted(self.population, key=lambda gene: gene.fitness, reverse=True)
        best_parents = parents[:self.n_parents]

        random.shuffle(best_parents)

        return np.array(best_parents)

    def _random_selection(self):
        """
        it performs the random selection on the population to get the parents
        Returns
        -------
        np.array
        an array that contains the selected parents for the reproduction
        """
        warnings.warn("The random selections leads to a stochastic search for the parameters")
        parents = random.choices(self.population, k=self.n_parents)

        return np.array(parents)
