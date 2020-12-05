import argparse
import os
from configparser import ConfigParser

parser = argparse.ArgumentParser()
default_data_folder = os.path.join('.', 'data')
parser.add_argument('--detail_voiv_data_dir', default=default_data_folder,
                    help='Set directory for store downloaded data')
parser.add_argument('--store_as_relative_path', action='store_true',
                    help='Force to use as relative data to the current '
                         'location of project')
args = parser.parse_args()

config_object = ConfigParser()
data_root_dir = args.data_dir if args.store_as_relative_path else os.path.abspath(args.data_dir)
config_object['STORE_CONFIG'] = {
    'data_root_dir': data_root_dir,
    'is_relative_data': args.store_as_relative_path,
}

with open('config.ini', 'w') as conf:
    config_object.write(conf)
