import numpy as np


class FeatureSetter:
    """
    Chromosome class, that contains the sequence, the hyperparameters and the fitness of its linked program run
    Attributes
    ----------
    algo_type: str
               can be "hyperparameter_tuning" or "feature_selection", it represents what is the purpose of the G
    feature_num: int
                 the number of features from which to select

    Methods
    -------
    self.set_feature_sequence(): it generates a sequence of 0s and 1s according to if we want to keep or not the column
    """
    def __init__(self, algo_type: str, feature_num: int) -> None:
        self.algo_type = algo_type
        self.feature_num = feature_num

    def set_feature_sequence(self) -> list:
        """
        it generates a sequence of 0s and 1s according to if we want to keep or not the column
        Returns
        -------
        list
        a sequence of 0s and 1s with the size equal to the n_features
        """
        if self.algo_type == "feature_selection":
            sequence = np.random.choice([0, 1], size=self.feature_num, p=[0.5, 0.5])
            return sequence

        else:
            raise ValueError("If the algo_type is not feature_selection, you should not need this method")
