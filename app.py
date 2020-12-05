import os, sys
sys.path.append(os.path.dirname(__file__))

from covid_voivodeships.app.web_app import app

server = app.server
if __name__ == '__main__':
    app.run_server(debug=False)
