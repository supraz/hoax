# coding: utf-8


import wykop
import urllib
import re
from datetime import datetime

from HTMLParser import HTMLParser

APPKEY=""
SECRETKEY=""
LOGIN = ''
ACCOUNTKEY=""

current_time = datetime.now().strftime('%H:') + "00"

HEADER = u"Aktualny #metar z godziny: " + current_time
FOOTER = u"#metar - sub/czarnólisto"

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


def get_metar_page(page_url):
    try:
        metar_page_source = urllib.urlopen(page_url).read()
        return metar_page_source
    except:
        raise SystemExit

def get_table_from_source(page_source):
    try:
        return re.search("<div class='forecast'>(.*)</table>",
                         page_source).group(1)
    except:
        raise SystemExit


def strip_tags(html):
    try:
        s = MLStripper()
        s.feed(html)
        return s.get_data()
    except:
        raise SystemExit



def main():
    page = get_metar_page('http://awiacja.imgw.pl/index.php?product=metar1h')
    source = get_table_from_source(page)
    metar_data = strip_tags(source)
    splitted= metar_data.split('METAR ')

    message = HEADER + "\n"
    for metar in splitted:
        message_link = metar.replace('    ', ' ').split(" ", 1)
        if len(message_link[0]) > 3:
            final_msg = '\n[**' + message_link[0] + '**]' \
                        '(http://awiacja.imgw.pl/' \
                        'index.php?product=metar30m&aport=' + message_link[0]\
                        + '#k) ' + message_link[-1]
            message += final_msg
    message += "\n\n\n" + FOOTER
    api = wykop.WykopAPI(APPKEY, SECRETKEY)
    api.authenticate(LOGIN, ACCOUNTKEY)
    api.add_entry(message)

if __name__ == '__main__':
    main()