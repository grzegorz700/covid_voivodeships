import os
import sys
from setup_config import config_data_store

sys.path.append(os.path.dirname(__file__))
is_on_heroku = 'ON_HEROKU' in os.environ
if is_on_heroku:
    config_data_store('.', False)

from covid_voivodeships.app.web_app import app

server = app.server
if __name__ == '__main__':
    app.run_server(debug=False)
