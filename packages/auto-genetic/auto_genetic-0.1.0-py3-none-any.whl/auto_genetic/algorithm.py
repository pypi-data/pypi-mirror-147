from typing import Iterable

from tqdm import tqdm
import pandas as pd

from auto_genetic.reproduction.reproduction import Reproduction
from auto_genetic.evaluation.evaluator import Evaluator
from auto_genetic.darwinism import Darwinism
from auto_genetic.population_initializer.chromosomes import Chromosome
from auto_genetic.population_initializer.population import PopulationInitializer
from sklearn.model_selection import train_test_split


class GeneticAlgorithm:
    """
    Class that runs the genetic algorithm for the specified program
    Attributes
    ----------
    program: class
        the user defined program that has the run() and predict() methods
    data: pd.DataFrame
          a pandas dataframe that contains the data for the program, including the target
    target_column: str
                   the name of the column that is used as target for the evaluation
    test_size: float
              the size of the test data for the testing of the chromosomes
    data_split: str
                it chooses if we want to split the data one time for all the generations or for each generation,
                it can take the values "single" or "multiple"
    algo_type: str
               can be "hyperparameter_tuning" or "feature_selection", it represents what is the purpose of the GA
    pop_size: int
              the number of chromosomes we want to have in each generation
    number_gen: int
                the number of generations we want the program to run for
    hyperparams_dict: List[dict, dict]
                      a list that contains 2 dictionaries, one with the hyperparameters' types and another with the
                      hyperparameters' values
    feature_num: int
                the number of features that the feature_selection algorithm can select from
    max_fitness_value: float
                       the maximum value that we want our fitness to take, if it gets higher the algorithm stops
    prob_crossover: float
                    the probability that the crossover is performed, by default it's equal to 1, so the crossover
                    will always be applied
    crossover_method: str
                      the methods that we can use to perform the crossover, it can be "single_point_split",
                      "two_point_split" or "uniform"
    mutation_method: str
                      the methods that we can use to perform the mutation, it can be "bit_flip", "random",
                      "swap", "scramble" or "inversion"
    prob_mutation: float
                    the probability that the mutation is performed
    prob_translation: float
                      the probability that the translation is performed
   reproduction_rate: flaat
                       the rate at which the population reproduces itself, the number of children is equal to number
                       of chromosome in the generation * reproduction_rate
    tournament_size: int
                     the size of the tournament that we use for the "tournament" selection
    selection_method: str
                      the method that we can use to perform the selection of the parents, it can be
                      "roulette_wheel", "stochastic_universal_sampling", "tournament", "rank" or "random"

    Methods
    -------
    self.initialize_population(): method that uses the Chromosome class to generate n (= pop_size) Chromosomes,
                                  passing by the PopulationInitializer class
    self.split_data(): Method that defines the train and test datasets
    self.set_evaluation_method(evaluation_method, custom_fitness_function): Method that sets the fitness function
                                                                            for the program
    self.evaluate_generation(): Method to evaluate the full generation by finding the fitness for every member of
                                the generation
    self.reproduction(): it puts together all the steps necessary for the reproduction and generates the children
                         that will be added to the population
    self.darwinism(): it eliminates the chromosomes with the worst fitness from the generation, to make space
                      for the children
    self.run(): run the genetic algorithm for n generation with m genes, storing the best score and the best gene
    """
    def __init__(self, program, data: pd.DataFrame, target_column: str, test_size: float = 0.2,
                 data_split: str = "single", algo_type: str = "hyperparameter_tuning", pop_size: int = 100,
                 number_gen: int = 20, hyperparams_dict: list[dict, dict] = None, feature_num: int = None,
                 max_fitness_value: float = None,
                 prob_crossover: float = 1.0, crossover_method: str = "single_point_split",
                 mutation_method: str = "bit_flip", prob_mutation: float = 0.3, prob_translation: float = 0.1,
                 reproduction_rate: float = 0.2, selection_method: str = "roulette_wheel", tournament_size: int = 4):

        self.algo_type = algo_type
        self.pop_size = pop_size
        self.number_gen = number_gen
        self.max_fitness_value = max_fitness_value
        self.prob_crossover = prob_crossover
        self.crossover_method = crossover_method
        self.prob_mutation = prob_mutation
        self.prob_translation = prob_translation
        self.reproduction_rate = reproduction_rate
        self.mutation_method = mutation_method
        self.hyperparams_dict = hyperparams_dict
        if self.hyperparams_dict:
            self.hyperparams_names = self.hyperparams_dict[0].keys()
            self.hyperparams_values = self.hyperparams_dict[1]
            self.hyperparams_types = self.hyperparams_dict[0]
        else:
            self.hyperparams_names = None
            self.hyperparams_values = None
            self.hyperparams_types = None
        self.population = None
        self.selection_method = selection_method
        self.best_chromosome = None
        self.tournament_size = tournament_size
        self.evaluation_method = None
        self.program = program
        self.target = target_column
        self.train_data = None
        self.test_data = None
        self.custom_fitness_function = None
        self.feature_num = feature_num
        self.data = data
        self.test_size = test_size
        self.data_split = data_split

    def initialize_population(self) -> None:
        """
        method that uses the Chromosome class to generate n (= pop_size) Chromosomes, passing by the
        PopulationInitializer class
        """
        self.population = PopulationInitializer(self.pop_size, self.algo_type, hyperparams_dict=self.hyperparams_dict,
                                                feature_num=self.feature_num).initialize_population()

    def split_data(self) -> None:
        """
        Method that defines the train and test datasets
        """
        if self.data_split == "single":
            if self.train_data is None and self.test_data is None:
                self.train_data, self.test_data = train_test_split(self.data, test_size=self.test_size)
        elif self.data_split == "multiple":
            self.train_data, self.test_data = train_test_split(self.data, test_size=self.test_size)

        else:
            raise ValueError("The type of data split specified does not exist")

    def set_evaluation_method(self, evaluation_method: str, custom_fitness_function=None) -> None:
        """
        Method that sets the fitness function for the program
        Parameters
        ----------
        evaluation_method: str
                           the string that defines the evaluation method that we want to use inside the evaluator,
                           if it's 'custom' the user needs to define the custom_fitness_function
        custom_fitness_function: class
                                 if evaluation_method is custom here we have to have a custom evaluation function
        """

        if self.evaluation_method == "custom" and custom_fitness_function is None:
            raise ValueError("To use a custom evaluation method we need a custom fitness function")

        self.evaluation_method = evaluation_method
        self.custom_fitness_function = custom_fitness_function

    def evaluate_generation(self) -> None:
        """
        Method to evaluate the full generation by finding the fitness for every member of the generation
        """
        evaluator = Evaluator(self.program, self.population, self.evaluation_method, self.target, self.algo_type,
                              self.train_data, self.test_data, self.custom_fitness_function)

        evaluator.evaluate_generation()

    def reproduction(self) -> Iterable:
        """
        it puts together all the steps necessary for the reproduction and generates the children that
        will be added to the population
        Returns
        -------
        Iterable
        a list or numpy array that contains the new chromosomes to be added to the next generation
        """

        rep_function = Reproduction(population=self.population, crossover_method=self.crossover_method,
                                    prob_crossover=self.prob_crossover, hyperparams_types=self.hyperparams_types,
                                    mutation_method=self.mutation_method,
                                    prob_mutation=self.prob_mutation, prob_translation=self.prob_translation,
                                    selection_method=self.selection_method, reproduction_rate=self.reproduction_rate,
                                    tournament_size=self.tournament_size)
        children = rep_function.reproduction()

        return children

    def darwinism(self) -> None:
        """
        it eliminates the chromosomes with the worst fitness from the generation, to make space for the children
        """

        pop_selector = Darwinism(self.population, self.reproduction_rate)
        self.population, self.best_chromosome = pop_selector.discard_worst_performers()

    def run(self) -> Chromosome:
        """
        runs the genetic algorithm for n generation with m genes, storing the best score and the best gene
        """
        self.initialize_population()

        if self.evaluation_method is None:
            raise ValueError("Remember to set the evaluation method before running the algorithm")

        for _ in tqdm(range(self.number_gen)):

            self.split_data()
            self.evaluate_generation()
            children = self.reproduction()

            self.darwinism()

            self.population = self.population + children

            if self.max_fitness_value:
                if self.best_chromosome.fitness > self.max_fitness_value:
                    break

        return self.best_chromosome
