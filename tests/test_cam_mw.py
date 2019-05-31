import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'\\..')
from dict_scrape import *
from msvcrt import getch

test_cases_EN = [
    'mass',
    'elaborate',
    'plead',
    'murky',
    'ebb',
    'lie',
    'finite',
    'hash',
    'not_supposed_to_have_result_HSAKFHA'
]

for test_func in [MW_Dictionary, MW_Thesaurus]:
    print(f'testing: {test_func.__name__}')
    for kw in test_cases_EN:
        print(f'searching: {kw}')
        results = test_func(kw)
        if results:
            for res in results:
                print(f'    definition: {res.definition}')
                print(f'    object info: {res}')
        else:
            print('    <not found>')
        print('\n'*2)
    print('Press any key to continue')
    getch()

for lang in [OnlineDict.Cam_EN, OnlineDict.Cam_EN_ZH_HANT, OnlineDict.Cam_EN_ZH_HANS]:
    print(f'testing: Cambridge--{lang}')
    for kw in test_cases_EN:
        print(f'searching: {kw}')
        results = test_func(kw)
        if results:
            for res in results:
                print(f'    definition: {res.definition}')
                print(f'    object info: {res}')
        else:
            print('    <not found>')
        print('\n'*2)
    print('Press any key to continue')
    getch()
