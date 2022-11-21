import ftplib 
from getpass import getpass
from ftplib import FTP_TLS
from config import *

# FTP_HOST = "hoerthin.de"
# FTP_USER = "47730f38165"
# # FTP_PASS = "Mini2021"

try:
    print("Connecting to minimusiker ftp server!") 
    ftp = FTP_TLS(FTP_HOST)
    passwd = getpass("Enter your password: ")
    ftp.login(FTP_USER, passwd)   # login before securing channel
    ftp.prot_p()  
    ftp.encoding = "utf-8"
    ftp.cwd("htdocs/hoerthin/mp3")
    print("Connection success! Directory: htdocs/hoerthin/mp3")
except ftplib.all_errors as e:
    print('FTP error:', e)   

# with closing(ftplib.FTP(FTP_HOST)) as ftp:
#     try:
#         ftp.login(FTP_USER, FTP_PASS)  
#         ftp.mkd('newdir') 



# ftpes = FTP_TLS(FTP_HOST, timeout=5)

# ftpes.login("47730f38165", passwd)   # login before securing channel
# ftpes.prot_p()          # switch to secure data connection
# ftpes.retrlines('LIST') # list directory content securely