from pathlib import Path
import pandas as pd
import plotly.express as px
import logging
import sys


# Sets up the logger
def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

#
def plot_graph_for_csv(
    csv_file, 
    input_trait_one_name, 
    input_trait_one_key_name,
    input_trait_two_name, 
    input_trait_two_key_name,
    objective_one_name,
    objective_two_name
):

    df = pd.read_csv(csv_file)

    column_headings = df.columns.tolist()

    fig = px.scatter(
        df, 
        x=input_trait_one_name, 
        y=input_trait_two_name, 
        template='plotly_white', 
        width=900, 
        height=600, 
        color=objective_one_name, 
        hover_data={objective_one_name: ':.2f', objective_two_name: ':.2f'},
        title=Path(csv_file).stem
    )

    fig.update_traces(mode="markers", marker=dict(size=20, opacity=1, line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(font_family='Courier New', font_size = 22, title_font_color = 'black', title_x=0.5, coloraxis_colorbar=dict(title = 'Yield (t/ha)'))
    fig.update_xaxes(title= f'<b>{input_trait_one_key_name}<b>', gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
    fig.update_xaxes(range =[130,190], tickprefix="<b>",ticksuffix ="</b><br>")
    fig.update_yaxes(range= [3,10], tickprefix="<b>",ticksuffix ="</b><br>")
    fig.update_yaxes(title= f'<b>{input_trait_two_key_name}<b>', gridcolor='lightgray', mirror= True, ticks='outside', showline=True,linecolor= 'lightgray')
    fig.show()


# Main entry point.
if __name__ == '__main__':
    setup_logging()

    # Example usage:
    # python plot_graph.py optimal_individuals_JobID-13.csv all_individuals_JobID-13.csv

    if len(sys.argv) != 3:
        print("Usage: python plot_graph <optimal_individuals_csv_file> <all_individuals_csv_file>")
        sys.exit(1)

    optimal_csv_file = sys.argv[1].lower()
    all_individuals_csv_file = sys.argv[2].lower()

    input_trait_one_name = '[Sorghum].Phenology.TTEndJuvToInit.FixedValue'
    input_trait_one_key_name = 'Maturity (DD)'
    input_trait_two_name = '[FixedSowing].Script.Density'
    input_trait_two_key_name = 'Planting Density (/m2)'
    objective_one = 'Yield'
    objective_two = 'Evapotranspiration'

    plot_graph_for_csv(optimal_csv_file, input_trait_one_name, input_trait_one_key_name, input_trait_two_name, input_trait_two_key_name, objective_one, objective_two)
    plot_graph_for_csv(all_individuals_csv_file, input_trait_one_name, input_trait_one_key_name, input_trait_two_name, input_trait_two_key_name, objective_one, objective_two)
