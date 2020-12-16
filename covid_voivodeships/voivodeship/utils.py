from datetime import datetime
import os

from covid_voivodeships.storage.structure import ProjectDataStructure


def load_voiv_urls_with_names():
    ps = ProjectDataStructure()
    pth = os.path.abspath(os.path.join(ps.data_dir, 'essential', 'voivodeship_links.txt'))
    with open(pth) as f:
        voivodeship_links = f.readlines()
    voivodeship_links = [vl.strip() for vl in voivodeship_links]

    voivodeship_names = [vs_link[vs_link.find('-')+1:] for vs_link in voivodeship_links]
    assert len(voivodeship_links) == 16
    
    return voivodeship_links, voivodeship_names


def get_actual_date():
    return datetime.now().strftime("%Y_%m_%d-%H")