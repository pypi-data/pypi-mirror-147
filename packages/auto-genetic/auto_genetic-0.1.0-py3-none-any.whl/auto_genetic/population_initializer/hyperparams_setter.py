from __future__ import annotations

import numpy as np
import random
from typing import List


class HyperParamsSetter:
    """
    Class used to set the hyperparameters for a specific chromosome
    Attributes
    ----------
    algo_type: str
               can be "hyperparameter_tuning" or "feature_selection", it represents what is the purpose of the GA
    hyperparams_dict: List[dict, dict]
                      a list that contains 2 dictionaries, one with the hyperparameters' types and another with the
                      hyperparameters' values
    sequence: list
              the list of the values of the chromosome's gene


    Methods
    -------
    Private:
        self._set_continuous(): it chooses the value in the sequence for a continuous hyperparameter
        self._set_categorical(): it chooses the value in the sequence for a categorical hyperparameter
    Public:
        self.get_hyperparameters(): it extracts the hyperparameters from the hyperparameter dict
        self.convert_hyperparams_values(): it sets the sequence for the chromosome, given the hyperparameters
        self.get_program_hyperparams(): it extracts the specific hyperparameters from a chromosome,
                                        that were encoded according to the hyperparameter map
    """
    def __init__(self, hyperparams_dict: List[dict, dict], algo_type: str) -> None:
        self.hyperparams_dict = hyperparams_dict
        self.algo_type = algo_type
        self.hyperparams_values = None
        self.hyperparams_names = None
        self.hyperparams_types = None
        self.hyperparams_map = None
        self.sequence = None

    def get_hyperparameters(self) -> HyperParamsSetter:
        """
        it extracts the hyperparameters from the hyperparameter dict
        Returns
        -------
        HyperParamsSetter
        returns the same class with the more attributes set
        """
        if self.algo_type == "hyperparameter_tuning":
            self.hyperparams_names = self.hyperparams_dict[0].keys()
            self.hyperparams_values = self.hyperparams_dict[1]
            self.hyperparams_types = self.hyperparams_dict[0]

        else:
            raise ValueError("If the algo_type is not hyperparameter_tuning, you should not need this method")
        return self

    def convert_hyperparams_values(self) -> np.array:
        """
        it sets the sequence for the chromosome, given the hyperparameters
        Returns
        -------
        np.array
        the sequence for the chromosome, encoded with the hyperparams map

        """
        self.hyperparams_map = {}
        sequence = []
        for param, values in self.hyperparams_values.items():
            if self.hyperparams_types[param] == "categorical":
                choice = self._set_categorical(param, values)
                sequence.append(choice)
            elif self.hyperparams_types[param] == "continuous":
                choice = self._set_continuous(param, values)
                sequence.append(choice)

            else:
                raise ValueError(f"The parameter: {param}, is neither categorical nor continuous, check the "
                                 f"hyperparameter types and restart")
        self.sequence = sequence

        return np.array(sequence)

    def get_program_hyperparams(self) -> tuple:
        """
        it extracts the specific hyperparameters from a chromosome, that were encoded according to the
        hyperparameter map
        Returns
        -------
        tuple
        A tuple containing 2 dictionaries, the specific hyperparams for the chromosome and the hyperparameter map

        """
        i = 0
        hyperparams = {}
        for name in self.hyperparams_names:
            index = self.sequence[i]
            if self.hyperparams_types[name] == "categorical":
                parameter = self.hyperparams_map[name][1][index]

            else:
                parameter = index

            hyperparams[name] = parameter
            i += 1
        return hyperparams, self.hyperparams_map

    def _set_continuous(self, param: str, values: list) -> float:
        """
        it chooses the value in the sequence for a continuous hyperparameter
        Parameters
        ----------
        param: str
               a string that identifies the parameter we are currently considering
        values: list
                the range between which our hyperparameter can be set

        Returns
        -------
        flaat
        the value that the parameter will take in the program
        """

        self.hyperparams_map[param] = values
        choice = random.uniform(values[0], values[1])

        return choice

    def _set_categorical(self, param: str, values: list) -> int:
        """
        it chooses the value in the sequence for a categorical hyperparameter
        Parameters
        ----------
        param: str
               a string that identifies the parameter we are currently considering
        values: list
                the list of values that our hyperparameter can take

        Returns
        -------
        int
        the encoded value that the parameter will take in the program, corresponding to its position in the
        hyperparameters map
        """
        choices = list(range(len(values)))
        self.hyperparams_map[param] = [choices, values]
        choice = np.random.choice(choices)

        return choice
