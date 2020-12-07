import sys
import argparse

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


from datetime import datetime
import numpy as np
from unidecode import unidecode

from covid_voivodeships.app.geo.utils import get_geo_df, \
    get_map, load_geojson, show_id_to_voiv_name
from covid_voivodeships.app.ids import IDS
from covid_voivodeships.app.layout.graphs import hover_map_graph, graph_day_cases_per_week
from covid_voivodeships.app.layout.layout import main_layout, separate_maps, \
    graph_shape_of_spread, graph_day_change_piechart
from covid_voivodeships.app.layout.options import interested_columns_checklist
from covid_voivodeships.app.layout.utils import not_supported_tab
from covid_voivodeships.app.utils import _only_value_from_dict
from covid_voivodeships.plots.comparison import shape_of_spread_in_voivs
from covid_voivodeships.plots.daily_cases import plot_single_voiv, day_change_pie_chart, \
    get_separate_voiv_plots, avg_cases_per_days_per_population
from covid_voivodeships.storage.serialization import load_all_vols, save_all_vols
from covid_voivodeships.storage.structure import ProjectDataStructure
from covid_voivodeships.voivodeship.downloader import download_data
from covid_voivodeships.voivodeship.utils import _load_links_with_names

OLD_VERSION = False
LAST_CHANGE = None
LAST_CHANGE_OUTPUT = None

ps = ProjectDataStructure()
voivodeship_links, voivodeship_names = _load_links_with_names()
voivs = load_all_vols(ps, latest=True)
if voivs is None:
    voivs = download_data(voivodeship_names, voivodeship_links,
                          verbose=True)
    save_all_vols(ps, voivs)


# Layout preparation:
pl_voiv_geojson = load_geojson()
voiv_name_to_dic = show_id_to_voiv_name(pl_voiv_geojson)
df_ill_cases = get_geo_df(voivs, voiv_name_to_dic)
hover_map_graph.figure = get_map(df_ill_cases, pl_voiv_geojson)
graph_shape_of_spread.figure = shape_of_spread_in_voivs(voivs)
graph_day_change_piechart.figure = day_change_pie_chart(voivs)
graph_day_cases_per_week.figure = avg_cases_per_days_per_population(voivs)

app = dash.Dash(
    name=__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    external_scripts=["https://cdn.plot.ly/plotly-locale-pl-latest.js"],
    suppress_callback_exceptions=True,
    title='Koronawirus województwa'
)


app.layout = main_layout

@app.callback(Output(IDS.Tab.TAB_DIV_CONTENT, "children"),
              [Input(IDS.Tab.TAB_BAR, "active_tab")])
def switch_tab(active_tab):
    print("Activate tab:", active_tab)
    if active_tab == IDS.Tab.LINE_SPREAD:
        return graph_shape_of_spread
    elif active_tab == IDS.Tab.DAILY_PIECHART:
        return graph_day_change_piechart
    elif active_tab == IDS.Tab.VOIV_GRID:
        return separate_maps
    elif active_tab == IDS.Tab.CASES_PER_WEEK:
        return graph_day_cases_per_week
    return not_supported_tab


