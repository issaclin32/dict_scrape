import re
from typing import Optional, List
from urllib.error import HTTPError

from dict_scrape.utils import url_to_soup as _url_to_soup
from dict_scrape.utils import ezip as _ezip
from ..data_types import *


def MW_Dictionary(keyword: str) -> Optional[List[Definition]]:
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

        defis = [re.sub(r'\s{2,}|:|\n', '', s.text).strip() for s in block.find_all('span', class_='dtText')]

        pos = Pos.not_categorized
        if header.find('a', class_='important-blue-link'):
            pos_text = header.find('a', class_='important-blue-link').text.split(' ')[0].lower()

            if pos_text == 'noun':
                pos = Pos.noun
            elif pos_text == 'verb':
                pos = Pos.verb
            elif pos_text == 'adjective':
                pos = Pos.adjective
            elif pos_text == 'adverb':
                pos = Pos.adverb

        for defi in defis:
            results.append(
                Definition(
                    type=Defi_Type.definition,
                    definition=MLString(defi),
                    part_of_speech = pos
                )
            )
    return results


def MW_Thesaurus(keyword: str) -> Optional[List[Definition]]:
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
        defi = Definition(
            type = Defi_Type.thesaurus,
            definition = block.find('span', class_='dt ').find(text=True, recursive=False).strip()
        )
        defi.examples = [MLString(block.find('ul', class_='vis').find('span', class_='t').text)]
        headers = [d.find('b').find(text=True, recursive=False).strip() for d in block.find_all('div', class_='thes-list-header')]

        for j, h in enumerate(headers):
            lst = [a.text for a in block.find_all('div', class_='thes-list-content')[j].find_all('a')]
            if h == 'Synonyms of':
                defi.synonyms = lst
            elif h == 'Near Synonyms of':
                defi.near_synonyms = lst
            elif h == 'Words Related to':
                defi.words_related = lst
            elif h == 'Antonyms of':
                defi.antonyms = lst
            elif h == 'Phrases Synonymous with':
                defi.synonym_phrases = lst
            elif h == 'Phrases Antonymous with':
                defi.antonym_phrases = lst

        results.append(defi)
    return results
