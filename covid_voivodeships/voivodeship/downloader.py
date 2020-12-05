import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from covid_voivodeships.voivodeship.parser import get_data_script, parse_data_script
from covid_voivodeships.voivodeship.utils import _get_actual_date


def get_page_content_old(link, driver=None):
    if driver is None:
        driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(link)
    content = driver.page_source
    return content


def get_page_content(link, driver=None):
    page = requests.get(link).text # get the raw text of the request
    return page


def download_data(voivodeship_names, voivodeship_links, driver=None, verbose=False):
    voivs = {}
    act_date = _get_actual_date()
    for idx, (voiv_name, voiv_link) in enumerate(zip(voivodeship_names, voivodeship_links)):
        if verbose:
            print(f"[{idx+1:2}/16] {voiv_name}")
        page_content = get_page_content(voiv_link, driver)
        data_script = get_data_script(page_content)
        voiv = parse_data_script(data_script, verbose=False)
        voiv.date = act_date
        voivs[voiv_name] = voiv
    return voivs
