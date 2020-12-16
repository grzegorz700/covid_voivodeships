from datetime import datetime
import locale

import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
from matplotlib import colors

from covid_voivodeships.voivodeship.data.utils import fill_missing_dates, normalize_by_population

_VOIV_COUNT = 16


def color_map(columns):
    col_map_dic = {
        'Chorzy': 'orange',
        'Wyleczeni': 'green',
        'Zarazeni': 'red',
        'Zgony': 'black',
    }
    return [col_map_dic[c] for c in columns]


def figure_daily(voivs, voivodeship_names, daily_change=False, moving_mean=0,
                 normalize=False, cols=4):
    locale.setlocale(locale.LC_TIME, "pl_PL.utf8")
    titles = [voivs[vol_name].full_name for vol_name in voivodeship_names]
    rows = int(np.ceil(_VOIV_COUNT/cols))
    fig = make_subplots(rows=rows, cols=cols,
                        subplot_titles=titles,
                        shared_xaxes='all')
    show_legend = True
    for idx, vol_name in enumerate(voivodeship_names):
        voiv = voivs[vol_name]
        fig_voiv = plot_single_voiv(voiv, daily_change, moving_mean, normalize)
        for trace in fig_voiv['data']:
            if not show_legend:
                trace.showlegend = False
            fig.add_trace(trace, row=int(idx/cols)+1, col=idx % cols + 1)
        show_legend = False
    fig.update_layout(title_text="Dzienne zmiany")
    return fig


def figure_daily_v2(voivs, voivodeship_names, daily_change=False, moving_mean=0,
                 normalize=False, cols=4, columns=None, filled_area=False,
                 start_date=None, end_date=None, with_shared_yaxis_lim=True):
    locale.setlocale(locale.LC_TIME, "pl_PL.utf8")
    #titles = [voivs[vol_name].full_name for vol_name in voivodeship_names]
    figs = []
    for idx, vol_name in enumerate(voivodeship_names):
        voiv = voivs[vol_name]
        single_plot = plot_single_voiv(
            voiv, daily_change, moving_mean, normalize, voiv.full_name, columns,
            filled_area, start_date=start_date, end_date=end_date)
        figs.append(single_plot)

    if with_shared_yaxis_lim:
        data = []
        for fig in figs:
            data += [np.nanmax(trace_data['y']) for trace_data in fig.data]
        y_max = np.ceil(np.max(data)*1.03)
        for fig in figs:
            fig.update_layout(yaxis=dict(range=[0, y_max]))
    return figs


def plot_single_voiv(voiv, daily_change, moving_mean, normalize, title=None,
                     columns=None, filled_area=False, start_date=None,
                     end_date=None):
    if daily_change:
        data = voiv.get_daily_change()
    else:
        data = voiv.get_state_daily()
    if moving_mean > 0:
        data = data.rolling(window=moving_mean).mean()
    if normalize:
        data = normalize_by_population(voiv, data)
    data = data.sort_index()
    data = fill_missing_dates(data)
    data_columns = list(data.columns)
    if data.Zgony.dtype == 'O':
        data_columns.remove('Zgony')
    if columns is not None:
        data_columns = [dc for dc in data_columns if dc in columns]
    x = data.index
    if len(data_columns) == 0:
        return px.line()

    if start_date is not None or end_date is not None:
        range_x = (start_date, end_date)
    else:
        range_x = None
    if filled_area:
        fig_voiv = go.Figure()
        for col in data_columns:
            color = color_map([col])[0]
            color_rgba = colors.to_rgba(color, 0.65)
            color_rgba_str = f"rgba{color_rgba}"
            scatter = go.Scatter(x=x, y=data[col], fill='tozeroy', mode='none',
                                 name=col, fillcolor=color_rgba_str)
            fig_voiv.add_trace(scatter)
        fig_voiv.update_layout(title=title)
        if range_x is not None:
            fig_voiv.update_layout(xaxis=dict(range=range_x))
    else:
        fig_voiv = px.line(data, x=x, y=data_columns, range_x=range_x,
                           color_discrete_sequence=color_map(data_columns),
                           title=title)
    return fig_voiv


