from abc import ABC, abstractmethod

import pandas as pd

from auto_genetic.evaluation.metrics import *


class FitnessFunctionBase(ABC):
    """
    Base Class for fitness functions
    Attributes
    ----------
    program: class
            the user defined program that has the run() and predict() methods
    target: str
            the name of the column that is used as target for the evaluation
    train_data: pd.DataFrame
                a pandas dataframe that contains the training data, including the target
    test_data: pd.DataFrame
               a pandas dataframe that contains the training data, possibly also the target (depends on the
               fitness function)

    Methods
    -------
    self.calculate_fitness(): abstract method
    """
    def __init__(self, program, train_data: pd.DataFrame, test_data: pd.DataFrame, target: str):
        self.train_data = train_data
        self.test_data = test_data
        self.program = program
        self.target = target

    @abstractmethod
    def calculate_fitness(self):
        pass


class RMSEFitness(FitnessFunctionBase):
    """
    Class to calculate Root Mean Squared Error fitness functions
    Attributes
    ----------
    program: class
            the user defined program that has the run() and predict() methods
    target: str
            the name of the column that is used as target for the evaluation
    train_data: pd.DataFrame
                a pandas dataframe that contains the training data, including the target
    test_data: pd.DataFrame
               a pandas dataframe that contains the training data, possibly also the target (depends on the
               fitness function)

    Methods
    -------
    self.calculate_fitness(): calculates the rmse of the program and then put it negative because we are solving
                              a maximisation problem
    """
    def __init__(self, program, train_data: pd.DataFrame, test_data: pd.DataFrame, target: str) -> None:
        super(RMSEFitness, self).__init__(program, train_data, test_data, target)

    def calculate_fitness(self) -> float:
        """
        runs the program and predicts the output, then it computes the RMSE and put it negative
        Returns
        -------
        float
        the negative RMSE of the program, it's negative because we always solve a maximisation problem

        """
        self.program.run(self.train_data)
        predictions = self.program.predict(self.test_data)

        error = self.test_data[self.target] - predictions

        rmse = root_mean_squared_error(error)

        return - rmse


class MAEFitness(FitnessFunctionBase):
    """
    Class to calculate Mean Absolute Error fitness functions
    Attributes
    ----------
    program: class
            the user defined program that has the run() and predict() methods
    target: str
            the name of the column that is used as target for the evaluation
    train_data: pd.DataFrame
                a pandas dataframe that contains the training data, including the target
    test_data: pd.DataFrame
               a pandas dataframe that contains the training data, possibly also the target (depends on the
               fitness function)

    Methods
    -------
    self.calculate_fitness(): calculates the mae of the program and then put it negative because we are solving
                              a maximisation problem
    """
    def __init__(self, program, train_data: pd.DataFrame, test_data: pd.DataFrame, target: str) -> None:
        super(MAEFitness, self).__init__(program, train_data, test_data, target)

    def calculate_fitness(self) -> float:
        """
        runs the program and predicts the output, then it computes the MAE and put it negative
        Returns
        -------
        float
        the negative MAE of the program, it's negative because we always solve a maximisation problem

        """
        self.program.run(self.train_data)
        predictions = self.program.predict(self.test_data)

        error = self.test_data[self.target] - predictions

        mae = root_mean_squared_error(error)

        return - mae


class SMAPEFitness(FitnessFunctionBase):
    """
    Class to calculate Scaled Mean Absolute Percentage Error fitness functions
    Attributes
    ----------
    program: class
            the user defined program that has the run() and predict() methods
    target: str
            the name of the column that is used as target for the evaluation
    train_data: pd.DataFrame
                a pandas dataframe that contains the training data, including the target
    test_data: pd.DataFrame
               a pandas dataframe that contains the training data, possibly also the target (depends on the
               fitness function)

    Methods
    -------
    self.calculate_fitness(): calculates the SMAPE of the program and then put it negative because we are solving
                              a maximisation problem
    """
    def __init__(self, program, train_data: pd.DataFrame, test_data: pd.DataFrame, target: str) -> None:
        super(SMAPEFitness, self).__init__(program, train_data, test_data, target)

    def calculate_fitness(self) -> float:
        """
        runs the program and predicts the output, then it computes the SMAPE and put it negative
        Returns
        -------
        float
        the negative SMAPE of the program, it's negative because we always solve a maximisation problem

        """
        self.program.run(self.train_data)
        predictions = self.program.predict(self.test_data)

        s_mape = symmetric_mean_average_percentage_error(self.test_data[self.target], predictions)

        return - s_mape


class MAAPEFitness(FitnessFunctionBase):
    """
    Class to calculate Mean Arctan Absolute Percentage Error fitness functions
    Attributes
    ----------
    program: class
            the user defined program that has the run() and predict() methods
    target: str
            the name of the column that is used as target for the evaluation
    train_data: pd.DataFrame
                a pandas dataframe that contains the training data, including the target
    test_data: pd.DataFrame
               a pandas dataframe that contains the training data, possibly also the target (depends on the
               fitness function)

    Methods
    -------
    self.calculate_fitness(): calculates the MAAPE of the program and then put it negative because we are solving
                              a maximisation problem
    """

    def __init__(self, program, train_data: pd.DataFrame, test_data: pd.DataFrame, target: str) -> None:
        super(MAAPEFitness, self).__init__(program, train_data, test_data, target)

    def calculate_fitness(self) -> float:
        """
        runs the program and predicts the output, then it computes the MAAPE and put it negative
        Returns
        -------
        float
        the negative MAAPE of the program, it's negative because we always solve a maximisation problem

        """
        self.program.run(self.train_data)
        predictions = self.program.predict(self.test_data)

        s_mape = mean_arctangent_absolute_percentage_error(self.test_data[self.target], predictions)

        return - s_mape
