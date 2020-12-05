import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from covid_voivodeships.app.ids import GraphIDs, IDS
from covid_voivodeships.app.layout.utils import hover_state_badges
from covid_voivodeships.plots.daily_cases import figure_daily

import plotly.graph_objects as go

GRAPH_HEIGHT = 200


hover_map_graph = dcc.Graph(
    id=IDS.MAP, style={'height': '450px'},
    config={'scrollZoom': False,
            'showAxisRangeEntryBoxes': False,
            'showAxisDragHandles': False}
)


def empty_plot(label_annotation):
    '''
    Returns an empty plot with a centered text.
    '''

    trace1 = go.Scatter(
        x=[],
        y=[]
    )

    data = [trace1]

    layout = go.Layout(
        showlegend=False,
        xaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
        ),
        yaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
        ),
        annotations=[
            dict(
                x=0,
                y=0,
                xref='x',
                yref='y',
                text=label_annotation,
                font=dict(size=25),
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=0
            )
        ]
    )

    fig = go.Figure(data=data, layout=layout)
    # END
    return fig


_empty_plot_figure = empty_plot('🖱 Aby zobaczyć wykres <br> najedź na <br>'
                               'wybrane województwo')
map_with_graph_panel = html.Div(children=[
        dbc.Row([
            dbc.Col([hover_map_graph], sm=12, md=4, lg=4),
            dbc.Col([html.Div([hover_state_badges,
                    html.H2(id=IDS.MAP_HOVER_HEADER,
                            style={'display': 'inline-block',
                                   'vertical-align': 'left',
                                   'margin-left': '10px'}),
                    dcc.Graph(id=IDS.MAP_HOVER_GRAPH,
                              config=dict(locale='pl'),
                              figure=_empty_plot_figure)])],
                    sm=12, md=8, lg=8)
        ])
    ])


def get_graphs_grid_separate_graphs(voivodeship_names):
    _separate_main_maps = []
    for voiv_name in voivodeship_names:
        _separate_main_maps.append(
            dcc.Graph(id=GraphIDs.get_main_separate_voiv_map_id(voiv_name),
                      config=dict(locale="pl"),
                      style={'height': f'{GRAPH_HEIGHT}px'}))

    separate_maps = dbc.Spinner(html.Div(children=[
        dbc.Row(id=GraphIDs.GRAPHS_ROW, children=[
            dbc.Col(graph, sm=12, md=6, lg=3) for graph in _separate_main_maps])
        ],
        style={'width': '95vw'}),
        spinner_style={"width": f"{4*GRAPH_HEIGHT}px",
                       "height": f"{4*GRAPH_HEIGHT}px",
                       "border": f"40px solid currentColor",
                       "border-right-color": "transparent"},
        color="info")
    return separate_maps


def get_graphs_grid_as_subplots(voivs, voivodeship_names):
    graph = figure_daily(voivs, voivodeship_names, daily_change=False,
                         moving_mean=0, normalize=False)
    subplots_maps = html.Div(children=[
        dcc.Graph(id=GraphIDs.MAIN_SUBGRAPHS, style={'height': '80vh'}, figure=graph)
        ], className="d-none d-lg-block")
    return subplots_maps


graph_shape_of_spread = dcc.Graph(id=GraphIDs.SHAPE_OF_SPREAD,
                 style={'height': '600px'},
                 config=dict(locale='pl'))

graph_day_change_piechart = dcc.Graph(id=GraphIDs.DAY_CASES_PIECHART,
                     style={'height': '600px'})

graph_day_cases_per_week = dcc.Graph(id=GraphIDs.DAY_CASES_PER_WEEK,
                     style={'height': '600px'})


