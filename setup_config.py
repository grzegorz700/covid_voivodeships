import argparse
import os
from configparser import ConfigParser


def config_data_store(data_dir, store_as_relative_path):
    config_object = ConfigParser()
    data_root_dir = data_dir if store_as_relative_path else os.path.abspath(
        data_dir)
    config_object['STORE_CONFIG'] = {
        'data_root_dir': data_root_dir,
        'is_relative_data': store_as_relative_path,
    }

    with open('config.ini', 'w') as conf:
        config_object.write(conf)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    default_data_folder = os.path.join('.', 'data')
    parser.add_argument('--data_dir', default=default_data_folder,
                        help='Set directory for store downloaded data')
    parser.add_argument('--store_as_relative_path', action='store_true',
                        help='Force to use as relative data to the current '
                             'location of project')
    args = parser.parse_args()
    config_data_store(args.data_dir, args.store_as_relative_path)
