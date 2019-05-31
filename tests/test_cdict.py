import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'\\..')
from dict_scrape import *

test_cases_CH = [
    '攻擊',
    '重擊',
    '紋章',
    '付款',
    '電荷',
    '歸咎',
    '賒帳',
    '哼哼哈兮'
]

for kw in test_cases_CH:
    print(f'中文: {kw}')
    results = cdict(kw)
    if results:
        for res in results:
            print(f'    英文: {res.definition}')
            for ex in res.examples:
                print(f'        例句: {ex}')
    else:
        print('    <查無資料>')