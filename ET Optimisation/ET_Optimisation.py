from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.optimize import minimize
import numpy as np
from apsim import ApsimRunner, ApsimOptions
import plotly.express as px
import statistics as stats
import pandas as pd
import time

start_time = time.time()

indivs=[]

f1_apsim = 'Yield'
f3_apsim = 'Evapotranspiration'

x1 = 'EndJuvtoFI Thermal Time (DD)'
x2 = 'Fertile Tiller Number'

f1 = 'Yield (t/ha)'
f2 = 'Failure Risk (Yield < 1.5 t/ha)'
f3 = 'Evapotranspiration (mm)'

options = ApsimOptions(r"C:\Users\uqgdurri\AppData\Local\Programs\APSIM2022.11.7108.0\bin\Models.exe",
                       r"C:\Users\uqgdurri\OneDrive - The University of Queensland\Desktop\PhD\ET Characterisation\Factorial Testing\ET_Dalby_Interdrought\Optimisation_Dalby_Interdrought.apsimx")
table = 'HarvestReport'
outs = ['Season', f1_apsim, f3_apsim]
test = ApsimRunner()

# ET1_Years= pd.read_csv(r'C:\Users\uqgdurri\OneDrive - The University of Queensland\Desktop\PhD\ET Characterisation\Factorial Testing\ET_Dalby_Interdrought\Dalby_ET1.csv')
# ET2_Years= pd.read_csv(r'C:\Users\uqgdurri\OneDrive - The University of Queensland\Desktop\PhD\ET Characterisation\Factorial Testing\ET_Dalby_Interdrought\Dalby_ET2.csv')
# ET3_Years= pd.read_csv(r'C:\Users\uqgdurri\OneDrive - The University of Queensland\Desktop\PhD\ET Characterisation\Factorial Testing\ET_Dalby_Interdrought\Dalby_ET3.csv')
# ET4_Years= pd.read_csv(r'C:\Users\uqgdurri\OneDrive - The University of Queensland\Desktop\PhD\ET Characterisation\Factorial Testing\ET_Dalby_Interdrought\Dalby_ET4.csv')
ET5_Years= pd.read_csv(r'C:\Users\uqgdurri\OneDrive - The University of Queensland\Desktop\PhD\ET Characterisation\Factorial Testing\ET_Dalby_Interdrought\Dalby_ET5.csv')

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
            params['[Fixed Sowing].Script.Ftn']= x[1]

            obj=test.run(options, params, outs, table)

            ET5 = pd.merge(obj, ET5_Years)

            f1val = -1 * (stats.mean(ET5[f1_apsim]))  # multiple years
            f2val = 1 * (((ET5[f1_apsim] < 150).sum())/ len(ET5)) # multiple years
            f3val = 1 * (stats.mean(ET5[f3_apsim]))

            results.append([f1val,f2val])

            indivs.append((x[0], x[1], (f1val * -0.01), f2val, f3val))

        out['F']=np.array(results)
        print(50)

#Create problem object
problem=OptProblem()

genNumber= 1
popSize= 2

#Create algorithm object
algorithm = NSGA2(
    pop_size=popSize,
    sampling=get_sampling("real_lhs"),
    crossover=get_crossover("real_sbx", prob=0.9, eta=15),
    mutation=get_mutation("real_pm", eta=20),
    eliminate_duplicates=True)

#Run the optimisation algorithm on the defined problem. Note: framework only performs minimisation,
# so problems must be framed such that each objective is minimised
res=minimize(problem, algorithm, ("n_gen", genNumber), save_history= True, verbose=False) #seed = 1

X=res.X #Variable values for non-dominated individuals in the last generation
F=res.F #Objective values for non-dominated individuals in the last generation
hist=res.history #History of data from all generations

tot=list(zip(X[:,0], X[:,1], ( -0.01 * F[:,0]), F[:,1]))
opt_df=pd.DataFrame(tot, columns =[x1, x2, f1, f2])
all_df=pd.DataFrame(indivs, columns =[x1, x2, f1, f2, f3])


all_df.to_csv(r'C:\Users\uqgdurri\OneDrive - The University of Queensland\Desktop\PhD\ET Characterisation\Factorial Testing\ET_Dalby_Interdrought\ET5\All_individuals.csv', encoding='utf-8', index=False)
opt_df.to_csv(r'C:\Users\uqgdurri\OneDrive - The University of Queensland\Desktop\PhD\ET Characterisation\Factorial Testing\ET_Dalby_Interdrought\ET5\Optimal_individuals.csv', encoding='utf-8', index=False)

print(opt_df.sort_values('Yield (t/ha)', ascending=False))
print(all_df.sort_values('Yield (t/ha)', ascending=False))

#Only running when script is run directly, i.e. no results plotted when imported
#if __name__ =='__main__':

    # Plotting Results

xl, xu = problem.bounds()

fig = px.scatter(opt_df, x=x1, y=x2, template = 'plotly_white',
                 hover_data={f1: ':.2f', f2: ':.2f', x1: False, x2: False},
                 width=800, height=600)
fig.update_traces(mode="markers", marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')))
fig.update_layout(font_family='Courier New', font_size = 20, title_font_color = 'black', title_x=0.5)
fig.update_xaxes(range=[xl[0], xu[0]], gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.update_yaxes(range=[xl[1], xu[1]], gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.show()
fig.write_html(r'C:\Users\uqgdurri\OneDrive - The University of Queensland\Desktop\PhD\ET Characterisation\Factorial Testing\ET_Dalby_Interdrought\ET5\Optimal_designs.html')

fig = px.scatter(opt_df, x=f2, y=f1, template='plotly_white',
                 hover_data={f1: False, f2: False, x1: ':.2f', x2: ':.2f'},
                 width=800, height=600)
fig.update_traces(mode="markers", marker=dict(size=12,line=dict(width=2, color='DarkSlateGrey')))
fig.update_layout(font_family='Courier New', font_size = 20, title_font_color = 'black', title_x=0.5)
fig.update_xaxes(gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.update_yaxes(gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.show()
