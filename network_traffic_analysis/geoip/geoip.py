import pygeoip

gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')


def print_record(target):
    rec = gi.record_by_name(target)
    city = rec['city']
    region = rec['region_name']
    country = rec['country_name']
    lon = rec['longitude']
    lat = rec['latitude']
    print "[*] Target Geo IP details:"
    print "[+] " + str(city) + ", " + str(region) + ", " + str(country)
    print "[+] Latitude: " + str(lat) + ", Longtitude: " + str(lat)


target = "173.255.226.98" #sample ip
print_record(target)