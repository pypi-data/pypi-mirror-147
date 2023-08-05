import pandas as pd
import requests
from bs4 import BeautifulSoup

cdc_url = 'https://phgkb.cdc.gov'
search_term = 'lung'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 '
                  '(KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}


class PhenopediaParser:

    def __init__(self):
        pass

    def parse(search_term: str, dataframe=True):
        url = f'{cdc_url}/PHGKB/phenoPedia.action?firstQuery={search_term}' \
              f'&typeSubmit=Go&typeOption=disease&check=n&which=1'
        html_text = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html_text, features="lxml")
        links = soup.find_all('a')
        diseases = {}
        for link in links:
            href = str(link.get('href'))
            if href.startswith('/PHGKB/phenoPedia.action?firstQuery='):
                diseases[link.getText()] = cdc_url + href

        genes = {}
        for disease in diseases.keys():
            html_text = requests.get(diseases[disease]).text
            soup = BeautifulSoup(html_text, features="lxml")
            urls = soup.find_all('a')
            for gene in urls:
                url = str(gene.get('href'))
                if 'geneID' in url and '/PHGKB/huGEPedia.action' in url:
                    geneID = url.split('=')[1].split('&')[0]
                elif 'searchSummary' in url and geneID is not None:
                    n_pubs = gene.getText().replace('\r\n\t\t\t', '')
                    genes[geneID] = [disease, n_pubs]
                    geneID = None

        if dataframe:
            df = pd.DataFrame.from_dict(genes, orient='index').reset_index()
            rename_map = {'index': 'gene', 0: 'disease', 1: 'n_publications'}
            return df.rename(rename_map, axis='columns')

        return genes
