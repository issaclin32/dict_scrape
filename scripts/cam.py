from typing import Optional

from utils import url_to_soup as _url_to_soup
from utils import ezip as _ezip
from enums import OnlineDict

def Cam(keyword: str, dict_name: OnlineDict = OnlineDict.Cam_EN) -> Optional[dict]:
    """
    search on Cambridge English dictionary
    available dict_names:
        OnlineDict.Cam_EN: English -> English
        OnlineDict.Cam_EN_ZH_HANT: English -> Traditional Chinese
        OnlineDict.Cam_EN_ZH_HANS: English -> Simplified Chinese
    """
    if dict_name == OnlineDict.Cam_EN_ZH_HANT:
        url = f'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/{keyword}'
        trans = True  # if Chinese translation is displayed on page
    elif dict_name == OnlineDict.Cam_EN_ZH_HANS:
        url = f'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B0%A1%E9%AB%94/{keyword}'
        trans = True
    elif dict_name == OnlineDict.Cam_EN:
        url = f'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E/{keyword}'
        trans = False
    else:
        raise ValueError(f'dict_name "{dict_name}" is not supported.')

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
            'definition_EN': block.find('b', class_='def').text,
            'examples_EN': [d.find('span', class_='eg').text for d in block.find_all('div', class_='examp emphasized')],
            'irregular_inflections': block.find('span', class_='irreg-infls').text if block.find('span', class_='irreg-infls') else '',
            'usage_tags': [s.text for s in block.find_all('span', class_='usage')] if block.find('span', class_='usage') else []
        }
        if trans:
            exp.update({
                'definition_CH': block.find('span', class_='trans').text,
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
            'definition_EN': block.find('b', class_='def').text,
            'examples_EN': [examp.find('span', class_='eg').text for examp in block.find_all('div', class_='examp emphasized')]
        }
        if trans:
            ph.update({
                'definition_CH': block.find('span', class_='trans').text,
                'examples_CH': [examp.find('span', class_='trans').text for examp in block.find_all('div', class_='examp emphasized')]
            })
        phrases.append(ph)

    return {'definitions': explanations, 'phrases': phrases}