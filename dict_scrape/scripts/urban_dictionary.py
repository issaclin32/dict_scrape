import re
from typing import Optional, List
from urllib.error import HTTPError

from dict_scrape.utils import url_to_soup as _url_to_soup
from dict_scrape.utils import ezip as _ezip
from ..data_types import *


def urban_dictionary(keyword: str) -> Optional[List[Definition]]:
    try:
        soup = _url_to_soup(f'https://www.urbandictionary.com/define.php?term={keyword}')
    except HTTPError:
        return None
    else:
        # <div class="shrug space">¯\_(ツ)_/¯</div>
        if soup.find('div', class_='shrug space'):
            return None
    return []