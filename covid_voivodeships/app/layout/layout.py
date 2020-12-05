"""Preparation of the structure of the main layout without data
"""
import dash_html_components as html

from covid_voivodeships.app.layout.graphs import get_graphs_grid_separate_graphs, \
    map_with_graph_panel, graph_shape_of_spread, \
    graph_day_change_piechart
from covid_voivodeships.app.layout.navigation import navbar, page_location, tabs
from covid_voivodeships.app.layout.options import options
from covid_voivodeships.app.layout.utils import header
from covid_voivodeships.voivodeship.utils import _load_links_with_names

_, _voivodeship_names = _load_links_with_names()

main_layout = html.Div([
    navbar,
    page_location,
    # dcc.Link('DailyState', href='/'+IDS.Page.DAILY_STATE),
    # dcc.Link('DailyChange', href='/'+IDS.Page.DAILY_CHANGE),
    html.Div(children=[
        header,
        options,
        map_with_graph_panel,
        # get_graphs_grid_as_subplots(voivs, voivodeship_names),
        tabs,
    ], style={'marginLeft': 10, 'marginRight': 10, 'marginTop': 10,
              'marginBottom': 10})
])


separate_maps = get_graphs_grid_separate_graphs(_voivodeship_names)
graph_shape_of_spread
graph_day_change_piechart

