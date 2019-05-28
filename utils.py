import urllib.request  # built-in for Python3
from typing import Iterable

from bs4 import BeautifulSoup  # pip/beautifulsoup4
import yattag  # pip/yattag


def url_to_soup(url: str) -> BeautifulSoup:
    HTML_content = urllib.request.urlopen(url).read().decode('utf8')
    return BeautifulSoup(HTML_content, 'lxml')


# not working when used with urllib.request
def pprint_HTML(url: str) -> None:
    HTML_content = urllib.request.urlopen(url).read()
    result = yattag.indent(
        HTML_content,
        indentation = '    ',
        newline = '\n',
        indent_text = True
    )
    print(result)
    return


def ezip(*args: Iterable):
    for arg in args:
        if arg is None:
            #raise TypeError(f'argument "{arg}" is not iterable')
            raise TypeError('NoneType passed to the function')
    for i, a in enumerate(zip(*args)):
        yield (i, *a)