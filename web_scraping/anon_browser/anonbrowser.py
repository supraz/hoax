import mechanize
import cookielib
import random


class AnonBrowser(mechanize.Browser):
    def __init__(self, proxies = [], useragents = []):
        mechanize.Browser.__init__(self)
        self.set_handle_robots(False)
        self.proxies = proxies
        self.useragents = useragents + ['Mozilla/4.0 ', 'FireFox/6.01', \
                                        'ExactSearch', 'Nokia7110/1.0']
        self.cookie_jar = cookielib.LWPCookieJar()
        self.set_cookiejar(self.cookie_jar)
        self.anonymize()


    def clear_cookies(self):
        self.cookie_jar = cookielib.LWPCookieJar()
        self.set_cookiejar(self.cookie_jar)


    def change_useragent(self):
        index = random.randrange(0, len(self.useragents))
        self.addheaders = [("User-agent", self.useragents[index])]


    def change_proxy(self):
        if self.proxies:
            index = random.randrange(0, len(self.proxies))
            self.set_proxies({"http", self.proxies[index]})


    def anonymize(self, sleep = False):
        self.clear_cookies()
        self.change_useragent()
        self.change_proxy()
        if sleep:
            time.sleep(60)