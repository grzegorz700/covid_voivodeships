import os
from configparser import ConfigParser

import covid_voivodeships
from covid_voivodeships.utils import SingletonMeta


class ProjectDataStructure(metaclass=SingletonMeta):
    def __init__(self):

        config_object = ConfigParser()
        module_path = os.path.abspath(os.path.dirname(covid_voivodeships.__file__))
        project_root_path = os.path.join(module_path, '..')
        config_object.read(os.path.join(project_root_path, 'config.ini'))
        store_config = config_object["STORE_CONFIG"]

        if store_config['is_relative_data']:
            all_data_dir = os.path.join(project_root_path, 'data')
        else:
            all_data_dir = store_config['detail_voiv_data_dir']

        self.data_dir = all_data_dir
        self.detail_voiv_data_dir = os.path.join(all_data_dir, 'covid_voivs')
        print(os.path.abspath(self.detail_voiv_data_dir))
        os.makedirs(self.detail_voiv_data_dir, exist_ok=True)
