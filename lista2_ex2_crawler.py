import requests
from bs4 import BeautifulSoup
import re

def web(page,WebUrl):
    if(page>0):
        url = WebUrl
        code = requests.get(url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        i = 0;
        for link in s.findAll('p'):
            tet = clean_text(str(link))
            i = i + 1;
            print(i , 'tag <p> =>', tet, '\n')


def clean_text(text):
    # remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # replace punctuation characters with spaces
    filters = '!"\'#$%&()*+-/:;<=>?@[\\]^_`{|}~\t\n'
    translate_dict = dict((c, " ") for c in filters)
    translate_map = str.maketrans(translate_dict)
    text = text.translate(translate_map)

    return text


web(1,'https://en.wikipedia.org/wiki/Wikipedia_talk:Getting_to_Philosophy')