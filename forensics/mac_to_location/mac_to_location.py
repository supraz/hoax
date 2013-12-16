import mechanize
import urllib
import urlparse
import re


# didn't forget to remove these :-)
USERNAME = 'devsupraz0'
PASSWORD = 'devsupraz123'
SAMPLE_MAC = '0A:2C:EF:3D:25:1B'

def wigle_print(username, password, netid):
    browser = mechanize.Browser()
    browser.open('http://wigle.net')
    request_data = urllib.urlencode({'credential_0' : username,
                                     'credential_1' : password})
    browser.open('http://wigle.net/gps/gps/main/login', request_data)
    params = {}
    params['netid'] = netid
    request_params = urllib.urlencode(params)
    resp_url = 'http://wigle.net/gps/gps/main/confirmquery/'
    resp = browser.open(resp_url, request_params).read()
    map_lat = 'N/A'
    map_lon = 'N/A'
    r_lat = re.findall(r'maplat=.*\&', resp)
    r_lon = re.findall(r'maplon=.*\&', resp)
    if r_lat:
        map_lat = r_lat[0].split('&')[0].split('=')[1]
    if r_lon:
        map_lon = r_lon[0].split()
    print '[-] LAT: ' + map_lat + ', LON: ' + map_lon


def main():
    wigle_print(USERNAME, PASSWORD, SAMPLE_MAC)

if __name__ == '__main__':
    main()