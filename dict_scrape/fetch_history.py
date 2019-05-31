import os
import platform
import subprocess
import re
from typing import List
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote

def fetch_history_Chrome_Cam() -> List[str]:
    CHROME_HISTORY_VIEW_EXE_PATH = f'{os.path.dirname(os.path.abspath(__file__))}\\bin\\ChromeHistoryView\\ChromeHistoryView.exe'
    if platform.system() != 'Windows':
        raise Exception('Only Windows systems are supported.')
    elif not os.path.isfile(CHROME_HISTORY_VIEW_EXE_PATH):
        raise Exception(f'ChromeHistoryView.exe is not found under {CHROME_HISTORY_VIEW_EXE_PATH}')

    tmp_file_path = f'{os.getenv("temp")}\\chrome_history.xml'

    print('Processing Chrome history data...')
    subprocess.call((CHROME_HISTORY_VIEW_EXE_PATH, '/sxml', tmp_file_path))

    with open(tmp_file_path, 'r', encoding='utf_16_le') as f:
        soup = BeautifulSoup(f, 'lxml')

    pat = re.compile(r'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/(\w+)')
    ret = []
    for item in soup.find_all('item'):
        url = item.find('url').text
        results = re.findall(pat, url)
        if results:
            if results[0] not in ret:
                ret.append(results[0])

    return ret