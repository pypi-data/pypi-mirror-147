from __future__ import annotations
import pandas as pd

from auto_genetic.evaluation.fitness_functions import *


class FitnessFuncSetter:
    """
    Class that sets the fitness function for the chromosomes
    Attributes
    ----------
    program: class
            the user defined program that has the run() and predict() methods
    evaluation_method: str
                       the string that defines the evaluation method that we want to use inside the evaluator,
                       if it's 'custom' the user needs to define the custom_fitness_function
    target: str
            the name of the column that is used as target for the evaluation
    train_data: pd.DataFrame
                a pandas dataframe that contains the training data, including the target
    test_data: pd.DataFrame
               a pandas dataframe that contains the training data, possibly also the target (depends on the
               fitness function)

    Methods
    -------
    self.set_fitness_func(custom_fitness_func): method that allows the user to pass a custom fitness function
    self.get_fitness_func(): method that sets a fitness function for a chromosome
    """
    def __init__(self, evaluation_method: str, program, train_data: pd.DataFrame, test_data: pd.DataFrame, target: str)\
            -> None:
        self.evaluation_method = evaluation_method
        self.program = program
        self.train_data = train_data
        self.test_data = test_data
        self.target = target
        self.fitness_func = None

    def set_fitness_func(self, custom_fitness_function=None) -> FitnessFuncSetter:
        """
        method that allows the user to pass a custom fitness function
        Parameters
        ----------
        custom_fitness_function: class
                                 user defined fitness function, it can be used if the evaluation_method is "custom"

        Returns
        -------
        FitnessFuncSetter
        it returns the class itself, so it can be used inline

        """
        if self.evaluation_method == "custom":
            if custom_fitness_function is None:
                raise ValueError("to use the custom method you need to implement a custom fitness function"
                                 "inheriting the FitnessFunction class or (at your own risk) by implementing it freely")

            self.fitness_func = custom_fitness_function(self.program, self.train_data, self.test_data, self.target)

        elif self.evaluation_method == "rmse":
            self.fitness_func = RMSEFitness(self.program, self.train_data, self.test_data, self.target)

        elif self.evaluation_method == "mae":
            self.fitness_func = MAEFitness(self.program, self.train_data, self.test_data, self.target)

        elif self.evaluation_method == "s_mape":
            self.fitness_func = SMAPEFitness(self.program, self.train_data, self.test_data, self.target)

        elif self.evaluation_method == "maape":
            self.fitness_func = MAAPEFitness(self.program, self.train_data, self.test_data, self.target)

        else:
            raise ValueError("The selected evaluation method is not available, choose one of the available ones or "
                             "implement your own by choosing custom")

        return self

    def get_fitness_func(self):
        """
        method that allows the user to pass a custom fitness function
        Returns
        -------
        class
        the initialised fitness function that it's chosen
        """
        if self.fitness_func:
            return self.fitness_func

        else:
            raise ValueError("The fitness function has not been defined")
