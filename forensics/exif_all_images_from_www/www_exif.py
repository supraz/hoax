import urllib2
import optparse
from bs4 import BeautifulSoup
from urlparse import urlsplit
from os.path import basename
from PIL import Image
from PIL.ExifTags import TAGS


def find_images(url):
    print "[+] Finding images on: " + url
    url_content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(url_content)
    img_tags = soup.findAll('img')
    return img_tags


def download_image(image_url):
    try:
        print "Downloading image..."
        img_source = image_url['src']
        img_content = urllib2.urlopen(img_source).read()
        img_filename = basename(urlsplit(img_source)[2])
        img_file = open(img_filename, 'wb')
        img_file.write(img_content)
        img_file.close()
        return img_filename
    except:
        return ''


def test_for_exif(image_filename):
    try:
        exif_data = {}
        img_file = Image.open(image_filename)
        info = img_file._getinfo()
        if info:
            for (tag, value) in info.items():
                decoded = TAGS.get(tag, tag)
                exif_data[decoded] = value
            exif_gps = exif_data['GPSInfo']
            if exif_gps:
                print "[+] " + image_filename + "contains GPS MetaData"
            else:
                print "[-] GPS data not found"
        else:
            print "[-] Info not found"
    except:
        pass

def main():
    parser = optparse.OptionParser("Usage %prog -u <URL>")
    parser.add_option("-u", dest="url", type="string",
                      help="Specify the URL")
    (options, args) = parser.parse_args()
    url = options.url
    if url == None:
        print parser.usage
        exit(0)
    else:
        img_tags = find_images(url)
        for img_tag in img_tags:
            img_filename = download_image(img_tag)
            test_for_exif(img_filename)


if __name__ == "__main__":
    main()
