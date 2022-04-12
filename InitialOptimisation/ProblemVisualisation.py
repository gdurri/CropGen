from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_problem, get_sampling, get_crossover, get_mutation
from pymoo.optimize import minimize
from pymoo.util.plotting import plot
import matplotlib.pyplot as plt
import numpy as np

class TNKProblem(Problem):

    def __init__(self):

        """Construct problem with the given dimensions and variable ranges"""

        super().__init__(n_var=2, n_obj=2, n_constr=2, xl=np.array([0.0,0.0]), xu= np.array([np.pi, np.pi]))

    def _evaluate(self, xs, out, *args, **kwargs):

        """Evaluate fitness of the individuals in the population
        Parameters:
            xs(list): The variable values (in lists) for each individual in the population
            out(dict): The dictionary to write the objective values out to. 'F' key for objectives
                       and 'G' key for constraints
        """

        results=[]
        constraints=[]
        for x in xs:

            #Replace here with APSIM call

            results.append([f1,f2])
            constraints.append([g1,g2])

        out['F']=np.array(results)
        out["G"]=np.array(constraints)

#Create problem object
problem=TNKProblem()

#Create algorithm object
algorithm = NSGA2(
    pop_size=25,
    sampling=get_sampling("real_random"),
    crossover=get_crossover("real_sbx", prob=0.9, eta=15),
    mutation=get_mutation("real_pm", eta=20),
    eliminate_duplicates=True)

genNumber=25

#Run the optimisation algorithm on the defined problem. Note: framework only performs minimisation,
# so problems must be framed such that each objective is minimised
res=minimize(problem, algorithm, ("n_gen", genNumber),  seed=1, save_history= True, verbose=False)

X=res.X #Variable values for non-dominated individuals in the last generation
F=res.F #Objective values for non-dominated individuals in the last generation
hist=res.history #History of data from all generations

#Only running when script is run directly, i.e. no results plotted when imported
if __name__ =='__main__':

    # Plotting Results

    empirical = get_problem("tnk")

    xl, xu = problem.bounds()
    plt.figure(figsize=(7, 5))
    plt.scatter(X[:, 0], X[:, 1], s=30, facecolors='r', edgecolors='r')
    plt.xlim(xl[0], xu[0])
    plt.ylim(xl[1], xu[1])
    plt.title("Design Space")
    plt.show()

    plt.figure(figsize=(7, 5))
    plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='b', edgecolors='b')
    plot(empirical.pareto_front(), no_fill=True)
    plt.title("Objective Space")
    plt.show()