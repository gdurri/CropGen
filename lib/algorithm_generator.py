from pymoo.algorithms.moo.nsga2 import NSGA2

class AlgorithmGenerator():  
  def _create_nsga2_algorithm(self, pop_size):
    # TODO - get_sampling ETC have been deprecated.
    # return NSGA2(
    #   pop_size = 5,
    #   sampling = get_sampling("real_random"),
    #   crossover = get_crossover("real_sbx", prob=0.9, eta=15),
    #   mutation = get_mutation("real_pm", eta=20),
    #   eliminate_duplicates = True
    # )
    return NSGA2(pop_size = pop_size)

