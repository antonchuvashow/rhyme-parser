import chompjs
import requests
from bs4 import BeautifulSoup


def get_rhymes(word):
    page = requests.get(f'https://www.rhymezone.com/r/rhyme.cgi?Word={word}&typeofrhyme=adv&loc=advlink')
    soup = BeautifulSoup(page.text, "html.parser")
    rhymes = soup.findAll('script')[7].text
    return chompjs.parse_js_object(rhymes)
