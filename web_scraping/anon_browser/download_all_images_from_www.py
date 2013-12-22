from BeautifulSoup import BeautifulSoup
from anonbrowser import *
import os
import optparse


def mirror_images(url, dir):
    ab = AnonBrowser()
    page = ab.open(url)
    soup = BeautifulSoup(page)
    image_tags = soup.findAll('img')
    for image in image_tags:
        filename = image['src'].lstrip('http://')
        filename = os.path.join(dir, filename.replace('/', '_'))
        print "[+] Saving " + str(filename)
        data = ab.open(image['src']).read()
        ab.back()
        save = open(filename, 'wb')
        save.write(data)
        save.close()


def main():
    parser = optparse.OptionParser("Usage %prog -u <URL> -d <save directory>")
    parser.add_option("-u", dest="url", type="string",
                      help="Specify valid URL")
    parser.add_option("-d", dest="dir", type="string",
                      help="Specify valid output folder")
    (options, args) = parser.parse_args()
    dir = options.dir
    url = options.url

    if dir == None or url == None:
        print parser.usage
        exit(0)
    else:
        try:
            mirror_images(url, dir)
        except Exception, e:
            print "[!] Error saving images:"
            print str(e)


if __name__ == "__main__":
    main()