import plotly.express as px

from lib.constants import Constants

class GraphGenerator():
  PRECISION = ':.2f'

  def _generate_design_space_graph_single_year(self, opt_data_frame, bounds):
    return self._generate_graph(
      opt_data_frame,
      Constants.GRAPH_TITLE_DESIGN_SPACE,
      Constants.END_JUV_TO_FI_THERMAL_TIME,
      Constants.FERTILE_TILLER_NUMBER,
      {
        Constants.TOTAL_CROP_WATER_USE_MM: self.PRECISION,
        Constants.YIELD_HA: self.PRECISION,
        Constants.END_JUV_TO_FI_THERMAL_TIME: False, 
        Constants.FERTILE_TILLER_NUMBER: False,
      },
      bounds
    )

  def _generate_design_space_graph_multi_year(self, opt_data_frame, bounds):
    return self._generate_graph(
      opt_data_frame,
      Constants.GRAPH_TITLE_DESIGN_SPACE,
      Constants.END_JUV_TO_FI_THERMAL_TIME,
      Constants.FERTILE_TILLER_NUMBER,
      {
        Constants.FAILURE_RISK_YIELD_HA: self.PRECISION,
        Constants.YIELD_HA: self.PRECISION,
        Constants.END_JUV_TO_FI_THERMAL_TIME: False, 
        Constants.FERTILE_TILLER_NUMBER: False,
      },
      bounds
    )

  def _generate_objective_space_graph_single_year(self, opt_data_frame):
    return self._generate_graph(
      opt_data_frame,
      Constants.GRAPH_TITLE_OBJECTIVE_SPACE,
      Constants.TOTAL_CROP_WATER_USE_MM,
      Constants.YIELD_HA,
      {
        Constants.TOTAL_CROP_WATER_USE_MM: False, 
        Constants.YIELD_HA: False,
        Constants.END_JUV_TO_FI_THERMAL_TIME: self.PRECISION,
        Constants.FERTILE_TILLER_NUMBER: self.PRECISION
      }
    )

  def _generate_objective_space_graph_multi_year(self, opt_data_frame):
    return self._generate_graph(
      opt_data_frame,
      Constants.GRAPH_TITLE_OBJECTIVE_SPACE,
      Constants.FAILURE_RISK_YIELD_HA,
      Constants.YIELD_HA,
      {
        Constants.FAILURE_RISK_YIELD_HA: False,
        Constants.YIELD_HA: False,
        Constants.END_JUV_TO_FI_THERMAL_TIME: self.PRECISION,
        Constants.FERTILE_TILLER_NUMBER: self.PRECISION
      }
    )

  def _generate_all_individuals_graph_single_year(self, all_df, bounds):
    return self._generate_graph(
      all_df,
      Constants.GRAPH_TITLE_ALL_INDIVIDUALS,
      Constants.END_JUV_TO_FI_THERMAL_TIME,
      Constants.FERTILE_TILLER_NUMBER,
      {
        Constants.TOTAL_CROP_WATER_USE_MM: self.PRECISION,
        Constants.YIELD_HA: self.PRECISION,
        Constants.END_JUV_TO_FI_THERMAL_TIME: False,
        Constants.FERTILE_TILLER_NUMBER: False
      },
      bounds
    )

  def _generate_all_individuals_graph_multi_year(self, all_df, bounds):
    return self._generate_graph(
      all_df,
      Constants.GRAPH_TITLE_ALL_INDIVIDUALS,
      Constants.END_JUV_TO_FI_THERMAL_TIME,
      Constants.FERTILE_TILLER_NUMBER,
      {
        Constants.FAILURE_RISK_YIELD_HA: self.PRECISION,
        Constants.YIELD_HA: self.PRECISION,
        Constants.END_JUV_TO_FI_THERMAL_TIME: False,
        Constants.FERTILE_TILLER_NUMBER: False
      },
      bounds
    )
  
  def _generate_all_objectives_graph_single_year(self, all_df):
    return self._generate_graph(
      all_df,
      Constants.GRAPH_TITLE_ALL_OBJECTIVES,
      Constants.TOTAL_CROP_WATER_USE_MM,
      Constants.YIELD_HA,
      {
        Constants.TOTAL_CROP_WATER_USE_MM: False,
        Constants.YIELD_HA: False,
        Constants.END_JUV_TO_FI_THERMAL_TIME: self.PRECISION,
        Constants.FERTILE_TILLER_NUMBER: self.PRECISION
      }
    )

  def _generate_all_objectives_graph_multi_year(self, all_df):
    return self._generate_graph(
      all_df,
      Constants.GRAPH_TITLE_ALL_OBJECTIVES,
      Constants.FAILURE_RISK_YIELD_HA,
      Constants.YIELD_HA,
      {
        Constants.FAILURE_RISK_YIELD_HA: False,
        Constants.YIELD_HA: False,
        Constants.END_JUV_TO_FI_THERMAL_TIME: self.PRECISION,
        Constants.FERTILE_TILLER_NUMBER: self.PRECISION
      }
    )

  def _generate_yield_over_maturity_graph_single_year(self, all_df):
    return self._generate_graph(
      all_df,
      Constants.GRAPH_TITLE_YIELD_OVER_MATURITY,
      Constants.END_JUV_TO_FI_THERMAL_TIME,
      Constants.YIELD_HA,
      {
        Constants.TOTAL_CROP_WATER_USE_MM: self.PRECISION,
        Constants.YIELD_HA: False,
        Constants.END_JUV_TO_FI_THERMAL_TIME: False,
        Constants.FERTILE_TILLER_NUMBER: self.PRECISION
      }
    )

  def _generate_yield_over_maturity_graph_multi_year(self, all_df):
    return self._generate_graph(
      all_df,
      Constants.GRAPH_TITLE_YIELD_OVER_MATURITY,
      Constants.END_JUV_TO_FI_THERMAL_TIME,
      Constants.YIELD_HA,
      {
        Constants.FAILURE_RISK_YIELD_HA: self.PRECISION,
        Constants.YIELD_HA: False,
        Constants.END_JUV_TO_FI_THERMAL_TIME: False,
        Constants.FERTILE_TILLER_NUMBER: self.PRECISION
      }
    )

  def _generate_graph(
    self, 
    opt_data_frame, 
    graph_title,
    x_axis_value, 
    y_axis_value,
    hover_data,
    bounds = None    
  ):
    graph = px.scatter(
      opt_data_frame, 
      x = x_axis_value, 
      y = y_axis_value, 
      title = graph_title,
      template = Constants.GRAPH_PLOT_TYPE,
      hover_data = hover_data,
      width = Constants.GRAPH_WIDTH,
      height = Constants.GRAPH_HEIGHT
    )

    self._add_graph_extras(graph, bounds)
    return graph

  def _add_graph_extras(self, graph, bounds = None):

    graph.update_traces(mode=Constants.GRAPH_MODE_MARKERS, marker=dict(size=12,line=dict(width=2, color=Constants.GRAPH_GRID_COLOUR_SLATE_GRAY)))
    graph.update_layout(font_family=Constants.GRAPH_FONT, font_size = Constants.GRAPH_FONT_SIZE, title_font_color = Constants.GRAPH_FONT_COLOUR, title_x=Constants.GRAPH_TITLE_X)

    if bounds == None:
      graph.update_xaxes(gridcolor=Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY, mirror= True, ticks=Constants.GRAPH_TICKS, showline=True,linecolor= Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY)
      graph.update_yaxes(gridcolor=Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY, mirror= True, ticks=Constants.GRAPH_TICKS, showline=True,linecolor= Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY)
    else: 
      graph.update_xaxes(range=[bounds[0], bounds[0]], gridcolor=Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY, mirror= True, ticks=Constants.GRAPH_TICKS, showline=True,linecolor= Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY)
      graph.update_yaxes(range=[bounds[1], bounds[1]], gridcolor=Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY, mirror= True, ticks=Constants.GRAPH_TICKS, showline=True,linecolor= Constants.GRAPH_GRID_COLOUR_LIGHT_GRAY)
