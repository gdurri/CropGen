import ProblemVisualisation as prb
import matplotlib.pyplot as plt

#Generations for which to plot historical information
gens_of_interest=[0, 4, 14, 24]
colours=['r','g', 'm', 'b']

#Create figure
fig= plt.figure()
ax1= fig.add_subplot(111)

#Count to access different colours
count=0

#For each generation we are interested in
for x in gens_of_interest:
    generation=prb.hist[x] #Get history information
    individuals = generation.opt #Get individuals at the end of that generation
    function_values = individuals.get("F") #Get objective data for each individual
    print(f"In generation {x+1}, there are {len(individuals)} non-dominated individuals")

    #Plot objective values of each individual for each generation of interest
    ax1.scatter(function_values[:, 0], function_values[:, 1], s=30, facecolors='none',
                edgecolors=colours[count], label="Generation {}".format((x+1)))
    plt.title("Objective Space")
    plt.legend(loc='upper right')
    count+=1

plt.show()
