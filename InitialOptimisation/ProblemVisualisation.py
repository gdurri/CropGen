from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.optimize import minimize
import numpy as np
from apsim_client import ApsimClient, PropertyType
import plotly.express as px
import plotly
import statistics as stats
import pandas as pd
import time

start_time = time.time()

indivs=[]

f1 = 'WaterUse'
f2 = 'Yield'

client = ApsimClient()
ip = "127.0.0.1"
port = 27746
outputNames = [f1, f2]
outputTypes = [PropertyType.DOUBLE, PropertyType.DOUBLE]
table = 'HarvestReport'
params={}


class OptProblem(Problem):

    def __init__(self):

        """Construct problem with the given dimensions and variable ranges"""

        super().__init__(n_var=2, n_obj=2, xl=np.array([130.0, 0.0]), xu= np.array([190.0, 4.0]))

    def _evaluate(self, xs, out, *args, **kwargs):

        """Evaluate fitness of the individuals in the population
        Parameters:
            xs(list): The variable values (in lists) for each individual in the population
            out(dict): The dictionary to write the objective values out to. 'F' key for objectives
                       and 'G' key for constraints
        """

        results=[]

        for x in xs:
            params = {}
            params['[Sorghum].Phenology.TTEndJuvToInit.FixedValue'] = x[0]
            params['[Sow on a fixed date].Script.Tillering']= x[1]
            print(params)

            obj=client.run(params, outputNames, outputTypes, table, ip, port)
            print(obj)

            f1val=1*(obj[f1][0]) # one year
            #f1 = -1 * (stats.median(obj['Yield'])) # multiple years
            f2val=-1*(obj[f2][0]) #one year
            #f2 = -1 * (stats.median(obj['Biomass']))  # multiple years

            results.append([f1val,f2val])

            indivs.append((x[0], x[1], f1val, (f2val * -0.01)))

        out['F']=np.array(results)


#Create problem object
problem=OptProblem()

#Create algorithm object
algorithm = NSGA2(
    pop_size=5,
    sampling=get_sampling("real_random"),
    crossover=get_crossover("real_sbx", prob=0.9, eta=15),
    mutation=get_mutation("real_pm", eta=20),
    eliminate_duplicates=True)

genNumber=5

#Run the optimisation algorithm on the defined problem. Note: framework only performs minimisation,
# so problems must be framed such that each objective is minimised
res=minimize(problem, algorithm, ("n_gen", genNumber), save_history= True, verbose=False) #seed = 1

X=res.X #Variable values for non-dominated individuals in the last generation
F=res.F #Objective values for non-dominated individuals in the last generation
hist=res.history #History of data from all generations

tot=list(zip(X[:,0], X[:,1], F[:,0], ( -0.01 * F[:,1])))
opt_df=pd.DataFrame(tot, columns =['EndJuvtoFI Thermal Time (DD)', 'Fertile Tiller Number',
                                   'Total Crop Water Use (mm)', 'Yield (t/ha)'])
all_df=pd.DataFrame(indivs, columns =['EndJuvtoFI Thermal Time (DD)', 'Fertile Tiller Number',
                                      'Total Crop Water Use (mm)', 'Yield (t/ha)'])

print(opt_df.sort_values('Yield (t/ha)', ascending=False))
print(all_df.sort_values('Yield (t/ha)', ascending=False))

#Only running when script is run directly, i.e. no results plotted when imported
#if __name__ =='__main__':

    # Plotting Results

xl, xu = problem.bounds()

fig = px.scatter(opt_df, x="EndJuvtoFI Thermal Time (DD)", y="Fertile Tiller Number", title="Design Space", template = 'plotly_white',
                 hover_data={"Total Crop Water Use (mm)": ':.2f', "Yield (t/ha)": ':.2f', "EndJuvtoFI Thermal Time (DD)": False, "Fertile Tiller Number": False},
                 width=1400, height=700)
