import re
from typing import Optional, Iterable
import urllib.request  # built-in for Python3
from urllib.error import HTTPError

from bs4 import BeautifulSoup  # pip/beautifulsoup4
import yattag  # pip/yattag


def _url_to_soup(url: str) -> BeautifulSoup:
    HTML_content = urllib.request.urlopen(url).read().decode('utf8')
    return BeautifulSoup(HTML_content, 'lxml')


def pprint_HTML(url: str) -> None:
    HTML_content = urllib.request.urlopen(url).read()
    result = yattag.indent(
        HTML_content,
        indentation = '    ',
        newline = '\n',
        indent_text = True
    )
    print(result)
    return


def _ezip(*args: Iterable):
    for arg in args:
        if arg is None:
            #raise TypeError(f'argument "{arg}" is not iterable')
            raise TypeError('NoneType passed to the function')
    for i, a in enumerate(zip(*args)):
        yield (i, *a)


def Cam(keyword: str, dict_name: str = 'EN-CHT') -> Optional[dict]:
    """
    search on Cambridge English dictionary
    available dict_names:
        EN-CHT: English -> Traditional Chinese
        EN-CHS: English -> Simplified Chinese
        EN-EN: English -> English
    """
    if dict_name == 'EN-CHT':
        url = f'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/{keyword}'
        trans = True  # if Chinese translation is displayed on page
    elif dict_name == 'EN-CHS':
        url = f'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B0%A1%E9%AB%94/{keyword}'
        trans = True
    elif dict_name == 'EN-EN':
        url = f'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E/{keyword}'
        trans = False
    else:
        raise Exception(f'dict_name "{dict_name}" is not supported.')

    soup = _url_to_soup(url)
    if soup.find('h2').text == '熱門搜索' \
            or '&#20320;&#25340;&#23531;&#27491;&#30906;&#20102;&#21966;&#65311;' in soup.find('title').text:
        # -- "你拼寫正確了嗎?"
        # print(f'cannot find keyword "{keyword}" in the dictionary')
        return None

    explanations = []
    for i, block in enumerate(soup.find_all('div', class_='di-body')):  # sense-block
        exp = {
            'guide_word': block.find('span', class_='guideword').find('span').text if block.find('span', class_='guideword') else '',
            'label': block.find('span', class_='pos').text,
            'explanation_EN': block.find('b', class_='def').text,
            'examples_EN': [d.find('span', class_='eg').text for d in block.find_all('div', class_='examp emphasized')],
            'irregular_inflections': block.find('span', class_='irreg-infls').text if block.find('span', class_='irreg-infls') else '',
            'usage_tags': [s.text for s in block.find_all('span', class_='usage')] if block.find('span', class_='usage') else []
        }
        if trans:
            exp.update({
                'explanation_CH': block.find('span', class_='trans').text,
                'examples_CH': [d.find('span', class_='trans').text for d in block.find_all('div', class_='examp emphasized')]
            })

        for key, target in [('IPA_UK', 'uk'), ('IPA_US','us')]:
            if block.find('span', class_=target):
                if block.find('span', class_=target).find('span', class_='ipa'):
                    exp.update({
                        key: block.find('span', class_=target).find('span', class_='ipa').text
                    })

        explanations.append(exp)

    phrases = []
    for block in soup.find_all('div', class_='phrase-block pad-indent'):
        ph = {
            'phrase': block.find('span', class_='phrase').text if trans else block.find('b', class_='phrase').text,
            'explanation_EN': block.find('b', class_='def').text,
            'examples_EN': [examp.find('span', class_='eg').text for examp in block.find_all('div', class_='examp emphasized')]
        }
        if trans:
            ph.update({
                'explanation_CH': block.find('span', class_='trans').text,
                'examples_CH': [examp.find('span', class_='trans').text for examp in block.find_all('div', class_='examp emphasized')]
            })
        phrases.append(ph)

    return {'explanations': explanations, 'phrases': phrases}


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
    if soup.find('p', class_='missing-query'):
        return None

    results = []

    for i, header, block in _ezip(soup.find_all('div', class_='row entry-header'), soup.find_all('div', class_='vg')):
        res = {
            #'word': header.find('h1', class_='hword').text,
            'label': header.find('a', class_='important-blue-link').text,
            'explanations': [s.find(text=True, recursive=False).strip() if s.find(text=True, recursive=False) else '' for s in block.find_all('span', class_='dtText')]
        }
        results.append(res)

    return results