def day_change_pie_chart(voivs, normalize=False):
    data_parts = []
    for voiv_name, voiv in voivs.items():
        last_date_row = voiv.get_daily_change().iloc[-2:]
        val_columns = ["Zarazeni", "Wyleczeni", "Zgony"]
        if normalize:
            real_values_df = last_date_row[val_columns].astype(np.float)  # Bugfixed: Convert here is important!
            last_date_row[val_columns] = normalize_by_population(
                voiv, real_values_df, per_100k=True)
        last_date_row['Voivodeship'] = voiv_name
        data_parts.append(last_date_row)
    df = pd.concat(data_parts)

    # Get only last day with full information:
    dates = np.unique(df.index.values)
    date_to_display = sorted(dates)[-1]
    df_oneday = df[df.index == date_to_display]
    if len(df_oneday) < _VOIV_COUNT:
        date_to_display = sorted(dates)[-2]
        df_oneday = df[df.index == date_to_display]
    ns = 1e-9  # number of seconds in a nanosecond
    date_to_display = datetime.utcfromtimestamp(
        date_to_display.astype(int) * ns)  # convert datetime64[ns] to string
    date_to_display_str = date_to_display.strftime('%Y-%m-%d')
    if date_to_display.date() == datetime.today().date():
        date_to_display_str += " (Dziś)"
    else:
        date_to_display_str += " (Dane z poprzedniego dnia)"
    fig = px.pie(df_oneday, values='Zarazeni', names='Voivodeship',
                 title=date_to_display_str)
    fig.update_traces(textposition='inside', textinfo='percent+label+value')
    return fig


def avg_cases_per_days_per_population(voivs):
    data_frames = []
    for vol_name, vol in voivs.items():
        df = vol.get_number_of_cases_normalized()
        data_frames.append(df)
    rdf = pd.concat(data_frames, axis=1)
    rdf = rdf.loc[:, ~rdf.columns.duplicated()]
    rdf = rdf.diff().rolling(7).mean()

    dfpx = pd.melt(rdf.reset_index(), id_vars='Data', var_name='Region',
                   value_name='Przypadki/100k')
    dfpx=dfpx.sort_values(["Region", "Data"])
    fig = px.line(dfpx, x="Data", y='Przypadki/100k',
                  title='Średnia liczba przypadków przez 7 dni na 100 tyś. populacji',
                  line_group="Region", hover_name="Region", color="Region")
    fig.update_layout(xaxis=dict(
                        rangeselector=dict(
                            buttons=list([
                                dict(count=1,
                                     label="1m",
                                     step="month",
                                     stepmode="backward"),
                                dict(count=2,
                                     label="2m",
                                     step="month",
                                     stepmode="backward"),
                                dict(count=6,
                                     label="6m",
                                     step="month",
                                     stepmode="backward"),
                                dict(step="all")
                            ])
                        ),
                        rangeslider=dict(
                            visible=True
                        ))
    )
    fig.add_hline(y=10, annotation_text='Strefa żółta',
                  line_dash='dot', line_color='yellow',
                  annotation_position='top left')
    fig.add_hline(y=25, annotation_text='Strefa czerwona',
                  line_dash='dot', line_color='red',
                  annotation_position='top left')
    fig.add_hline(y=50, annotation_text='Bezpiecznik',
                  line_dash='dot', line_color='purple',
                  annotation_position='top left')
    fig.add_hline(y=70, annotation_text='Lockdown',
                  line_dash='dot', line_color='purple',
                  annotation_position='top left')
    return fig


def get_separate_voiv_plots(voivs, voivodeship_names, daily_change=False,
                            normalize=False, moving_mean=0, columns=None,
                            filled_area=False, start_date=None, end_date=None,
                            with_shared_yaxis_lim=False):
    print("Request: plot separate")
    figs = figure_daily_v2(voivs, voivodeship_names, daily_change=daily_change,
                           moving_mean=moving_mean, normalize=normalize,
                           columns=columns, filled_area=filled_area,
                           start_date=start_date, end_date=end_date,
                           with_shared_yaxis_lim=with_shared_yaxis_lim)
    graphs = []
    show_legend = True
    for idx, vol_name in enumerate(voivodeship_names):
        fig = figs[idx]
        fig.update_layout(
            showlegend=show_legend,
            legend=dict(orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                        ),
            margin={'l': 0,'r': 0, 't': 50, 'b': 0},
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=3,
                             label="3m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        #dict(count=1,
                        #     label="YTD",
                        #     step="year",
                        #     stepmode="todate"),
                        dict(count=1,
                             label="1rok",
                             step="year",
                             stepmode="backward"),
                        dict(label="Całość",
                            step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=False  # False - default value
                ),
                type="date"
            )
        )
        graphs.append(fig)
        show_legend = False
    return graphs