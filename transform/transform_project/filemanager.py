import os
import ftplib
from os import walk

FTP_HOST = 'ftp-server'
FTP_USERNAME = 'ftp_username'
FTP_PASSWORD = 'ftp_password'

FTP = ''

def Login(path):
    global FTP
    try:
        FTP = ftplib.FTP(FTP_HOST, FTP_USERNAME, FTP_PASSWORD)
        FTP.cwd(path)
        print('FTP Connected')
    except Exception as e:
        print('Not Connected. try to reconnect')
        print(e)
        try:
            FTP = ftplib.FTP(FTP_HOST, FTP_USERNAME, FTP_PASSWORD)
        except Exception as e:
            print('Can not reconnect')
            print(e)

def isLoggedin()-> bool:
    global FTP
    try:
        FTP.pwd()
        return True
    except Exception as e:
        return False
        

def setCurrentPath(path):
    try:
        if not isLoggedin():
            Login()
        else:
            if FTP.pwd() != path:
                FTP.cwd(path)
    except Exception as e:
        print(e)
        
        
def SendFile(destination_path, path, filename):
    try:
        if not isLoggedin():
            Login(destination_path)
        else:
            setCurrentPath(destination_path)
            with open(path + filename, 'rb') as file:
                FTP.storbinary('STOR ' + filename, file)
            os.remove(path + filename)
    except Exception as e:
        print(e)

    
    
def RetriveFile(source_path, path, filename):
    try:
        if not isLoggedin():
            Login(source_path)
        else:
            setCurrentPath(source_path)
            with open(path + filename, 'wb') as file:
                FTP.retrbinary('RETR ' + filename, file.write)
            return True
    except Exception as e:
        print(e)
        return False
    

def readNewExtractedFiles(path):
    filesls = []
    try:
        if not isLoggedin():
            Login(path)
        else:
            setCurrentPath(path)
            filesls = FTP.nlst()
    except Exception as e:
        print(e)
        
    return filesls

def listNextExtractedFile(path):
    extracted_files = readNewExtractedFiles(path)
    same_files = []
    pattern_name = ''
    for file in extracted_files:
        if len(same_files) == 0:
            same_files.append(file)
            pattern_name = same_files[0][:same_files[0].find('_')]
        else:
            if pattern_name in file:
                same_files.append(file)

    return same_files, pattern_name

            
            
def archiveFiles(source_path, destination_path, temp_path, filesls):
    try:
        if not isLoggedin():
            Login(source_path)
        else:
            setCurrentPath(source_path)
            for file in filesls:
                FTP.rename('{}/{}'.format(source_path,file) , '{}/{}'.format(destination_path,file))
                os.remove(temp_path + file)
    except Exception as e:
        print(e)
