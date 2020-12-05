import dash_bootstrap_components as dbc
import dash_html_components as html

from covid_voivodeships.app.ids import BadgesIDs, IDS

BADGE_WIDTH = 55
_badge_style = {"width": f"{BADGE_WIDTH}px", "text-align": "right"}
hover_state_badges = html.H5([
    dbc.Badge("Zdrowi", color='success', id=BadgesIDs.HEALTHY, style=_badge_style),
    dbc.Tooltip("Zdrowi", target=BadgesIDs.HEALTHY),
    dbc.Badge("Chorzy", color='warning', id=BadgesIDs.ILL, style=_badge_style),
    dbc.Tooltip("Chorzy", target=BadgesIDs.ILL),
    dbc.Badge("Zmarli", color='dark', id=BadgesIDs.DEAD, style=_badge_style),
    dbc.Tooltip("Zmarli", target=BadgesIDs.DEAD)],
    style={'display': 'inline-block', 'vertical-align': 'left', 'margin': 'auto'})

header = html.Div([
    dbc.Label("Ostatnia aktualizacja: ", id=IDS.Page.LAST_UPDATE), # TODO: add this function based on downoaded data
    html.H1(id=IDS.Page.HEADER)
])

not_supported_tab = html.P("Not supported tab")
