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

f1_apsim = 'WaterUse'
f2_apsim = 'Yield'

x1 = 'EndJuvtoFI Thermal Time (DD)'
x2 = 'Fertile Tiller Number'
f1 = 'Total Crop Water Use (mm)'
f2 = 'Yield (t/ha)'

client = ApsimClient()
ip = "127.0.0.1"
port = 27746
outputNames = [f1_apsim, f2_apsim]
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

            f1val=1*(obj[f1_apsim][0]) 
            f2val=-1*(obj[f2_apsim][0]) 
            

            results.append([f1val,f2val])

            indivs.append((x[0], x[1], f1val, (f2val * -0.01)))

        out['F']=np.array(results)


#Create problem object
problem=OptProblem()

genNumber= 2
popSize= 5

#Create algorithm object
algorithm = NSGA2(
    pop_size=popSize,
    sampling=get_sampling("real_random"),
    crossover=get_crossover("real_sbx", prob=0.9, eta=15),
    mutation=get_mutation("real_pm", eta=20),
    eliminate_duplicates=True)


#Run the optimisation algorithm on the defined problem. Note: framework only performs minimisation,
# so problems must be framed such that each objective is minimised
res=minimize(problem, algorithm, ("n_gen", genNumber), save_history= True, verbose=False) #seed = 1

X=res.X #Variable values for non-dominated individuals in the last generation
F=res.F #Objective values for non-dominated individuals in the last generation
hist=res.history #History of data from all generations

tot=list(zip(X[:,0], X[:,1], F[:,0], ( -0.01 * F[:,1])))
opt_df=pd.DataFrame(tot, columns =[x1, x2, f1, f2])
all_df=pd.DataFrame(indivs, columns =[x1, x2, f1, f2])

#all_df.to_csv('C:/Users/uqgdurri/OneDrive - The University of Queensland/Desktop/PhD/CropGen_WorkingCopy/Results/All_individuals.csv', encoding='utf-8', index=False)

print(opt_df.sort_values(f2, ascending=False))
#print(all_df.sort_values('Yield (t/ha)', ascending=False))


#Only running when script is run directly, i.e. no results plotted when imported
#if __name__ =='__main__':

    # Plotting Results

xl, xu = problem.bounds()

fig = px.scatter(opt_df, x= x1, y= x2, title="Design Space", template = 'plotly_white',
                 hover_data={f1: ':.2f', f2: ':.2f', x1: False, x2: False},
                 width=1400, height=700)
fig.update_traces(mode="markers", marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')))
fig.update_layout(font_family='Courier New', font_size = 16, title_font_color = 'black', title_x=0.5)
fig.update_xaxes(range=[xl[0], xu[0]], gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.update_yaxes(range=[xl[1], xu[1]], gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.show()

fig = px.scatter(opt_df, x= f1, y= f2, title="Objective Space", template='plotly_white',
                 hover_data={f1: False, f2: False, x1: ':.2f', x2: ':.2f'},
                 width=1400, height=700)
fig.update_traces(mode="markers", marker=dict(size=12,line=dict(width=2, color='DarkSlateGrey')))
fig.update_layout(font_family='Courier New', font_size = 16, title_font_color = 'black', title_x=0.5)
fig.update_xaxes(gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.update_yaxes(gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.show()

fig = px.scatter(all_df, x= x1, y= x2, color="Yield (t/ha)", title="All Individuals", template='plotly_white',
                 hover_data={f1: ':.2f', f2: ':.2f', x1: False, x2: False},
                 width=1400, height=700)
fig.update_traces(mode="markers", marker=dict(size=12,line=dict(width=2, color='DarkSlateGrey')))
fig.update_layout(font_family='Courier New', font_size = 16, title_font_color = 'black', title_x=0.5)
fig.update_xaxes(range=[xl[0], xu[0]], gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.update_yaxes(range=[xl[1], xu[1]], gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.show()

fig = px.scatter(all_df, x= f1, y= f2, title="All Objectives", template='plotly_white',
                 hover_data={f1: False, f2: False, x1: ':.2f', x2: ':.2f'},
                 width=1400, height=700)
fig.update_traces(mode="markers", marker=dict(size=12,line=dict(width=2, color='DarkSlateGrey')))
fig.update_layout(font_family='Courier New', font_size = 16, title_font_color = 'black', title_x=0.5)
fig.update_xaxes(gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.update_yaxes(gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.show()

fig = px.scatter(all_df, x= x1, y= f2, color= x2, title="Yield over Maturity", template = 'plotly_white',
                 hover_data={f1: ':.2f', f2: False, x1: False, x2: ':.2f'},
                 width=1400, height=700)
fig.update_traces(mode="markers", marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')))
fig.update_layout(font_family='Courier New', font_size = 16, title_font_color = 'black', title_x=0.5)
fig.update_xaxes(gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.update_yaxes(gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.show()

print("--- %s seconds ---" % (time.time() - start_time))