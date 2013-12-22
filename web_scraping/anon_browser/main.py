from anonbrowser import *

def main():
    ab = AnonBrowser(proxies = [], useragents = [('User-agent',
                                                  'SuperSecret')])
    for attempt in range (1, 5):
        ab.anonymize()
        print "[*] Fetching page "
        response = ab.open("http://kittenwar.com")
        for cookie in ab.cookie_jar:
            print cookie


if __name__ == "__main__":
    main()