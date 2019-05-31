from typing import Optional, List
from urllib.parse import quote, unquote
from urllib.error import HTTPError

from dict_scrape.utils import url_to_soup as _url_to_soup
from ..data_types import *


def cdict(keyword: str) -> Optional[List[Definition]]:
    try:
        soup = _url_to_soup(f'https://cdict.info/query/{quote(keyword)}')
    except HTTPError:
        return None
    else:
        if soup.find('div', class_='resultbox').find('p'):
            if soup.find('div', class_='resultbox').find('p').text == '找不到相關中英文資料':
                return None
    results = []
    for box in soup.find_all('div', class_='resultbox'):
        defi = Definition(
            type=Defi_Type.definition,
            definition=box.find('div', class_='bartop').find(text=True, recursive=False)
        )

        # tree structure: parts of speech -> definitions -> example sentences
        current_def = ''
        current_part_of_speech = ''
        for box_text in box.find_all(text=True, recursive=False):
            box_text = box_text.strip()
            if box_text[0] == '【':
                end = box_text.index('】')
                current_part_of_speech = box_text[1:end]
            # was '\u4e00'<= ch <= '\u9fff'
            elif current_part_of_speech == '慣用語':
                continue
            elif all([ch >= '\u0080' for ch in box_text.replace(' ', '')])\
                    or (box_text[0] in [str(i) for i in range(10)]) \
                    or (box_text[0] in ['a', 'b', 'c', 'd'] and box_text[1] == '.'):
                current_def = box_text
            elif all(['A' <= ch <= 'z' for ch in box_text.replace(' ', '')]):
                current_def = box_text
            elif keyword in current_def:
                first_Chinese_char = -1
                for i in range(len(box_text)):
                    if box_text[i] >= '\u0080':
                        first_Chinese_char = i
                        break
                if first_Chinese_char != -1:
                    defi.examples.append(
                        MLString({
                            Lang.EN: box_text[:first_Chinese_char].strip(' "'),
                            Lang.ZH_HANT: box_text[first_Chinese_char:].strip()
                        })
                    )
                else:
                    defi.examples.append(MLString(box_text.strip(' "')))
            else:
                pass

        results.append(defi)
    return results
