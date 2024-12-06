from bs4 import BeautifulSoup as bs
import requests, threading

headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'}

class AwesomeNations:
    def __init__(self) -> None:
        pass
    
    def get_census(nation_name = 'testlandia', censusid = [0], raw = True):
        data = {}
        
        nation_name.lower()
        nation_name = nation_name.replace(' ', '_')

        for id in censusid:
            html = requests.get(f'https://www.nationstates.net/nation={nation_name}/detail=trend/censusid={id}', headers=headers)
            soup = bs(html.text, 'html.parser')

            if raw == False:
                census_value = soup.find('div', class_='censusscoreboxtop').get_text().replace(',', '')
                if '.' in census_value:
                    census_value = float(census_value)
                else:
                    census_value = int(census_value)
            else:
                census_value = soup.find('div', class_='censusscoreboxtop').get_text().replace(' ', '')
            census_name = str(soup.find('h2').findChild('a', class_ = 'quietlink').get_text().lower().replace(' ', '_').replace(':', ''))
            data[census_name] = census_value
        return data
    
    def one_plus_one():
        return 1 + 1