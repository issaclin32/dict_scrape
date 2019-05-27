from pprint import pprint
from dict_scrape import *
from dict_scrape import pprint_HTML

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

    #pprint_HTML('https://www.merriam-webster.com/thesaurus/folderol')

    pprint( MW_Dictionary('hash') )

    '''
    for word in test_cases:
        result = Cam(word, dict_name='EN-CHT')
        if result:
            pprint(result)
    '''