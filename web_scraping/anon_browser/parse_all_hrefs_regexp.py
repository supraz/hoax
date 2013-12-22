from anonbrowser import *
from BeautifulSoup import BeautifulSoup
import os
import optparse
import re


def print_links(url):
    ab = AnonBrowser()
    ab.anonymize()
    page = ab.open(url)
    html = page.read()
    try:
        print "[*] Printing links"
        link_finder = re.compile('href="(.*?)"')
        links = link_finder.findall(html)
        for link in links:
            print link
    except:
        pass
    try:
        print "[*] Printing links from Beautiful Soup."
        soup = BeautifulSoup(html)
        links = soup.findAll(name='a')
        for link in links:
            if link.has_key('href'):
                print link['href']
    except:
        pass


def main():
    parser = optparse.OptionParser("Usage %prog: -u <URL>")
    parser.add_option("-u", dest="url", type="string",
                      help="Please specify valid URL")
    (options, args) = parser.parse_args()
    url = options.url
    if url == None:
        print parser.usage
        exit(0)
    else:
        print_links(url)

if __name__ == "__main__":
    main()