fig.update_traces(mode="markers", marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')))
fig.update_layout(font_family='Courier New', font_size = 16, title_font_color = 'black', title_x=0.5)
fig.update_xaxes(range=[xl[0], xu[0]], gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.update_yaxes(range=[xl[1], xu[1]], gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.show()

fig = px.scatter(opt_df, x="Total Crop Water Use (mm)", y="Yield (t/ha)", title="Objective Space", template='plotly_white',
                 hover_data={"Total Crop Water Use (mm)": False, "Yield (t/ha)": False, "EndJuvtoFI Thermal Time (DD)": ':.2f', "Fertile Tiller Number": ':.2f'},
                 width=1400, height=700)
fig.update_traces(mode="markers", marker=dict(size=12,line=dict(width=2, color='DarkSlateGrey')))
fig.update_layout(font_family='Courier New', font_size = 16, title_font_color = 'black', title_x=0.5)
fig.update_xaxes(gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.update_yaxes(gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.show()

fig = px.scatter(all_df, x="EndJuvtoFI Thermal Time (DD)", y="Fertile Tiller Number", color="Yield (t/ha)", title="All Individuals", template='plotly_white',
                 hover_data={"Total Crop Water Use (mm)": ':.2f', "Yield (t/ha)": ':.2f', "EndJuvtoFI Thermal Time (DD)": False, "Fertile Tiller Number": False},
                 width=1400, height=700)
fig.update_traces(mode="markers", marker=dict(size=12,line=dict(width=2, color='DarkSlateGrey')))
fig.update_layout(font_family='Courier New', font_size = 16, title_font_color = 'black', title_x=0.5)
fig.update_xaxes(range=[xl[0], xu[0]], gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.update_yaxes(range=[xl[1], xu[1]], gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.show()

fig = px.scatter(all_df, x="Total Crop Water Use (mm)", y="Yield (t/ha)", title="All Objectives", template='plotly_white',
                 hover_data={"Total Crop Water Use (mm)": False, "Yield (t/ha)": False, "EndJuvtoFI Thermal Time (DD)": ':.2f', "Fertile Tiller Number": ':.2f'},
                 width=1400, height=700)
fig.update_traces(mode="markers", marker=dict(size=12,line=dict(width=2, color='DarkSlateGrey')))
fig.update_layout(font_family='Courier New', font_size = 16, title_font_color = 'black', title_x=0.5)
fig.update_xaxes(gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.update_yaxes(gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.show()

"""
xl, xu = problem.bounds()
plt.figure(figsize=(7, 5))
plt.scatter(X[:, 0], X[:, 1], s=30, facecolors='r', edgecolors='r')
plt.xlim(xl[0], xu[0])
plt.ylim(xl[1], xu[1])
plt.title("Design Space")
plt.ylabel("Fertile Tiller Number")
plt.xlabel("EndJuvtoFI Thermal Time (DD)")
plt.show()

plt.figure(figsize=(7, 5))
plt.scatter((F[:, 0] * 1), (F[:, 1] * -0.01), s=30, facecolors='b', edgecolors='b')
#plt.xlim(0, 1000)
#plt.ylim(0, 2000)
plt.title("Objective Space")
plt.xlabel("Total Crop Water Use (mm)")
plt.ylabel("Yield (t/ha)")
plt.show()

xl, xu = problem.bounds()
plt.figure(figsize=(7, 5))
plt.scatter(x1vals, x2vals, s=30, facecolors='r', edgecolors='r')
plt.xlim(xl[0], xu[0])
plt.ylim(xl[1], xu[1])
plt.title("All Individuals")
plt.ylabel("Fertile Tiller Number")
plt.xlabel("EndJuvtoFI Thermal Time (DD)")
plt.show()

plt.figure(figsize=(7, 5))
plt.scatter(f1vals, f2vals, s=30, facecolors='b', edgecolors='b')
plt.title("All Objectives")
plt.xlabel("Total Crop Water Use (mm)")
plt.ylabel("Yield (t/ha)")
plt.show()
"""

print("--- %s seconds ---" % (time.time() - start_time))