@app.callback(
    [Output(IDS.Options.OPTIONS_COLLAPSE, "is_open"),
     Output(IDS.Options.SHOW_OPTIONS_BTN, "children")],
    [Input(IDS.Options.SHOW_OPTIONS_BTN, "n_clicks")],
    [State(IDS.Options.OPTIONS_COLLAPSE, "is_open")],
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open, "Opcje ▲" if not is_open else "Opcje ▼"
    return is_open, "Opcje ▲" if is_open else "Opcje ▼"


# TODO: Przemyśleć
@app.callback(Output(IDS.Options.UPDATE_SPINNER, 'children'),
              [Input(IDS.Options.CHECK_UPDATE, 'n_clicks')])
def update_data(n_clicks):
    print("n_clicks: ", n_clicks)
    if n_clicks is not None and n_clicks > 0:
        global voivs
        #TODO: check if nessessary is update
        voivs = download_data(voivodeship_names, voivodeship_links, verbose=True)
        save_all_vols(ps, voivs)
        print('Updated')
        return "Updated " + str(datetime.now())
    else:
        raise PreventUpdate()


# TODO: Globale
@app.callback(#+[Output(IDS.Graphs.MAIN_SUBGRAPHS, "figure")]
              [Output(IDS.Graphs.get_main_separate_voiv_map_id(voiv_name), "figure")
               for voiv_name in voivodeship_names],
              [Input(IDS.Options.VOIVS_NAMES_DROPDOWN, "value"),
               #Input(IDS.Options.GRAPHS_COLUMNS_SWITCHER, "value"),
               Input(IDS.Options.NORMALIZATION, "value"),
               Input(IDS.Page.URL_PAGE_LOCATION, 'pathname'),
               Input(IDS.Options.MOVING_AVG, 'value'),
               Input(IDS.Options.INTERESTED_DATA_PICKER, 'value'),
               Input(IDS.Options.DATE_RANGE, 'start_date'),
               Input(IDS.Options.DATE_RANGE, 'end_date'),
               Input(IDS.Options.COMMON_AXIS, 'value')
               ])
def update_plots_grid(selected_voiv_names, normalize, pathname, moving_mean, columns,
                      start_date, end_date, with_shared_yaxis_lim):
    ctx = dash.callback_context
    global LAST_CHANGE
    global LAST_CHANGE_OUTPUT
    if LAST_CHANGE == ctx.triggered:
        print("Fix repreted update", ctx.triggered, file=sys.stderr)
        return LAST_CHANGE_OUTPUT
        # raise PreventUpdate()
    print('# Triggered: ', ctx.triggered)
    if pathname == ('/' + IDS.Page.DAILY_STATE):
        daily_change = False
    else:
        daily_change = True
    print(f'Update grid in time: {(datetime.now())}')

    #graph = figure_daily(voivs, voivodeship_names, DAILY_CHANGE=DAILY_CHANGE,
    #                        moving_mean=7, normalize=False, cols=columns)
    with_filled_chart = daily_change
    plots = get_separate_voiv_plots(voivs, voivodeship_names, selected_voiv_names, daily_change, normalize != 0,
                                    moving_mean, columns, with_filled_chart,
                                    start_date, end_date, with_shared_yaxis_lim)
    LAST_CHANGE_OUTPUT = plots
    LAST_CHANGE = ctx.triggered
    return LAST_CHANGE_OUTPUT
    #return [graph] #+ get_separate_voiv_plots(voivs, voivodeship_names,
    # selected_voiv_names, DAILY_CHANGE, normalize != 0)


@app.callback(Output(IDS.Page.HEADER, "children"),
              [Input(IDS.Page.URL_PAGE_LOCATION, 'pathname')])
def update_title(raw_path_name):
    path_name = raw_path_name[1:] if raw_path_name.startswith('/') else raw_path_name
    if path_name == IDS.Page.DAILY_STATE:
        title = "Stan zachorowań"
    elif path_name in ("", IDS.Page.DAILY_CHANGE):
        title = "Dzienne zmiany zachorowań"
    else:
        title = "Strona domyślna - sprawdź adres"
    print(f'Update view to: "{title}" in time: {(datetime.now())}')
    return title


@app.callback([Output(IDS.MAP_HOVER_HEADER, 'children'),
               Output(IDS.MAP_HOVER_GRAPH, 'figure'),
               Output(IDS.Badges.HEALTHY, 'children'),
               Output(IDS.Badges.ILL, 'children'),
               Output(IDS.Badges.DEAD, 'children')],
              [Input(IDS.MAP, 'hoverData')],
              [State(IDS.Page.URL_PAGE_LOCATION, 'pathname'),
               State(IDS.Options.NORMALIZATION, 'value'),
               State(IDS.Options.MOVING_AVG, 'value')])
def map_hover_data(hover_data, pathname, normalize, moving_mean):
    if hover_data is None:
        raise PreventUpdate()
    if pathname == ('/' + IDS.Page.DAILY_STATE):
        daily_change = False
    else:
        daily_change = True
    voiv_name = str(hover_data['points'][0]['hovertext'])
    print("Hover over: ", voiv_name.encode('utf-8'))
    voiv = voivs[unidecode(voiv_name)]
    plot = plot_single_voiv(voiv, daily_change=daily_change, moving_mean=moving_mean, normalize=normalize != 0)
    plot.update_layout(yaxis_title="", legend_title="Grupa osób")
    state = voiv.get_state_daily().iloc[-1:]
    badges = [state.Wyleczeni.values[0],
              state.Chorzy.values[0],
              state.Zgony.values[0]]
    badges = list(map(lambda val: 0 if np.isnan(val) else str(int(val)), badges))
    return [voiv_name.title(), plot] + badges


@app.callback(Output(IDS.MAP, 'figure'),
              [Input(IDS.Options.NORMALIZATION, "value")])
def map_normalize(normalize):
    df_ill_cases = get_geo_df(voivs, voiv_name_to_dic, normalize != 0)
    title = "Zakażenia"
    if normalize != 0:
        title += '<br>(na 100k ludności)'
    return get_map(df_ill_cases, pl_voiv_geojson, title)


@app.callback(Output(IDS.Graphs.DAY_CASES_PIECHART, 'figure'),
              [Input(IDS.Options.NORMALIZATION, 'value')])
def piechart_normalize(normalize):
    return day_change_pie_chart(voivs, normalize != 0)


@app.callback(
    [Output(IDS.Options.INTERESTED_DATA_PICKER, 'options'),
     Output(IDS.Options.INTERESTED_DATA_PICKER, 'value')],
    [Input(IDS.Page.URL_PAGE_LOCATION, 'pathname')]
)
def update_options_checklist(pathname):
    if pathname == '/day-state':
        return_list = interested_columns_checklist
    else:
        return_list = list(filter(lambda dct: dct['value'] != 'Chorzy',
                                  interested_columns_checklist))
    return return_list, _only_value_from_dict(return_list)


@app.callback(
    Output(IDS.Options.NO_INTEREST_ALERT, 'is_open'),
    [Input(IDS.Options.INTERESTED_DATA_PICKER, 'value')]
)
def alert_no_columns(columns):
    return len(columns) == 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--update', help='Update data before start', action='store_true')
    args = parser.parse_args()
    if args.update:
        voivs = download_data(voivodeship_names, voivodeship_links,
                              verbose=True)
        save_all_vols(ps, voivs)
    app.run_server(debug=True)
