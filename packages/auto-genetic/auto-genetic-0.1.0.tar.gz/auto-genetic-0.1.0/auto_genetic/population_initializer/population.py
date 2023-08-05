from auto_genetic.population_initializer.chromosomes import Chromosome
from typing import List


class PopulationInitializer:
    """
    Class used to initialize the population, made of chromosomes
    Attributes
    ----------
    pop_size: int
              the number of chromosomes we want in our population
    algo_type: str
               can be "hyperparameter_tuning" or "feature_selection", it represents what is the purpose of the GA
    hyperparams_dict: List[dict, dict]
                      a list that contains 2 dictionaries, one with the hyperparameters' types and another with the
                      hyperparameters' values
    feature_num: int
                 the number of features from which to select


    Methods
    -------
        self.initialize_population(): method that uses the Chromosome class to generate n (= pop_size) Chromosomes
    """
    def __init__(self, pop_size: int, algo_type: str, hyperparams_dict: list = None, feature_num: int = None) -> None:
        self.population = []
        self.algo_type = algo_type
        self.hyperparams_dict = hyperparams_dict
        self.feature_num = feature_num
        self.pop_size = pop_size

    def initialize_population(self) -> List[Chromosome]:
        """
        method that uses the Chromosome class to generate n (= pop_size) Chromosomes
        Returns
        -------
        List[Chromosome]
        a list that contains all the chromosomes for the first generation

        """
        for _ in range(self.pop_size):
            chromosome = Chromosome(self.algo_type, hyperparams_dict=self.hyperparams_dict,
                                    feature_num=self.feature_num).initialize()

            self.population.append(chromosome)

        return self.population
