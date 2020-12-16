import pandas as pd
import plotly.express as px


def shape_of_spread_in_voivs(voivs):
    datas = []
    for vol_name, vol in voivs.items():
        data = vol.get_number_of_cases_normalized()
        datas.append(data)
    rdf = pd.concat(datas, axis=1)
    rdf = rdf.loc[:, ~rdf.columns.duplicated()]

    dfpx = pd.melt(rdf.reset_index(), id_vars='Data', var_name='Region',
                   value_name='Przypadki/100k')
    dfpx = dfpx.sort_values(["Region","Data"])
    return px.line(dfpx, x="Data", y='Przypadki/100k', title='Zmiany',
                   line_group="Region", hover_name="Region", color="Region")
