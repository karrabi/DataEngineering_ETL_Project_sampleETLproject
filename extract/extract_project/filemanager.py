import os
import ftplib
from os import walk
from logger import Log

# FTP server credentials
FTP_HOST = 'ftp-server'
FTP_USERNAME = 'ftp_username'
FTP_PASSWORD = 'ftp_password'

# FTP connection object
FTP = ''

def Login():
    """
    Log in to the FTP server using the provided credentials.
    """
    global FTP
    try:
        FTP = ftplib.FTP(FTP_HOST, FTP_USERNAME, FTP_PASSWORD)
        FTP.cwd('fromapi1min')  # Change to the desired directory
        Log('FTP Connected')
    except Exception as e:
        Log('Not Connected. Trying to reconnect')
        Log(e)
        try:
            FTP = ftplib.FTP(FTP_HOST, FTP_USERNAME, FTP_PASSWORD)
        except Exception as e:
            Log('Could not reconnect')
            Log(e)

def isLoggedin() -> bool:
    """
    Check if the FTP connection is still valid and logged in.

    Returns:
        bool: True if logged in, False otherwise.
    """
    global FTP
    try:
        FTP.pwd()  # Attempt to get current directory; raises an exception if not logged in
        return True
    except Exception as e:
        return False

def SendFile(path, filename):
    """
    Upload a file to the FTP server.

    Args:
        path (str): The path to the file.
        filename (str): The name of the file to upload.
    """
    try:
        if not isLoggedin():
            Login()
        else:
            with open(path + filename, 'rb') as file:
                FTP.storbinary('STOR ' + filename, file)  # Store the file on the server
            os.remove(path + filename)  # Remove the local file after successful upload
    except Exception as e:
        Log(e)

def moveFilesToDataLake(path):
    """
    Move files from a specified path to the FTP server's data lake directory.

    Args:
        path (str): The path to the directory containing the files.
    """
    files = next(walk(path), (None, None, []))[2]
    for file in files:
        SendFile(path=path, filename=file)
