import pandas as pd
import plotly.express as px


def shape_of_spread_in_voivs(voivs):
    datas = []
    for vol_name, vol in voivs.items():
        data = vol.get_number_of_cases_normalized()
        datas.append(data)
        #print(vol_name, " is any nan: ", data.isna().any().values.any())
    rdf = pd.concat(datas, axis=1)
    rdf = rdf.loc[:, ~rdf.columns.duplicated()]

    dfpx = pd.melt(rdf.reset_index(), id_vars='Data', var_name='Region',
                   value_name='Cases/100k')
    dfpx = dfpx.sort_values(["Region","Data"])
    return px.line(dfpx, x="Data", y='Cases/100k', title='Zmiany',
                   line_group="Region", hover_name="Region", color="Region")
