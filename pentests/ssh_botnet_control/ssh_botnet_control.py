import optparse
import pxssh

class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception, e:
            print e
            print '[-]  Error Connecting'

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

def botnet_command(command):
    for client in bot_net:
        output = client.send_command(command)
        print "[*] Output from " + client.host
        print "[+] " + output + "\n"


def add_client(host, user,password):
    client = Client(host, user, password)
    bot_net.append(client)

bot_net = []
add_client('10.10.10.110', 'root', 'password')
add_client('10.10.10.120', 'root', 'password')
add_client('10.10.10.130', 'root', 'password')
botnet_command('uname -v')
botnet_command('cat /etc/issue')
