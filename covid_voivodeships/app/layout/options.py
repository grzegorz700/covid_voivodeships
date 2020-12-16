from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from covid_voivodeships.app.ids import OptionsIDs
from covid_voivodeships.utils import only_value_from_dict
from covid_voivodeships.plots.daily_cases import color_map
from covid_voivodeships.voivodeship.data.utils import DEFAULT_START_DATE
from covid_voivodeships.voivodeship.utils import load_voiv_urls_with_names


voivodeship_links, voivodeship_names = load_voiv_urls_with_names()

_columns = ['Chorzy', 'Zarazeni', 'Wyleczeni', 'Zgony']
interested_columns_checklist = [{'label': v, 'value': v} for v in _columns]

colors = color_map(only_value_from_dict(interested_columns_checklist))

normalize_slider = dcc.Slider(
    min=0,
    max=7,
    step=None,
    marks={
        0: 'Brak',
        3: 'Średnia 3 dni',
        7: 'Średnia 7 dni',
    },
    value=0,
    id=OptionsIDs.MOVING_AVG
)

average_form_group = dbc.FormGroup([
    dbc.Label("Uśrednianie:", width=3),
    dbc.Col([normalize_slider], width=9)], #, sm=8, md=6, lg=4
    row=True)

normalization_form_group = dbc.FormGroup([
    dbc.Label("Normalizacja:", width=3),
    dbc.Col(dcc.RadioItems(id=OptionsIDs.NORMALIZATION, options=[
        {'label': ' Liczba bezwględna', 'value': 0},
        {'label': ' na 100 tyś przypadków', 'value': 1},
    ], value=0), width=8),
], row=True)


interested_data_form_group = dbc.FormGroup([
    dbc.Label("Co wyświetlić?", width=3),
    dbc.Col([dbc.Checklist(
        id=OptionsIDs.INTERESTED_DATA_PICKER,
        options=interested_columns_checklist,
        value=only_value_from_dict(interested_columns_checklist),
        labelStyle={'display': 'inline-block'},
        # 'background-color':['red', 'green','orange']},
        inline=True,
        switch=True)]
    ),
], row=True)

data_picker_form_group = dbc.FormGroup([
    dbc.Label("Wybierz zakres dat:", width=3),
    dbc.Col([dcc.DatePickerRange(
        id=OptionsIDs.DATE_RANGE,
        min_date_allowed=datetime(*DEFAULT_START_DATE),
        max_date_allowed=datetime.today(),
        # initial_visible_month=datetime(*DEFAULT_START_DATE),
        start_date=datetime(*DEFAULT_START_DATE),
        end_date=datetime.today(),
        display_format="DD.MM.YYYY",
        # config=dict(locale="pl")
        month_format="MM.YYYY")]),
], row=True)

common_scale_form_group = dbc.FormGroup([
    dbc.Label("Oś pionowa: ", width=3),
    dbc.Col([dbc.Checklist(id=OptionsIDs.COMMON_AXIS,
        options=[{"label": "Wspólna skala", "value": 0}],
        value=0,
        labelStyle={'display': 'inline-block'},
        inline=True,
        switch=True)
        ])
], row=True)

options = html.Div([
    dbc.Button(['Opcje ▼'], id=OptionsIDs.SHOW_OPTIONS_BTN, color="info", className="mr-1"),
    dbc.Button('Sprawdź aktualizacje', id=OptionsIDs.CHECK_UPDATE, n_clicks=0, className="mr-1"),
    dbc.Spinner(html.Div(id=OptionsIDs.UPDATE_SPINNER, className="mr-1")),
    dbc.Collapse(id=OptionsIDs.OPTIONS_COLLAPSE, children=dbc.Card(dbc.CardBody([
        dbc.Form([
            average_form_group,
            normalization_form_group,
            interested_data_form_group,
            dbc.Alert("Nie wybrano nic do wyświetlenia!",
                      id=OptionsIDs.NO_INTEREST_ALERT,
                      color="danger",
                      is_open=False,
                      ),
            data_picker_form_group,
            common_scale_form_group,
        ]),
        # columns_picker,
    ]), style={"width": "45rem"},))
], className="sticky-options", style={'margin-bottom': '10px'})

columns_picker = dcc.RadioItems(id=OptionsIDs.GRAPHS_COLUMNS_SWITCHER, options=[
            {'label': '4 columns', 'value': 4},
            {'label': '3 columns', 'value': 3},
            {'label': '2 columns', 'value': 2},
            {'label': '1 column', 'value':  1},
        ], value=4)
