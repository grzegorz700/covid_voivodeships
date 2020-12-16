import pandas as pd


class VoivodeshipTables:
    def __init__(self, name, data, comment=None):
        self.name = name
        self.data = data
        self.comment = comment


class Voivodeship:
    def __init__(self, name, tables, variables, date=None):
        self.name = name
        self.tables = tables
        self.variables = variables
        self.date = date
    
    @property
    def full_name(self):
        return self.variables['w_nazwa']

    def get_total_state(self):
        df = self.tables['data'].data
        df['commodity'] = df['commodity'].replace('Chorzy',
                                                  'Aktualnie zakażeni')
        df.country = [self.full_name] * df.shape[0]
        df = df.rename(columns={
            "commodity": "Grupa",
            "country": "Województwo",
            "total": "Przypadki"
        })
        df = df.set_index('Grupa')
        return df

    def get_healthy_unhealthy(self):
        df = self.tables['data_populacja'].data
        df.popul = [self.full_name] * df.shape[0]
        df = df.rename(columns={
            "commodity": "Grupa",
            "popul": "Województwo",
            "total": "Liczba"
        })
        df = df.set_index('Grupa')
        return df

    def get_state_daily(self):
        if 'dataSource_przyrost' in self.tables:  # Data source before October
            df = self.tables['dataSource_przyrost'].data
            df = df.rename(columns={
                "country": "Data",
                "chor": "Chorzy",
                "wyl": "Wyleczeni",
                "zar": "Zarazeni",
                "zgo": "Zgony"
            })
        elif 'dataSource_koronawirus' in self.tables:  # Data source since October
            df = self.tables['dataSource_koronawirus'].data
            df = df.rename(columns={
                "dzien": "Data",
                "woj_chor": "Chorzy",
                "woj_wyl": "Wyleczeni",
                "woj_zar": "Zarazeni",
                "woj_zgo": "Zgony"
            })
        else:
            raise AssertionError("Some problem with the data source, check the"
                                 "downloaded data")
        df.Data = pd.to_datetime(df.Data, dayfirst=True)
        df = df.set_index('Data')
        return df

    def get_daily_change(self):
        df = self.tables['populationData'].data
        df = df.rename(columns={
            "arg": "Data",
            "p_chorzy": "Zarazeni",
            "p_wyleczeni": "Wyleczeni",
            "p_zgony": "Zgony"
        })
        df.Data = pd.to_datetime(df.Data, dayfirst=True)
        df = df.set_index('Data')
        return df

    def get_number_of_cases_normalized(self):
        df = self.tables['dataSource_wskaznik_100'].data
        df = df.rename(columns={
            "country": "Data",
            "polska": "Polska",
            "zar": self.full_name[0].upper() + self.full_name[1:]
        })
        df.Data = pd.to_datetime(df.Data, dayfirst=True)
        df = df.set_index('Data')
        return df

    def get_quarantine_etc(self):
        df = self.tables['dataSource_hospitalizacja'].data
        df = df.rename(columns={
            "country": "Data",
            "wyl": "Kwarantanna",
            "zar": "Hospitalizacja",
            "zgo": "Nadzór Epidemiologiczny",
        })
        df.Data = pd.to_datetime(df.Data, dayfirst=True)
        df = df.set_index('Data')
        return df

    def get_hospitalized_daily(self):
        df = self.tables['Data_przyrost_szpital'].data
        df = df.rename(columns={
            "arg": "Data",
            "p_szpital": "Przyrost Hospitalizowanych",
        })
        df.Data = pd.to_datetime(df.Data, dayfirst=True)
        df = df.set_index('Data')
        return df

    def get_tests(self):
        df = self.tables['dataSource_testy'].data
        df = df.rename(columns={
            "dzien": "Data",
            "mmp": "Testy",
            "smp": "Zarażenia",
        })
        df.Data = pd.to_datetime(df.Data, dayfirst=True)
        df = df.set_index('Data')
        return df

    def get_tests_daily(self):
        df = self.tables['Data_przyrost_testy'].data
        df = df.rename(columns={
            "arg": "Data",
            "p_testy": "Nowe Testy",
            "p_chorzy": "Nowe Zarażenia",
        })
        df.Data = pd.to_datetime(df.Data, dayfirst=True)
        df = df.set_index('Data')
        return df

    def get_death_rate(self):
        return self.variables['smiertelnosc']

    def population_count(self):
        return self.get_healthy_unhealthy().Liczba.sum()
