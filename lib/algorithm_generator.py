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
        # TODO - get_sampling etc have all been deprecated.
        # return NSGA2(
        #   pop_size = 5,
        #   sampling = get_sampling("real_random"),
        #   crossover = get_crossover("real_sbx", prob=0.9, eta=15),
        #   mutation = get_mutation("real_pm", eta=20),
        #   eliminate_duplicates = True
        # )

        return NSGA2(pop_size=pop_size,
                     sampling=FloatRandomSampling(),
                     crossover=SBX(eta=cross_over_eta, prob=cross_over_prob),
                     mutation=PM(eta=mutation_eta),
                     eliminate_duplicates=True)
