import SingleYear_ProblemVisualisation as prb #Make sure to pick the correct version for single/ multi year runs
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

colours=['red','green', 'fuchsia', 'yellow', 'blue']
objective_fig = make_subplots(rows=1, cols=1)
variable_fig = make_subplots(rows=1, cols=1)                             

if prb.genNumber <= 5: 
    count=0
    legends=[f'Generation {x+1}' for x in range(prb.genNumber)]

    for i in range(0, len(prb.all_df), prb.popSize):
        objectives= px.scatter(prb.all_df[i: i+ prb.popSize], x=prb.f1, y=prb.f2)
        objectives.data[0]['marker']['color']= colours[count]
        objectives.data[0]['showlegend']= True
        objectives.data[0]['name'] = legends[count]
        objective_fig.add_trace(objectives.data[0])

        variables= px.scatter(prb.all_df[i: i+ prb.popSize], x=prb.x1, y=prb.x2)
        variables.data[0]['marker']['color']= colours[count]
        variables.data[0]['showlegend']= True
        variables.data[0]['name'] = legends[count]
        variable_fig.add_trace(variables.data[0])


        count +=1
else:
    indivGroups= list(range(len(prb.all_df)))[0::prb.popSize]
    gensInterest= np.round(np.linspace(0, len(indivGroups) - 1, 5)).astype(int)
    groupsInterest=[indivGroups[x] for x in gensInterest]

    for i in range(len(groupsInterest)):
        objectives= px.scatter(prb.all_df[groupsInterest[i]: (groupsInterest[i]+ prb.popSize)], x=prb.f1, y=prb.f2)
        objectives.data[0]['marker']['color']= colours[i]
        objectives.data[0]['showlegend']= True
        objectives.data[0]['name'] = f'Generation {(gensInterest[i]+1)}'
        objective_fig.add_trace(objectives.data[0])

        variables= px.scatter(prb.all_df[groupsInterest[i]: (groupsInterest[i]+ prb.popSize)], x=prb.x1, y=prb.x2)
        variables.data[0]['marker']['color']= colours[i]
        variables.data[0]['showlegend']= True
        variables.data[0]['name'] = f'Generation {(gensInterest[i]+1)}'
        variable_fig.add_trace(variables.data[0])


objective_fig.update_traces(mode="markers", marker=dict(size=12,line=dict(width=2, color='DarkSlateGrey')))
objective_fig.update_layout(font_family='Courier New', font_size = 16, title_font_color = 'black', title="Objectives over Generations",
                title_x=0.5, template='plotly_white', width=1400, height=700)
objective_fig.update_xaxes(title_text = prb.f1, gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
objective_fig.update_yaxes(title_text = prb.f2, gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
objective_fig.show()

variable_fig.update_traces(mode="markers", marker=dict(size=12,line=dict(width=2, color='DarkSlateGrey')))
variable_fig.update_layout(font_family='Courier New', font_size = 16, title_font_color = 'black', title="Variables over Generations",
                title_x=0.5, template='plotly_white', width=1400, height=700)
variable_fig.update_xaxes(range=[prb.xl[0], prb.xu[0]], title_text = prb.x1, gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
variable_fig.update_yaxes(range=[prb.xl[1], prb.xu[1]], title_text = prb.x2, gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
variable_fig.show()



