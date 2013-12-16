from _winreg import *
import os
import optparse
import mechanize
import urllib
import re
import urlparse


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


def val2addr(val):
    addr = ''
    for ch in val:
        addr += '%02x ' % ord(ch)
    addr = addr.strip(' ').replace(' ', ':')[0:17]
    return addr


def print_networks(username, password):
    net = "SOFTWARE\Microsoft\Windows NT\CurrentVersion" \
          "\NetworkList\Signatures\Unmanaged"
    key = OpenKey(HKEY_LOCAL_MACHINE, net)
    print '\n[*] Networks you have joined:'
    for i in range(100):
        try:
            guid = EnumKey(key, i)
            netKey = OpenKey(key, str(guid))
            (n, addr, t) = EnumValue(netKey, 5)
            (n, name, t) = EnumValue(netKey, 4)
            macAddr = val2addr(addr)
            netName = str(name)
            print '[+] ' + netName + ' ' + macAddr
            wigle_print(username, password, macAddr)
            CloseKey(netKey)
        except:
            break


def main():
    parser = optparse.OptionParser("Usage %prog -u <username> -p <password>")
    parser.add_option("-u", dest="username", type="string",
                      help="specify username")
    parser.add_option("-p", dest="password", type="string",
                      help="specify password")
    (options, args) = parser.parse_args()
    username = options.username
    password = options.password

    if username == None or password == None:
        print parser.usage
        exit(0)
    else:
        print_networks(username, password)

if __name__ == "__main__":
    main()