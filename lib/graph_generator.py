import plotly.express as px

from lib.constants import Constants

class GraphGenerator():
  def _generate_design_space_graph_single_year(self, opt_data_frame, bounds):
    return self._generate_design_space_graph(
      opt_data_frame,
      Constants.END_JUV_TO_FI_THERMAL_TIME,
      Constants.FERTILE_TILLER_NUMBER,
      Constants.TOTAL_CROP_WATER_USE_MM,
      Constants.FERTILE_TILLER_NUMBER,
      bounds
    )

  def _generate_design_space_graph_multi_year(self, opt_data_frame, bounds):
    return self._generate_design_space_graph(
      opt_data_frame,
      Constants.END_JUV_TO_FI_THERMAL_TIME,
      Constants.FERTILE_TILLER_NUMBER,
      Constants.FAILURE_RISK_YIELD_HA,
      Constants.FERTILE_TILLER_NUMBER,
      bounds
    )    

  def _generate_design_space_graph(self, opt_data_frame, x, y, f1, f2, bounds):
    design_space_graph = px.scatter(
      opt_data_frame, 
      x = x, 
      y = y, 
      title = Constants.GRAPH_TITLE_DESIGN_SPACE, 
      template = Constants.GRAPH_PLOT_TYPE,
      hover_data = {
        f1: ':.2f', 
        f2: ':.2f', 
        x: False, 
        y: False
      },
      width = Constants.GRAPH_WIDTH,
      height = Constants.GRAPH_HEIGHT
    )
    
    design_space_graph.update_traces(mode=Constants.GRAPH_MODE_MARKERS, marker=dict(size=12, line=dict(width=2, color=Constants.GRAPH_GRID_COLOUR_SLATE_GRAY)))
    design_space_graph.update_layout(font_family=Constants.GRAPH_FONT, font_size = Constants.GRAPH_FONT_SIZE, title_font_color = Constants.GRAPH_FONT_COLOUR, title_x=Constants.GRAPH_TITLE_X)
    design_space_graph.update_xaxes(range=[bounds[0], bounds[0]], gridcolor=Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY, mirror= True, ticks=Constants.GRAPH_TICKS, showline=True,linecolor= Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY)
    design_space_graph.update_yaxes(range=[bounds[1], bounds[1]], gridcolor=Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY, mirror= True, ticks=Constants.GRAPH_TICKS, showline=True,linecolor= Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY)
    return design_space_graph

  def _generate_objective_space_graph_single_year(self, opt_data_frame):
    return self._generate_objective_space_graph(
      opt_data_frame, 
      Constants.TOTAL_CROP_WATER_USE_MM,
      Constants.YIELD_HA, 
      Constants.END_JUV_TO_FI_THERMAL_TIME,
      Constants.FERTILE_TILLER_NUMBER
    )

  def _generate_objective_space_graph_multi_year(self, opt_data_frame):
    return self._generate_objective_space_graph(
      opt_data_frame,
      Constants.END_JUV_TO_FI_THERMAL_TIME,
      Constants.FERTILE_TILLER_NUMBER,
      Constants.FAILURE_RISK_YIELD_HA,
      Constants.YIELD_HA      
    )

  def _generate_objective_space_graph(self, opt_data_frame, x, y, f1, f2):
    objective_space_graph = px.scatter(
      opt_data_frame, 
      x = x, 
      y = y, 
      title = Constants.GRAPH_TITLE_OBJECTIVE_SPACE,
      template = Constants.GRAPH_PLOT_TYPE,
      hover_data = {
        f1: False,
        f2: False,
        x: ':.2f', 
        y: ':.2f'
      },
      width = Constants.GRAPH_WIDTH,
      height = Constants.GRAPH_HEIGHT
    )
    
    objective_space_graph.update_traces(mode=Constants.GRAPH_MODE_MARKERS, marker=dict(size=12,line=dict(width=2, color=Constants.GRAPH_GRID_COLOUR_SLATE_GRAY)))
    objective_space_graph.update_layout(font_family=Constants.GRAPH_FONT, font_size = Constants.GRAPH_FONT_SIZE, title_font_color = Constants.GRAPH_FONT_COLOUR, title_x=Constants.GRAPH_TITLE_X)
    objective_space_graph.update_xaxes(gridcolor=Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY, mirror= True, ticks=Constants.GRAPH_TICKS, showline=True,linecolor= Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY)
    objective_space_graph.update_yaxes(gridcolor=Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY, mirror= True, ticks=Constants.GRAPH_TICKS, showline=True,linecolor= Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY)
    return objective_space_graph

  def _generate_all_objectives_graph(self, all_df):
    objective_space_graph = px.scatter(
      all_df, 
      x = Constants.FAILURE_RISK_YIELD_HA, 
      y = Constants.YIELD_HA, 
      title = Constants.GRAPH_TITLE_ALL_OBJECTIVES,
      template = Constants.GRAPH_PLOT_TYPE,
      hover_data = {
        Constants.FAILURE_RISK_YIELD_HA: False,
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
