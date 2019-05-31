from typing import List, Dict, Union
# from typing import overload
from enum import Enum
from dataclasses import dataclass, field  # pip/dataclasses for Python 3.6; built-in for Python 3.7 and above


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


# Part of speech: verb, noun, etc.
class Pos(Enum):
    # reference: https://en.wikipedia.org/wiki/Part_of_speech
    not_categorized = 0
    noun = 1
    verb = 2
    adjective = 3
    adverb = 4
    pronoun = 5
    preposition = 6
    conjunction = 7  # but, and, or, etc.
    interjection = 8  # emotional greeting or exclamation (Huzzah, Alas)
    determiners = 9  # articles (a, the) and quantifiers(all, some, any)
    auxiliary_verb = 10
    phrase = 11
    noun_phrase = 12
    verb_phrase = 13
    measure_word = 14  # not used in English, but commonly used in Chinese and Japanese (一"張"紙)
    contraction = 15  # let's, I'm, etc.
    verb_transitive = 16
    verb_intransitive = 17

    def __bool__(self):
        return self != self.not_categorized

    @classmethod
    def from_string(cls, string: str, unknown_ok: bool = True):
        for item in cls:
            if string.strip().lower() == item.name:
                return item
        else:  # if not "break"ing from the for-loop
            if unknown_ok:
                return cls.not_categorized
            else:
                raise KeyError(f'part of speech with type {string} is not defined.')

    @classmethod
    def from_abbr(cls, abbr: str, unknown_ok: bool = True):
        abbr_table = {
            'n': cls.noun,
            'v': cls.verb,
            'adj': cls.adjective,
            'a': cls.adjective,
            'adv': cls.adverb,
            'pron': cls.pronoun,
            'prep': cls.preposition,
            'conj': cls.conjunction,
            'aux': cls.auxiliary_verb,
            'phr': cls.phrase
        }
        if abbr in abbr_table.keys():
            return abbr_table[abbr]
        else:
            if unknown_ok:
                return cls.not_categorized
            else:
                raise KeyError(f'part of speech with abbreviation {abbr} is not defined.')


class Defi_Type(Enum):
    definition = 0
    thesaurus = 1
    phrase = 2


# Used for storing multi-language data for "definition", "example sentence", etc.
# May need a better name for describing this object
class MLString:
    def __init__(self, content: Union[Dict[Lang, str], str]):
        if type(content) is str:
            content = {Lang.EN: content}  # treat as English by default
        self.content = content

    def get(self, lang: Lang) -> str:
        if lang in self.content.keys():
            return self.content[lang]
        else:
            raise KeyError(f'no content found for language {lang}')

    def get_all(self) -> Dict[Lang, str]:
        return self.content

    def has_lang(self, lang: Lang) -> bool:
        if lang in self.content.keys():
            return True
        else:
            return False

    def all_langs(self):
        return self.content.keys()

    def __str__(self):
        return '  '.join([ f'{k.value}: {v}  ' for k, v in self.content.items()])

    def __repr__(self):
        return str(self)


# Using Dataclass instead of Dict for better static checking
# (whether the field name / types are correct)
@dataclass(eq=True)  # eq: enable comparison
class Definition:
    # required fields
    type: Defi_Type
    definition: MLString
    part_of_speech: Pos = Pos.not_categorized

    # optional fields
    # TODO: more specific structure for storing pronunciation data (including mp3 URL/file)
    term: str = ''  # used in related phrases
    examples: List[MLString] = field(default_factory=list)
    guide_word: str = ''
    irregular_inflections: List[str] = field(default_factory=list)
    usage_tags: List[str] = field(default_factory=list)
    IPA_US: str = ''
    IPA_UK: str = ''


    # fields for thesaurus results
    synonyms: List[str] = field(default_factory=list)
    near_synonyms: List[str] = field(default_factory=list)
    antonyms: List[str] = field(default_factory=list)
    near_antonyms: List[str] = field(default_factory=list)
    words_related: List[str] = field(default_factory=list)
    synonym_phrases: List[str] = field(default_factory=list)
    antonym_phrases: List[str] = field(default_factory=list)

    def __str__(self):
        ret = ''
        for k, v in vars(self).items():
            if bool(v):
                ret += f'{k}: {v},\n'
        return ret
