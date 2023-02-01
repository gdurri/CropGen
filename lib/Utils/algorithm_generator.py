from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM


class AlgorithmGenerator():

    def _create_nsga2_algorithm(self,
                                pop_size,
                                cross_over_eta=15,
                                cross_over_prob=0.9,
                                mutation_eta=20):
        return NSGA2(pop_size=pop_size,
                     # TODO - This used to be set to get_sampling("real_random"),
                     sampling=FloatRandomSampling(),
                     crossover=SBX(eta=cross_over_eta, prob=cross_over_prob),
                     mutation=PM(eta=mutation_eta),
                     eliminate_duplicates=True)
