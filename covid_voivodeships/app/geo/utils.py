import sys

import json
import os
import pandas as pd
import numpy as np

import plotly.express as px

from covid_voivodeships.voivodeship.data.utils import normalize_by_population
from covid_voivodeships.storage.structure import ProjectDataStructure


def load_geojson(detailed=True):
    ps = ProjectDataStructure()
    if detailed:
        json_path = 'wojewodztwa-min.geojson'
    else:
        json_path = 'poland-provinces.json'
    pl_voiv_geojson_file_path = os.path.join(ps.data_dir, 'topologies', json_path)
    with open(pl_voiv_geojson_file_path, encoding='UTF-8') as pl_voiv_geojson_f:
        pl_voiv_geojson = json.load(pl_voiv_geojson_f)
    return pl_voiv_geojson


def show_id_to_voiv_name(geojson):
    fts = geojson['features']
    name_to_id_dic = {}
    for voiv_dic in fts:
        name = voiv_dic['properties']['nazwa']
        voiv_id = voiv_dic['id']
        name_to_id_dic[name] = voiv_id
    return name_to_id_dic


def get_geo_df(voivs, voiv_name_to_dic, normalize=False, is_active_cases=False):
    data = []
    for voiv in voivs.values():
        voiv_name = voiv.full_name
        voiv_id = voiv_name_to_dic[voiv_name]
        if is_active_cases:
            df = voiv.get_total_state()
            if normalize:
                data_col = df['Przypadki'].astype(np.float)
                df['Przypadki'] = normalize_by_population(voiv, data_col,
                                                          per_100k=True)
            print("Active cases feature is not working after the 23.11,"
                  " no proper data.", file=sys.stderr)
            ill_cases = df.loc['Aktualnie zakażeni'].Przypadki
        else:
            df = voiv.get_healthy_unhealthy()
            ill_cases = df.loc['Potwierdzone zakażenia', 'Liczba']
            if normalize:
                ill_cases = normalize_by_population(voiv, float(ill_cases),
                                                    per_100k=True)
        data.append([voiv_id, voiv_name, ill_cases])
    return pd.DataFrame(data, columns=['voiv_id', 'voiv_name', "ill"])


def get_map(df_ill_cases, pl_voiv_geojson, ill_name='Chorzy(nadal)'):
    fig = px.choropleth(df_ill_cases, geojson=pl_voiv_geojson,
                        locations='voiv_id',
                        hover_name='voiv_name',
                        scope='europe',
                        hover_data={'ill':True, 'voiv_id': False},
                        color='ill',
                        color_continuous_scale="Reds",
                        # range_color=(0, 12),
                        labels={'voiv_name': 'Województwo',
                                'ill': ill_name},
                        )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    fig.update_geos(fitbounds="locations")
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    return fig