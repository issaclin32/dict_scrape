from pprint import pprint
from dict_scrape import *

if __name__ == '__main__':

    test_cases = [
        'mass',
        'elaborate',
        'plead',
        'murky',
        'ebb',
        'lie',
        'finite',
        'hash',
        'sjkfhsdjkfhaks'
    ]


    '''
    output = MW_Dictionary('hash')
    pprint(output)

    with open('output.log', 'w', encoding='utf8') as f:
        f.write( str(output) )
    '''

    for word in test_cases:
        result = Cam(word, dict_name=OnlineDict.Cam_EN_ZH_HANT)
        if result:
            pprint(result)