import ProblemVisualisation as prb
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

colours=['red','green', 'fuchsia', 'yellow', 'blue']
fig = make_subplots(rows=1, cols=1)

if prb.genNumber <= 5: 
    count=0
    legends=[f'Generation {x+1}' for x in range(prb.genNumber)]

    for i in range(0, len(prb.all_df), prb.popSize):
        fig1= px.scatter(prb.all_df[i: i+ prb.popSize], x="Total Crop Water Use (mm)", y="Yield (t/ha)")
        fig1.data[0]['marker']['color']= colours[count]
        fig1.data[0]['showlegend']= True
        fig1.data[0]['name'] = legends[count]
        fig.add_trace(fig1.data[0])
        count +=1
else:
    indivGroups= list(range(len(prb.all_df)))[0::prb.popSize]
    gensInterest= np.round(np.linspace(0, len(indivGroups) - 1, 5)).astype(int)
    groupsInterest=[indivGroups[x] for x in gensInterest]

    for i in range(len(groupsInterest)):
        fig1= px.scatter(prb.all_df[groupsInterest[i]: (groupsInterest[i]+ prb.popSize)], x="Total Crop Water Use (mm)", y="Yield (t/ha)")
        fig1.data[0]['marker']['color']= colours[i]
        fig1.data[0]['showlegend']= True
        fig1.data[0]['name'] = f'Generation {(gensInterest[i]+1)}'
        fig.add_trace(fig1.data[0])


fig.update_traces(mode="markers", marker=dict(size=12,line=dict(width=2, color='DarkSlateGrey')))
fig.update_layout(font_family='Courier New', font_size = 16, title_font_color = 'black', title="Objectives over Generations",
                title_x=0.5, template='plotly_white', width=1400, height=700)
fig.update_xaxes(title_text = "Total Crop Water Use (mm)", gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.update_yaxes(title_text = "Yield (t/ha)", gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
fig.show()



