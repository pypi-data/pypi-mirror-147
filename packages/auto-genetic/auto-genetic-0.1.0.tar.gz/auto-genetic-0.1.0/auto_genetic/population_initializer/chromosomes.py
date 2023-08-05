from __future__ import annotations

from auto_genetic.population_initializer.hyperparams_setter import HyperParamsSetter
from auto_genetic.population_initializer.feature_setter import FeatureSetter
from auto_genetic.evaluation.fitnessfuncsetter import FitnessFuncSetter
from typing import List


class Chromosome:
    """
    Chromosome class, that contains the sequence, the hyperparameters and the fitness of its linked program run
    Attributes
    ----------
    algo_type: str
               can be "hyperparameter_tuning" or "feature_selection", it represents what is the purpose of the GA
    hyperparams_dict: List[dict, dict]
                      a list that contains 2 dictionaries, one with the hyperparameters' types and another with the
                      hyperparameters' values
    feature_num: int
                 the number of features from which to select
    sequence: list
              the list of the values of the chromosome's gene
    hyperparams: dict
                 the dictionary that contains the hyperparameters linked to this specific Chromosome
    fitness: float
             the fitness of the chromosome


    Methods
    -------
    Private:
        self._initialize_hyperparams(): it sets the sequence of the chromosome given the set of hyperparameters
        self._initialize_features(): it sets the sequence of the chromosome given the number of features
    Public:
        self.initialize(): method that initializes the sequence of the chromosome according to the algo_type
        self.set_fitness_function(fitness_function_initialised): method that sets the fitness function for the
                                                                 chromosome
        self.calculate_fitness(): method that uses the previously set fitness function to calculate the fitness for
                                  this specific chromosome
    """
    def __init__(self, algo_type: str, hyperparams_dict: List[dict, dict] = None, feature_num: int = None) -> None:
        self.fitness = None
        self.fitness_function = None
        self.algo_type = algo_type
        if self.algo_type == "hyperparameter_tuning" and hyperparams_dict is None:
            raise ValueError("We don't have any hyerparameters to tune!!")

        elif self.algo_type == "feature_selection" and feature_num is None:
            raise ValueError("What's the number of features you want to tune?")

        self.hyperparams_dict = hyperparams_dict
        self.feature_num = feature_num
        self.hyperparams = None
        self.sequence = None
        self.hyperparams_map = None
        self.features = None

    def initialize(self) -> Chromosome:
        """
        method that initializes the sequence of the chromosome according to the algo_type
        Returns
        -------
        Chromosome
        it returns the class itself, so it can be used inline
        """
        if self.algo_type == "hyperparameter_tuning":
            self._initialize_hyperparams()
        elif self.algo_type == "feature_selection":
            self._initialize_feature()

        return self

    def set_fitness_function(self, fitness_function_initialised: FitnessFuncSetter) -> None:
        """
        method that sets the fitness function for the chromosome
        Parameters
        ----------
        fitness_function_initialised: FitnessFuncSetter
                                      The initialised fitness function that contains the program to run

        """
        self.fitness_function = fitness_function_initialised

    def calculate_fitness(self):
        """
        method that uses the previously set fitness function to calculate the fitness for this specific chromosome
        """
        if self.fitness:
            return self.fitness
        else:
            self.fitness = self.fitness_function.calculate_fitness()

    def _initialize_hyperparams(self) -> None:
        """
        it sets the sequence of the chromosome given the set of hyperparameters
        """
        setter = HyperParamsSetter(self.hyperparams_dict, self.algo_type).get_hyperparameters()
        self.sequence = setter.convert_hyperparams_values()
        self.hyperparams, self.hyperparams_map = setter.get_program_hyperparams()

    def _initialize_feature(self) -> None:
        """
        it sets the sequence of the chromosome given the number of features
        """
        setter = FeatureSetter(self.algo_type, self.feature_num)
        self.sequence = setter.set_feature_sequence()
