import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from covid_voivodeships.app.ids import IDS

tabs = html.Div([
    dbc.Tabs(
        [
            dbc.Tab(label="Wojewodztwa siatka", tab_id=IDS.Tab.VOIV_GRID),
            dbc.Tab(label="Skala zachorowalności w czasie",
                    tab_id=IDS.Tab.LINE_SPREAD),
            dbc.Tab(label="Udział dziennych przypadków", tab_id=IDS.Tab.DAILY_PIECHART),
            dbc.Tab(label="Liczba przypadków przez 7 dni",
                    tab_id=IDS.Tab.CASES_PER_WEEK),
        ],
        id=IDS.Tab.TAB_BAR,
        active_tab=IDS.Tab.VOIV_GRID,
    ),
    html.Div(id=IDS.Tab.TAB_DIV_CONTENT),
])

navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Dzienna zmiany", href='/' + IDS.Page.DAILY_CHANGE)),
            dbc.NavItem(dbc.NavLink("Dzienny stan", href='/' + IDS.Page.DAILY_STATE)),
        ],
        brand="Koronawirus w województwach",
        brand_href="#",
        color="primary",
        dark=True,
        # sticky="top",
        # style={'height': '45px'},
)
page_location = dcc.Location(id=IDS.Page.URL_PAGE_LOCATION, refresh=False)