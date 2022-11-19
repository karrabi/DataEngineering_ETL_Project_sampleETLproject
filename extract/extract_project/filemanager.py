import os
import ftplib
from os import walk
from logger import Log


FTP_HOST = 'ftp-server'
FTP_USERNAME = 'ftp_username'
FTP_PASSWORD = 'ftp_password'

FTP = ''

def Login():
    global FTP
    try:
        FTP = ftplib.FTP(FTP_HOST, FTP_USERNAME, FTP_PASSWORD)
        FTP.cwd('fromapi1min')
        Log('FTP Connected')
    except Exception as e:
        Log('Not Connected. try to reconnect')
        Log(e)
        try:
            FTP = ftplib.FTP(FTP_HOST, FTP_USERNAME, FTP_PASSWORD)
        except Exception as e:
            Log('Can not reconnect')
            Log(e)

def isLoggedin()-> bool:
    global FTP
    try:
        FTP.pwd()
        return True
    except Exception as e:
        return False
        

def SendFile(path, filename):
    try:
        if not isLoggedin():
            Login()
        else:
            with open(path + filename, 'rb') as file:
                FTP.storbinary('STOR ' + filename, file)
            os.remove(path + filename)
    except Exception as e:
        Log(e)

    
def moveFilesToDataLake(path):
    files = next(walk(path), (None, None, []))[2]
    for file in files:
        SendFile(path=path, filename=file)
        