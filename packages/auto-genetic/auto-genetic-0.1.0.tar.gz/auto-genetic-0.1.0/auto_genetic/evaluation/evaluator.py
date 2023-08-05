from auto_genetic.population_initializer.chromosomes import Chromosome
from auto_genetic.evaluation.fitnessfuncsetter import FitnessFuncSetter
from auto_genetic.evaluation.feature_selector import FeatureSelector
from tqdm import tqdm
import pandas as pd


class Evaluator:
    """
    Class for the evaluation of chromosomes
    Attributes
    ----------
    program: class
            the user defined program that has the run() and predict() methods
    population: list
                the list that contains all the Chromosomes that make up the population
    evaluation_method: str
                       the string that defines the evaluation method that we want to use inside the evaluator,
                       if it's 'custom' the user needs to define the custom_fitness_function
    target: str
            the name of the column that is used as target for the evaluation
    algo_type: str
               can be "hyperparameter_tuning" or "feature_selection", it represents what is the purpose of the GA
    train_data: pd.DataFrame
                a pandas dataframe that contains the training data, including the target
    test_data: pd.DataFrame
               a pandas dataframe that contains the training data, possibly also the target (depends on the
               fitness function)
    custom_fitness_function: class
                             if evaluation_method is custom here we have to have a custom evaluation function

    Methods
    -------
    Private:
        self._set_program_hyperparams(chromosome): it sets the hyperparameters for the program using a specific
                                                   chromosome
        self._filter_data(chromosome): it filters the data for the dataframe for a certain chromosome
    Public:
        self.evaluate_chromosome(chromosome): it computes the fitness for a certain chromosome
        self.evaluate_generation(): it computes the fitness for the whole population
    """

    def __init__(self, program, population: list, evaluation_method: str, target: str, algo_type: str,
                 train_data: pd.DataFrame, test_data: pd.DataFrame, custom_fitness_function=None) -> None:

        self.program = program
        self.population = population
        self.evaluation_method = evaluation_method
        self.train_data = train_data
        self.test_data = test_data
        self.target = target
        self.custom_fitness_function = custom_fitness_function
        self.algo_type = algo_type

    def _set_program_hyperparams(self, chromosome: Chromosome) -> None:
        """
        it sets the hyperparameters of a certain chromosome
        Parameters
        ----------
        chromosome: Chromosome
                    A chromosome that contains the hyperparameters to feed to our program

        """
        if chromosome.hyperparams is None:
            raise ValueError("There is an issue with the hyperparameters of this chromosome")

        self.program.set_program_hyperparams(chromosome.hyperparams)

    def _filter_data(self, chromosome: Chromosome) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        it uses the sequence of the chromosome to select which columns will be selected from the dataframe
        Parameters
        ----------
        chromosome: Chromosome
                    A chromosome that contains a sequence of 0s and 1s to activate/dis-activate the columns

        """
        selector_train = FeatureSelector(data=self.train_data, target=self.target)
        selector_test = FeatureSelector(data=self.test_data, target=self.target)

        train_data, test_data = selector_train.feature_select(chromosome), selector_test.feature_select(
            chromosome)

        return train_data, test_data

    def evaluate_chromosome(self, chromosome: Chromosome) -> None:
        """
        Function to evaluate the fitness of a chromosome by running the program using the predefined fitness function
        Parameters
        ----------
        chromosome: Chromosome
                    contains the information needed for the evaluation and will receive a fitness attribute

        """
        if self.algo_type == "feature_selection":
            train_data, test_data = self._filter_data(chromosome)
            func_setter = FitnessFuncSetter(self.evaluation_method, self.program, train_data, test_data,
                                            self.target)
        elif self.algo_type == "hyperparameter_tuning":
            self._set_program_hyperparams(chromosome)
            func_setter = FitnessFuncSetter(self.evaluation_method, self.program, self.train_data, self.test_data,
                                            self.target)

        else:
            raise ValueError("Please specify a valid algo_type")

        fitness_function = func_setter.set_fitness_func(
            custom_fitness_function=self.custom_fitness_function).get_fitness_func()
        chromosome.set_fitness_function(fitness_function)

        chromosome.calculate_fitness()

    def evaluate_generation(self):
        """
        Method to evaluate the full generation by using self.evaluate_chromosome for every member of the generation
        """
        for chromosome in tqdm(self.population, miniters=10):
            self.evaluate_chromosome(chromosome)
