import numpy as np
from datetime import datetime

import pandas as pd


DEFAULT_START_DATE = (2020, 3, 6)


def fill_missing_dates(df, from_date=DEFAULT_START_DATE):
    missing_values = pd.date_range(datetime(*from_date), df.index[0])[:-1]
    missing_rows = pd.DataFrame(index=missing_values, columns=df.columns,
                                dtype=np.float)
    missing_rows = missing_rows.replace(np.nan, None)
    missing_rows.index.name = 'Data'
    return pd.concat([df, missing_rows]).sort_index()


def normalize_by_population(vol, df, per_100k=True):
    population_count = vol.population_count()
    coefficient = 1e5 if per_100k else 1
    if isinstance(df, pd.DataFrame) or isinstance(df, pd.Series):
        return df.mul((1/population_count) * coefficient)
    else:
        return df * (1 / population_count) * coefficient
