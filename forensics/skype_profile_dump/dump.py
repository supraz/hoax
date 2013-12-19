import sqlite3
import optparse
import os

def print_profile(skype_db):
    conn = sqlite3.connect(skype_db)
    c = conn.cursor()
    c.execute("SELECT fullname, skypename, city, country, \
              datetime(profile_timestamp, 'unixepoch') FROM Accounts;" )
    for row in c:
        print "[+] Found account:"
        print "Name: " + str(row[0])
        print "Skype login: " + str(row[1])
        print "Location: " + str(row[2]) + ", " + str(row[3])
        print "Profile date: " + str(row[4]) + "\n"


def print_contacts(skype_db):
    conn = sqlite3.connect(skype_db)
    c = conn.cursor()
    c.execute("SELECT displayname, skypename, city, country, \
              phone_mobile, birthday FROM Contacts;")
    for row in c:
        print "[+] Found contact: "
        print "Name: " + str(row[0])
        print "Skype login: " + str(row[1])
        print "Location: " + str(row[2]) + ", " + str(row[3])
        if row[4] != None:
            print "Mobile no.: " + str(row[4])
        if row[5] != None:
            print "Birthday: " + str(row[5])
        print "\n"


def print_calllog(skype_db):
    conn = sqlite3.connect(skype_db)
    c = conn.cursor()
    c.execute("SELECT datetime(begin_timestamp, 'unixepoch'), identity \
              FROM calls, conversations \
              WHERE calls.conv_dbid = conversations.id;")
    print "\n[*] Found calls:"
    for row in c:
        print "[+] Time: " + str(row[0]) + " | Partner id: " + str(row[1])


def print_messages(skype_db):
    conn = sqlite3.connect(skype_db)
    c = conn.cursor()
    c.execute("SELECT datetime(timestamp,'unixepoch'), \
               dialog_partner, author, body_xml FROM Messages;")
    print "\n[*] Found messages: "
    for row in c:
        try:
            if 'partlist' not in str(row[3]):
                if str(row[1]) != str(row[2]):
                    msg_direction = " To " + str(row[1]) + ": "
                else:
                    msg_direction = " From " + str(row[2]) + ": "
                print "Time: " + str(row[0]) +  msg_direction + row[3]
        except:
            pass


def main():
    parser = optparse.OptionParser("Usage %prog -p <path>")
    parser.add_option("-p", dest="path", type="string",
                      help="specify Skype profile path")
    (options, args) = parser.parse_args()
    skype_path = options.path
    if skype_path is None:
        print parser.usage
        exit(0)
    elif os.path.isdir(skype_path) == False:
        print "[!] Specified path does not exist!"
        exit(0)
    else:
        skype_db = os.path.join(skype_path, 'main.db')
        if os.path.isfile(skype_db):
            print_profile(skype_db)
            print_contacts(skype_db)
            print_calllog(skype_db)
            print_messages(skype_db)
        else:
            print "[!] Skype database does not exist!"
            exit(0)

if __name__ == "__main__":
    main()