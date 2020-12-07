from glob import glob
import json
from unidecode import unidecode
import os

import pandas as pd

from covid_voivodeships.voivodeship.data.data import VoivodeshipTables, Voivodeship


def save_vol_data_by_csv(ps, vol):
    date_str = vol.date if vol.date is not None else ""
    out_dir = os.path.join(ps.detail_voiv_data_dir, date_str, vol.name)
    file_name_csv = os.path.join(out_dir, "{}.csv")
    file_name_json = os.path.join(out_dir, "variables.json")
    os.makedirs(out_dir, exist_ok=True)
    
    for tname, tobj in vol.tables.items():
        tobj.data.to_csv(file_name_csv.format(tname))
    
    with open(file_name_json, 'w', encoding='UTF-8') as f:
        json.dump(vol.variables, f)
    return out_dir


def save_all_vols(ps, vols):
    for vname, vol in vols.items():
        save_vol_data_by_csv(ps, vol)
        

def load_vol_data_by_csv(out_dir):
    split_dirs = out_dir.split(os.path.sep)
    if not split_dirs[-1]:
        date = split_dirs[-3]
    else:
        date = split_dirs[-2]
    with open(os.path.join(out_dir, "variables.json"), 'r', encoding='UTF-8') as f:
        variables = json.load(f)
    
    tables = {}
    for file in glob(os.path.join(out_dir, "*.csv")):
        df = pd.read_csv(file, index_col=0)
        name = os.path.splitext(os.path.basename(file))[0]
        tables[name] = VoivodeshipTables(name, df)
    return Voivodeship(unidecode(variables['w_nazwa']), tables, variables, date=date)


def load_all_vols(ps, date=None, latest=True):
    if not (latest ^ (date is not None)):
        raise AttributeError('Load vols: Check atributes,'
                             'use date or latest not both or none of them')
    if latest:
        found = sorted(glob(os.path.join(ps.detail_voiv_data_dir, "*")))
        if len(found) < 1:
            return None
        date_data_dir = found[-1]
    else:
        date_data_dir = os.path.join(ps.detail_voiv_data_dir, date)
        if not os.path.exists(date_data_dir):
            return None
    vols = {}
    for vol_dir in glob(os.path.join(date_data_dir, "*")):
        vol = load_vol_data_by_csv(vol_dir)
        vols[vol.name] = vol
    return vols
