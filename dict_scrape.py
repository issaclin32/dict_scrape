import re

from typing import Optional
from urllib.error import HTTPError
from bs4 import BeautifulSoup  # pip/beautifulsoup4

from enums import OnlineDict, Lang

from scripts.mw import MW_Dictionary, MW_Thesaurus
from scripts.cam import Cam

# TODO: unified dict result class that applies to all kinds of dictionary results
# TODO: a "redirecting" method that accepts all kinds of OnlineDict