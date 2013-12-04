# sample usage:
# python unix_password_cracker.py passwordfile.txt dictionaryfile.txt
#
# generate passwordfile.txt from /etc/shadow

import crypt
import sys

def testPass(crypt_pass):
    salt = crypt_pass[0:2]
    dictionary_file = open(sys.argv[2], 'r')
    for word in dictionary_file.readlines():
        word = word.strip('\n')
        crypt_word = crypt.crypt(word, salt)
        if (crypt_word == crypt_pass):
            print "[+] Found Password: " + word + "\n"
            return
    print "[-] Password Not Found. \n"
    return

def main():
    pass_file = open(sys.argv[1])
    for line in pass_file.readlines():
        if ":" in line:
            user = line.split(':')[0]
            crypt_pass = line.split(':')[1].strip(' ')
            print "[*] Cracking Password For: " + user
            testPass(crypt_pass)
if __name__ == "__main__":
    main()
