import re
from typing import Optional
from urllib.error import HTTPError

from dict_scrape.utils import url_to_soup as _url_to_soup
from dict_scrape.utils import ezip as _ezip


def MW_Dictionary(keyword: str) -> Optional[list]:
    """
    search on Merriam-Webster Thesaurus
    """
    url = f'https://www.merriam-webster.com/dictionary/{keyword}'
    # HACK
    try:
        soup = _url_to_soup(url)
    except HTTPError:
        return None
    else:
        if soup.find('p', class_='missing-query'):
            return None

    # delete all elements after "learn more" (which is not required)
    for element in soup.find('span', id='anchor-seporator').find_all_next('div'):
        element.decompose()

    results = []

    for i, header, block in _ezip(soup.find_all('div', class_='row entry-header'), soup.find_all('div', class_='vg')):
        # for i, header, block in _ezip(soup.find('p', id='more-definitions-anchor').find_all_previous('div', class_='row entry-header'), soup.find('p', id='more-definitions-anchor').find_all_previous('div', class_='vg')):
        # for i, header, block in _ezip(soup.find_all('div', class_='row entry-header'), soup.find_all('div', {'class': re.compile(r'sb .*')})):
        res = {
            #'word': header.find('h1', class_='hword').text,
            'label': header.find('a', class_='important-blue-link').text,
            'definitions': [re.sub(r'\s{2,}|:|\n', '', s.text).strip() for s in block.find_all('span', class_='dtText')]
        }
        results.append(res)

    return results

def MW_Thesaurus(keyword: str) -> Optional[list]:
    """
    search on Merriam-Webster Thesaurus
    """
    url = f'https://www.merriam-webster.com/thesaurus/{keyword}'
    # HACK
    try:
        soup = _url_to_soup(url)
    except HTTPError:
        return None

    if soup.find('p', class_='missing-query'):
        return None

    results = []

    for i, block in enumerate(soup.find_all('div', class_='vg')):
        defi = {
            'definition': block.find('span', class_='dt ').find(text=True, recursive=False).strip(),
            'example': block.find('ul', class_='vis').find('span', class_='t').text,
        }

        headers = [d.find('b').find(text=True, recursive=False).strip() for d in block.find_all('div', class_='thes-list-header')]
        header_conversions = {
            'Synonyms of': 'synonyms',
            'Near Synonyms of': 'near_synonyms',
            'Words Related to': 'words_related',
            'Near Antonyms of': 'near_antonyms',
            'Antonyms of': 'antonyms',
            'Phrases Synonymous with': 'synonym_phrases',
            'Phrases Antonymous with': 'antonym_phrases'
        }
        headers = [header_conversions[h] for h in headers]

        for j, h in enumerate(headers):
            defi[h] = [a.text for a in block.find_all('div', class_='thes-list-content')[j].find_all('a')]

        results.append(defi)
    return results
