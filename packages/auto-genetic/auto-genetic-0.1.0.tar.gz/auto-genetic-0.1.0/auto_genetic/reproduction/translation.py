import numpy as np
from auto_genetic.population_initializer.chromosomes import Chromosome
from copy import deepcopy


class Translation:
    """
    Class that performs the translation over a Chromosome
    Attributes
    ----------
    prob_translation: float
                      the probability that the translation is performed
    Methods
    -------
    self.perform_translation(child): it uses the Translation class on a Chromosome and performs the translation
    """
    def __init__(self, prob_translation: float) -> None:
        self.prob_translation = prob_translation

    def perform_translation(self, child: Chromosome) -> Chromosome:
        prob = np.random.rand()
        translated_gene = deepcopy(child)
        if prob <= self.prob_translation:
            num_traslated = np.random.randint(0, len(child.sequence))
            translated_gene.sequence = np.hstack([translated_gene.sequence[-num_traslated:],
                                                  translated_gene.sequence[:-num_traslated]])

        translated_gene.fitness = None

        return translated_gene
