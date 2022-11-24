import pandas as pd
import time

from simpledataengineeringtoolkit.checker import ValueChecker, ColumnChecker, NanValues
from simpledataengineeringtoolkit.cleaner import ValueCleaner, ColumnCleaner

from oltp_server import save_to_database
from logger import Log
import filemanager as fm

EXTRACTED_PATH = '/fromapi1min'
ARCHIVE_PATH = '/archivefromapi1min'
TRANSFORMED_PATH = '/transformedfromapi1min'
TEMP_PATH = 'temp/'

def resolveSymbols():
    symbols = pd.read_csv('symbols.csv')
    return symbols


def resolve_from(symbol):
    history = pd.read_csv('summary.csv')
    history = history[history['symbol']==symbol]
    if history.shape[0] > 0:
        return max(history['to']) + 1
    else:
        return int(time.time()) - 8053600

def readData(files_list):
    new_data = pd.DataFrame()
    ignored=[]
    for file in files_list:
        if fm.RetriveFile(EXTRACTED_PATH, TEMP_PATH, file):
            file_data = pd.read_csv(TEMP_PATH+file)
            new_data = new_data.append(file_data)
        else:
            ignored.append(file)
    return new_data, ignored


def __monolithColumns(data_frame):
    columns = {
        'c': 'close', 
        'h': 'high', 
        'l': 'low',
        'o': 'open',
        't': 'timestamp',
        'v': 'volume'
        }

    data_frame.rename(columns=columns, inplace=True)


def resampleDataToFiveMin(dataframe:pd.DataFrame):
    fiveMinData = dataframe.copy(deep=True)
    
    fiveMinData['timestamp'] = pd.to_datetime(fiveMinData['t'], unit='s')
    fiveMinData.set_index('timestamp', inplace=True)
    
    agg_dict = {'o': 'first', 'h': 'max', 'l': 'min', 'c': 'last', 'v': 'mean', 't': 'min'}
    fiveMinData = fiveMinData.resample('5T').agg(agg_dict)
    fiveMinData.reset_index(drop=True, inplace=True)
    
    return fiveMinData
    
def transformData(new_data:pd.DataFrame, symbol_name):
    
    vck = ValueChecker(dataframe=new_data, reset_index=True)
    vck.CheckFloatValues('o',change_type_to_float=True,
                        remove_thousands_seperator=True,
                        nan_values_set_to=NanValues.DropNan)
    vck.CheckFloatValues('h',change_type_to_float=True,
                        remove_thousands_seperator=True,
                        nan_values_set_to=NanValues.DropNan)
    vck.CheckFloatValues('l',change_type_to_float=True,
                        remove_thousands_seperator=True,
                        nan_values_set_to=NanValues.DropNan)
    vck.CheckFloatValues('c',change_type_to_float=True,
                        remove_thousands_seperator=True,
                        nan_values_set_to=NanValues.DropNan)
    
    vck.CheckUnixTimestampValues(column='t', base='s', remove='*', 
                                nan_values_set_to=NanValues.DropNan)
    
    cck = ColumnChecker(dataframe=new_data, necessary_columns=['c', 'h', 'o', 'l', 't', 'v'])
    cck.CheckNecessaryColumns()
    
    ccl = ColumnCleaner(dataframe=new_data, reset_index=False,
                        necessary_columns=['c', 'h', 'o', 'l', 't', 'v'])
    ccl.RemoveUnnecessaryColumns()
    
    
    vcl = ValueCleaner(dataframe=new_data, reset_index=True)
    vcl.RemoveDuplicateValues(keep='first')
    vcl.RemoveNanValues(how='any')

    
    fiveMinResData = resampleDataToFiveMin(dataframe=new_data)
    
    __monolithColumns(data_frame=fiveMinResData)
    
    fiveMinResData['symbol'] = symbol_name
    fiveMinResData['resolution'] = '5min'
    
    __monolithColumns(data_frame=new_data)

    new_data['symbol'] = symbol_name
    new_data['resolution'] = '1min'
    
    new_data = new_data.append(fiveMinResData, ignore_index=True)
    
    return new_data
    

def saveDataToOLTPDatabase(symbol_name, transformed_data):
    Log('{} New Records of {} Retrived for Transform'.format(transformed_data.shape[0], symbol_name))
    save_to_database(data=transformed_data)



def saveDataToCSVFile(symbol_name, transformed_data):
    _from = min(transformed_data['timestamp'])
    _to = max(transformed_data['timestamp'])
    filename = '{}_{}_{}.csv'.format(symbol_name, _from, _to)
    transformed_data.to_csv('{}{}'.format(TEMP_PATH,filename))
    fm.SendFile(TRANSFORMED_PATH, TEMP_PATH,filename)
    
def archivedNewExtactedData(next_new_files, ignored, symbol_name):
    if len(ignored) > 0:
        next_new_files = [x for x in next_new_files if x not in ignored]

    Log('{} New Extracted Files of {} Archived after Transform'.format(len(next_new_files), symbol_name))
    fm.archiveFiles(EXTRACTED_PATH, ARCHIVE_PATH, TEMP_PATH, next_new_files)
    
def transformNewExtractedData():
    while True:
        next_new_files, symbol_name = fm.listNextExtractedFile(EXTRACTED_PATH)
        while len(next_new_files) > 0:
            
            Log('{} New Extracted Files of {} Start to Retrive for Transform'.format(len(next_new_files), symbol_name))
            
            new_data, ignored = readData(next_new_files)
            
            transformed_data = transformData(new_data, symbol_name)

            saveDataToOLTPDatabase(symbol_name, transformed_data)

            archivedNewExtactedData(next_new_files, ignored, symbol_name)

            next_new_files, symbol_name = fm.listNextExtractedFile(EXTRACTED_PATH)
            
        time.sleep(10)



def main():
    
    fm.Login(EXTRACTED_PATH)

    transformNewExtractedData()


if __name__ == '__main__':
    main()
    