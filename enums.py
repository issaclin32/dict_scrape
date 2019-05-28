from enum import Enum

class Lang(Enum):
    # language code reference: https://en.wikipedia.org/wiki/Template:ISO_639_name
    EN = 'English'
    JA = 'Japanese'
    ZH_HANS = 'Simplified Chinese'
    ZH_HANT = 'Traditional Chinese'

class OnlineDict(Enum):
    Cam_EN = 0  # Cambridge English -> English
    Cam_EN_ZH_HANT = 1
    Cam_EN_ZH_HANS = 2
    MW_DICT = 3  # Merriam-Webster
    MW_THESAURUS = 4
    CDICT = 5
    URBAN_DICTIONARY = 6