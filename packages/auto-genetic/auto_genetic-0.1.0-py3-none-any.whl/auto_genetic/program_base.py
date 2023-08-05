import pandas as pd
from abc import ABC, abstractmethod


class BaseProgram(ABC):
    """
    Abstract Base Class for the programs, any program has to inherit from this one, or have the same methods, is
    possible to add any additional method, but they need to be run inside either run or predict
    Methods
    -------
    self.set_program_hyperparams(hyperparams): method that is used by each chromosome to set the hyperparameter for
                                               the program, os it needs to be there
    self.run(train_data): it runs the defined program, all the processes of the program have to be passed here
    self.predict(test_data): it predicts and these predictions are used to calculate the fitness of the program
    """
    def __init__(self):
        self.hyperparams = None

    def set_program_hyperparams(self, hyperparams: dict):
        self.hyperparams = hyperparams

    @abstractmethod
    def run(self, train_data: pd.DataFrame):
        pass

    @abstractmethod
    def predict(self, test_data: pd.DataFrame):
        pass
