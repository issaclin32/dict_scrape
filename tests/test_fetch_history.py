import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'\\..')
from dict_scrape import fetch_history_Chrome_Cam as fetch

for result in fetch():
    print(result)