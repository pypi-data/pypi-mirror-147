import pandas as pd
import numpy as np
from auto_genetic.population_initializer.chromosomes import Chromosome


class FeatureSelector:
    """
    Class used to select the features
    Attributes
    ----------
    data: pd.DataFrame
          the data that we want to apply the feature selector on, it needs to have the column target
    target: str
            the name of the column that is used as target for the evaluation

    Methods
    -------
    self.feature_select(chromosome): it selects the features of the data given the sequence of the chromosome
    """
    def __init__(self, data: pd.DataFrame = None, target: str = None) -> None:
        self.data = data
        self.target = target
        self.x = data.drop(self.target, axis=1)
        self.y = data[self.target]

    def feature_select(self, chromosome: Chromosome) -> pd.DataFrame:
        """
        it selects the features of the data given the sequence of the chromosome
        Parameters
        ----------
        chromosome: Chromosome
                    a chromosome class that contains the sequence with the columns that we want to have active or not

        Returns
        -------
        pd.DataFrame
        a dataframe that contains the target column and the columns selected from the chromosome

        """
        sequence = chromosome.sequence
        filterer = np.argwhere(sequence == 1)
        x_filtered = self.x.iloc[:, filterer.flatten()]
        df_filtered = pd.concat([x_filtered, self.y], axis=1)

        chromosome.features = list(df_filtered.columns)

        return df_filtered
