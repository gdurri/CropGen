import plotly.express as px

from lib.constants import Constants

class GraphGenerator():
  def _generate_design_space_graph(self, opt_data_frame, bounds):
    design_space_graph = px.scatter(
      opt_data_frame, 
      x = Constants.END_JUV_TO_FI_THERMAL_TIME, 
      y = Constants.FERTILE_TILLER_NUMBER, 
      title="Design Space", 
      template = Constants.GRAPH_PLOT_TYPE,
      hover_data = {
        Constants.TOTAL_CROP_WATER_USE_MM: ':.2f', 
        Constants.YIELD_HA: ':.2f', 
        Constants.END_JUV_TO_FI_THERMAL_TIME: False, 
        Constants.FERTILE_TILLER_NUMBER: False
      },
      width = Constants.GRAPH_WIDTH,
      height = Constants.GRAPH_HEIGHT
    )
    
    design_space_graph.update_traces(mode=Constants.GRAPH_MODE_MARKERS, marker=dict(size=12, line=dict(width=2, color=Constants.GRAPH_GRID_COLOUR_SLATE_GRAY)))
    design_space_graph.update_layout(font_family=Constants.GRAPH_FONT, font_size = Constants.GRAPH_FONT_SIZE, title_font_color = Constants.GRAPH_FONT_COLOUR, title_x=Constants.GRAPH_TITLE_X)
    design_space_graph.update_xaxes(range=[bounds[0], bounds[0]], gridcolor=Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY, mirror= True, ticks=Constants.GRAPH_TICKS, showline=True,linecolor= Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY)
    design_space_graph.update_yaxes(range=[bounds[1], bounds[1]], gridcolor=Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY, mirror= True, ticks=Constants.GRAPH_TICKS, showline=True,linecolor= Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY)
    return design_space_graph

  def _generate_objective_space_graph(self, opt_data_frame):
    objective_space_graph = px.scatter(
      opt_data_frame, 
      x = Constants.TOTAL_CROP_WATER_USE_MM, 
      y = Constants.YIELD_HA, 
      title = "Objective Space", 
      template = Constants.GRAPH_PLOT_TYPE,
      hover_data = {
        Constants.TOTAL_CROP_WATER_USE_MM: False, 
        Constants.YIELD_HA: False, 
        Constants.END_JUV_TO_FI_THERMAL_TIME: ':.2f', 
        Constants.FERTILE_TILLER_NUMBER: ':.2f'
      },
      width = Constants.GRAPH_WIDTH,
      height = Constants.GRAPH_HEIGHT
    )
    
    objective_space_graph.update_traces(mode=Constants.GRAPH_MODE_MARKERS, marker=dict(size=12,line=dict(width=2, color=Constants.GRAPH_GRID_COLOUR_SLATE_GRAY)))
    objective_space_graph.update_layout(font_family=Constants.GRAPH_FONT, font_size = Constants.GRAPH_FONT_SIZE, title_font_color = Constants.GRAPH_FONT_COLOUR, title_x=Constants.GRAPH_TITLE_X)
    objective_space_graph.update_xaxes(gridcolor=Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY, mirror= True, ticks=Constants.GRAPH_TICKS, showline=True,linecolor= Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY)
    objective_space_graph.update_yaxes(gridcolor=Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY, mirror= True, ticks=Constants.GRAPH_TICKS, showline=True,linecolor= Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY)
    return objective_space_graph
