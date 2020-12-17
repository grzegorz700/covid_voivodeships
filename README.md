# Covid in Polish Voivodeships - Interactive web application

---

## Quick graphical overview:

![Application](recording-webapp.gif "Website recording")

## Online application:
This application is currently available at heroku at:
> [covid-pl.herokuapp.com](covid-pl.herokuapp.com)

The first run (after being not active for 30 minutes) takes longer than normal. It's connected with the limitations of the free heroku plan.

In mobile, the application works fine; however, in the future, it is considered to adjust the application to prevent users from unexpected clicks on interactive graphs.

## Usage:

### Preparation locally:
#### Installation of requirements:

    pip install -r requirements.txt

#### Config data store directory:
 
    python setup_config.py [--data_dir PATH_TO_DATA_DIR [--store_as_relative_path]]

### Deployment on heroku:

Additional configuration on heroku:
    
    heroku run bash
    python setup_config.py
    exit

    heroku buildpacks:add heroku-community/locale

### Run:

    python app.py

## Application overview:
Application consists of a few parts:
* Downloading, parsing and storing data about covid cases from the web.
* Preparation of rare (or not existed) data visualization about covid cases in Poland with the distinction to voivodeships.  
* Presentation of this visualization in a configurable, interactive way.
* Preparation of the app to deploy it on the heroku (using free plan)

## Disclaimer

Application is prepared for the Polish-speaking people because they are the main group of people interested in detailed data of covid cases with the distinction to voivodeships.
However, the whole application, except the data with the Polish names of columns, is written in English.

The application was showing also the number of recovery people. It was before the change of reporting in Poland. That causes that is no data of sick and healthy people after the 23.11.2020.

## Main technology:
* Python 3.8
* Dash & Plotly