import ftplib


def return_default(ftp):
    try:
        dir_list = ftp.nlst()
    except:
        dir_list = []
        print '[-] Could not list directory contents'
        print '[-] Skipping to next target'
        return
    ret_list = []
    for file_name in dir_list:
        fn = file_name.lower()
        if '.php' in fn or '.htm' in fn or '.asp' in fn:
            print "[+] Found default page: " + file_name
            ret_list.append(file_name)
    return ret_list

host = '192.168.95.179'
username = 'guest'
password = 'guest'
ftp = ftplib.FTP(host)
ftp.login(username, password)
return_default(ftp)