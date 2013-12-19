import optparse
from pyPdf import PdfFileReader


def print_metadata(filename):
    pdf_file = PdfFileReader(file(filename, 'rb'))
    doc_info = pdf_file.getDocumentInfo()
    print "[*] Metadata for: " + filename
    for meta_item in doc_info:
        print "[+] " + meta_item + ": " + doc_info[meta_item]


def main():
    parser = optparse.OptionParser("Usage %prog -f <filename>")
    parser.add_option("-f", dest="filename", type="string",
                      help="specify the filename")
    (options, args) = parser.parse_args()
    filename = options.filename
    if filename == None:
        print parser.usage
        exit(0)
    else:
        print_metadata(filename)


if __name__ == "__main__":
    main()