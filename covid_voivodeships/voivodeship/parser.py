import json
from unidecode import unidecode

from IPython.display import display
import _jsonnet
import pandas as pd
from bs4 import BeautifulSoup, Comment

from covid_voivodeships.voivodeship.data.data import VoivodeshipTables, Voivodeship


def get_data_script(content):
    soup = BeautifulSoup(content, features="lxml")
    chart_comment = soup.findAll(
        text=lambda text: isinstance(text, Comment) and
                          text.title().strip() == 'Wykresy')[0]
    data_script = chart_comment.findNext().findNext()
    return data_script


def parse_data_script(data_script, verbose=False):
    if not verbose:
        print_if_required = (lambda *args, **kwargs: None)
    else:
        print_if_required = print
    datas = data_script.string.split(';')
    tables = {}
    variables = {}
    for d in datas:
        d = d.strip()
        if len(d) == 0:
            continue
        if d.startswith('/*'):
            _, d = d.split('\n', 1)
            d = d.strip()
        if '*/' in d:
            _, d = d.split('*/', 1)
            d = d.strip()

        if ("\n" in d and d.startswith('//')):
            end_fist_line = d.find('\n')
            comment = d[2:end_fist_line]
            d = d[end_fist_line+1:].strip()
            print_if_required(f"Comment: {comment}")
        else:
            comment = None

        if d.startswith('var'):
            equal_sign_idx = d.find('=')
            variable_name = d[3:equal_sign_idx].strip()
            print_if_required('Variable_name: ', variable_name)
            d = d[equal_sign_idx+1:].strip()
            if '[' not in d:
                d = d.replace("'", "")
                if d.replace('.', '', 1).isdigit() :
                    value = float(d)
                else:
                    value = d
                print_if_required('Value = ', value)
                variables[variable_name] = value
            else:
                values = json.loads(_jsonnet.evaluate_snippet('snippet', d))
                df_values = pd.DataFrame(values)
                if verbose:
                    display(df_values)
                tables[variable_name] = VoivodeshipTables(variable_name,
                                                          df_values, comment)
        else:
            raise SyntaxError('Data_sript parsing error with: ',  str(d))
        print_if_required('-'*30)
    vol = Voivodeship(unidecode(variables['w_nazwa']), tables, variables)
    return vol
