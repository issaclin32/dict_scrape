from typing import Optional

from dict_scrape.utils import url_to_soup as _url_to_soup
from dict_scrape.data_types import *


def Cam(keyword: str, dict_name: OnlineDict = OnlineDict.Cam_EN) -> Optional[List[Definition]]:
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
        trans_lang = Lang.ZH_HANT
    elif dict_name == OnlineDict.Cam_EN_ZH_HANS:
        url = f'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B0%A1%E9%AB%94/{keyword}'
        trans = True
        trans_lang = Lang.ZH_HANS
    elif dict_name == OnlineDict.Cam_EN:
        url = f'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E/{keyword}'
        trans = False
        trans_lang = None  # for static checking issues
    else:
        raise ValueError(f'dict_name "{dict_name}" is not supported.')

    soup = _url_to_soup(url)
    if soup.find('h2').text == '熱門搜索' \
            or '&#20320;&#25340;&#23531;&#27491;&#30906;&#20102;&#21966;&#65311;' in soup.find('title').text:
        # -- "你拼寫正確了嗎?"
        # print(f'cannot find keyword "{keyword}" in the dictionary')
        return None

    definitions = []
    explanations = []
    for i, block in enumerate(soup.find_all('div', class_='di-body')):  # sense-block
        if trans:
            defi = Definition(type=Defi_Type.definition,
                              definition=MLString({
                                  Lang.EN: block.find('b', class_='def').text,
                                  trans_lang: block.find('span', class_='trans').text
                              }))
        else:
            defi = Definition(type=Defi_Type.definition,
                              definition=MLString(block.find('b', class_='def').text))

        defi.guide_word = block.find('span', class_='guideword').find('span').text if block.find('span', class_='guideword') else ''
        defi.part_of_speech = Pos.from_string(block.find('span', class_='pos').text, unknown_ok=True)
        defi.irregular_inflections = block.find('span', class_='irreg-infls').text if block.find('span', class_='irreg-infls') else []
        defi.usage_tags = [s.text for s in block.find_all('span', class_='usage')] if block.find('span', class_='usage') else []

        for d in block.find_all('div', class_='examp emphasized'):
            if trans:
                defi.examples.append(
                    MLString({
                        Lang.EN: d.find('span', class_='eg').text,
                        trans_lang: d.find('span', class_='trans').text
                    })
                )
            else:
                defi.examples.append(MLString(d.find('span', class_='eg').text))

        if block.find('span', class_='uk'):
            if block.find('span', class_='uk').find('span', class_='ipa'):
                defi.IPA_UK = block.find('span', class_='uk').find('span', class_='ipa').text
            elif block.find('span', class_='us').find('span', class_='ipa'):
                defi.IPA_US = block.find('span', class_='us').find('span', class_='ipa').text

        definitions.append(defi)

    for block in soup.find_all('div', class_='phrase-block pad-indent'):
        if trans:
            defi = Definition(
                type=Defi_Type.phrase,
                definition=MLString({
                    Lang.EN: block.find('b', class_='def').text,
                    trans_lang:  block.find('span', class_='trans').text
                })
            )
        else:
            defi = Definition(
                type=Defi_Type.phrase,
                definition=MLString(block.find('b', class_='def').text)
            )
        defi.term = block.find('span', class_='phrase').text if trans else block.find('b', class_='phrase').text

        for d in block.find_all('div', class_='examp emphasized'):
            if trans:
                defi.examples.append(MLString({
                    Lang.EN: d.find('span', class_='eg').text,
                    trans_lang: d.find('span', class_='trans').text
                }))
            else:
                defi.examples.append(MLString(d.find('span', class_='eg').text))
        definitions.append(defi)

    return definitions
