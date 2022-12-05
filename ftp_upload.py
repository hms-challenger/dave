import os
import shutil
import ftplib
# import getpass
from ftplib import FTP_TLS
from config import FTP_HOST, FTP_USER, FTP_PASS

# save connection to ftp-server
try:
    print("Connecting to minimusiker ftp server!") 
    ftp = FTP_TLS(FTP_HOST, timeout=30)
    # passwd = getpass("Enter your password: ")
    ftp.login(FTP_USER, FTP_PASS)
    ftp.prot_p()  
    ftp.encoding = "utf-8"
    ftp.cwd("htdocs/hoerthin/mp3")
    print("Connection success! Directory: ", ftp.pwd())
except ftplib.all_errors as e:
    print('FTP error:', e)

def uploadThis(uploadFolder):
    files = os.listdir(uploadFolder)
    os.chdir(uploadFolder)
    for f in files:
        print("Uploading...", f)
        if os.path.isfile(uploadFolder + r'/{}'.format(f)):
            fh = open(f, 'rb')
            ftp.storbinary('STOR %s' % f, fh)
            fh.close()
        elif os.path.isdir(uploadFolder + r'/{}'.format(f)):
            ftp.mkd(f)
            ftp.cwd(f)
            uploadThis(uploadFolder + r'/{}'.format(f))
    ftp.cwd('..')
    os.chdir('..')

desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

for folderName in os.listdir(desktop):
    if folderName.startswith("MM"):
        base = desktop + "/" + folderName
        splitFolderName = folderName.split()
        schoolID = splitFolderName[0][2:]
        print("\n-------------------------------------------------------------")
        print("folder created on sftp-server: ", schoolID)
        print("-------------------------------------------------------------\n")

mp3Folder = base + "/mp3"
uploadFolder = base + "/" + str(schoolID)
os.rename(os.path.join(base, mp3Folder), os.path.join(base, schoolID).replace('mp3', schoolID))

# upload mp3Folder to ftp server
print("Creating mp3 folder on ftp server!")
ftp.mkd(schoolID)
ftp.cwd(schoolID)
uploadThis(uploadFolder)

ftp.quit()

# delete cache Folder 
try:
    shutil.rmtree(base)
    print("cache folder deleted!")
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))

print("Job done!")
exit(0)