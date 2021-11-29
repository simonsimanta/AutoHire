from utils import one_or_default,get_info,all_or_default
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

def overview(overview_soup):
    """Return dict of the overview section of the Linkedin Page"""
    banner = one_or_default(
        overview_soup, 'div.org-top-card-module__container')
    container = one_or_default(
        overview_soup, 'section.org-about-company-module')

    overview = get_info(container, {
        'description': '.org-about-us-organization-description__text',
        'website': '.org-about-us-company-module__website',
        'location': '.org-about-company-module__headquarters',
        'year_founded': '.org-about-company-module__founded',
        'company_type': '.org-about-company-module__company-type',
        'company_size': '.org-about-company-module__company-staff-count-range',
        'specialties': '.org-about-company-module__specialities'
    })

    overview.update(get_info(banner, {
        'name': '.org-top-card-module__name',
        'industry': '.company-industries'
    }))

    all_employees_links = all_or_default(
        banner, '.org-company-employees-snackbar__details-highlight')

    if all_employees_links:
        all_employees_text = all_employees_links[-1].text
    else:
        all_employees_text = ''

    match = re.search(r'((\d+?,?)+)', all_employees_text)
    if match:
        overview['num_employees'] = int(match.group(1).replace(',', ''))
    else:
        overview['num_employees'] = None
    return overview