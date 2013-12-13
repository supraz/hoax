# sample usage
# python zip_file_password_cracker.py -f archive.zip -d dictionary.txt

import zipfile
import optparse
import os
from threading import Thread


def extract_file(archive, password):
    try:
        archive.extractall(pwd=password)
        print '[+] Password = ' + password + '\n'
        return
    except:
        pass


def main():
    parser = optparse.OptionParser("usage " + os.path.basename(__file__) + " -f <zipfile> -d <dictionary")
    parser.add_option('-f', dest='archive', type='string', help='specify zip file')
    parser.add_option('-d', dest='dictionary', type='string', help='specify dictionary file')
    (options, args) = parser.parse_args()
    if options.archive is None or options.dictionary is None:
        print parser.usage
        exit(0)
    else:
        archive = options.archive
        dictionary = options.dictionary
    archive_file = zipfile.ZipFile(archive)
    dictionary_file = open(dictionary)
    for line in dictionary_file.readlines():
        password = line.strip('\n')
        t = Thread(target=extract_file, args=(archive_file, password))
        t.start()
        guess = extract_file(archive, password)
        if guess:
            exit(0)

if __name__ == '__main__':
    main()
