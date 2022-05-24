import SingleYear_ProblemVisualisation as prb #Make sure to pick the correct version for single/ multi year runs
import numpy as np
import matplotlib.pyplot as plt

#Lists for historical information
n_evals= []
hist_F= []
hist_cv= []
hist_cv_avg= []
num_nondom=[]

#For each generation in the history
for gen in prb.hist:

    #Append list with number of evaluations in the generation
    n_evals.append(gen.evaluator.n_eval)

    #Optimal individuals from the generation
    opt=gen.opt

    #Append lists with miniumum and average constraint violations
    hist_cv.append(opt.get("CV").min())
    hist_cv_avg.append(gen.pop.get("CV").mean())

    #list of Non-dominated individuals
    feas=np.where(opt.get('feasible'))[0]

    #Append list with number of non-dominant individuals in generation
    num_nondom.append(len(feas))

    #Append list with objective values for non-dominated individuals in generation
    hist_F.append(opt.get("F")[feas])

#Generation with the first feasible individual
k=np.where(np.array(hist_cv)<=0)[0].min()
print(f"At least one feasible solution in generation {k} after {n_evals[k]} evaluations")

#Generation with all feasible individuals
k=np.where(np.array(hist_cv_avg)<=0)[0].min()
print(f"Whole population feasible in generation {k} after {n_evals[k]} evaluations")

#Plot constraint violation against number of fucntion evaluations
plt.figure(figsize=(7, 5))
plt.plot(n_evals, hist_cv_avg,  color='black', lw=0.7, label="Avg. CV of Pop")
plt.scatter(n_evals, hist_cv_avg,  facecolor="none", edgecolor='black', marker="p")
plt.axvline(n_evals[k], color="red", label="All Feasible", linestyle="--")
#plt.title("Convergence")
plt.xlabel("Function Evaluations")
plt.ylabel("Constraint Violation")
plt.legend()
plt.show()

#Plot number of non-dominated solutions against generation number
plt.figure(figsize=(7, 5))
plt.plot(np.arange(1,(prb.genNumber +1),1), num_nondom,  color='black', lw=0.7)
plt.scatter(np.arange(1,(prb.genNumber +1),1), num_nondom,  facecolor="none", edgecolor='black', marker="p")
plt.xlabel("Generation")
plt.ylabel("Number of Non-Dominated Solutions")
plt.show()

