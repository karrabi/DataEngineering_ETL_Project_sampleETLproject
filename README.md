SAMPLE DATA ETL PROJECT

Here you can find some info about this project
- [About the project](./README.md#about-the-project)
    - [EXTRACT](./README.md#extract)
    - [TRANSFORM](./README.md#transform)
- [About the codes](./README.md#about-the-codes)

# HOW TO RUN
Make a clone of project on your computer and open it

![inside basic_etl_project folder image](./docs/project%20folder.png)

Inside project folder run:
```
docker-compose up -d
```

also pgadmin is accessible by: http://localhost:15432

in pgadmin 3 database servers can easily add by its names:
-   ***logserver***  
    -   port: ***5432***
    -   username:   ***postgresuser***
    -   password:   ***postgrespassword***
-   ***oltpserver***
    -   port: ***5433***
    -   username:   ***postgresuser***
    -   password:   ***postgrespassword***
-   ***olapserver***
    -   port: ***5434***
    -   username:   ***postgresuser***
    -   password:   ***postgrespassword***

FTP Server is accessible by: ftp://localhost

to see whats happening, just look inside ***logs*** table in ***Logs*** database in ***logserver***


---
---
# About the Project Infrastructure

This project containerized with Docker
Whole Farm consists of:
- 3 postgres Database Server as:
    - Log Server
    - OLTP Server
    - OLAP Server
- 1 pgadmin to access Database servers from web
- 1 FTP Server as DATALAKE
- 3 python Application Server as:
    - Extract Server
    - Transform Server
    - Load Server

Inside [docker file](./docker-compose.yaml) each Database Servers has its own init.sql file to create required objects

Log Database Server [init file](./init_log.sql) create **Logs** database and logs table

OLTP Database Server [init file](./init_oltp.sql) create **extracted_data** database and required tables

OLAP Database Server [init file](./init_olap.sql) create **dw** database and required tables

Each application runs in its own server. application servers build through Dockerfiles inside its own subfolders.


---
---
# About the Project Structure
This is a very simple Data ETL project.
In fintech that process crypto currencies stock market data, access and process crypto's data is a fundamental need.

gather crypto data from various resources, do some process on it and finally send and save them in data warehouses for further use is a Data Engineer job.
Here is a very simple data ETL project just to show how it can be happen.

This project consists of three main part:

[Extract](./README.md#extract)
   > the part that extract data from data source 

[Transform](./README.md#transform)
   > the part that transform data to the required shape and save it to OLTP database

[Load](./README.md#load)
   > and finally the part that load data from OLTP database to OLAP data warehouse

Each project consists of following files:
- main.py
    - main module
- logger.py
    - responsible to saving (log) messages into logserver's Logs database
- fetcher.py `(only in **extract** project)`
    - responsible to connect to Web API and extract data from it
- filemanager.py
    - responsible to connect to FTP server and manage files
- oltp_server.py `(only in **transform** project)`
    - responsible to save data in OLTP Server
- loader.py `(only in **load** project)`
    - responsible to load data from OLTP database to Data Warehouse
- summary.csv `(only in **extract** project)`
    - save some info about newly extracted data for each symbol
- symbols.csv `(only in **extract** project)`
    - contains Symbols list to process

## EXTRACT
About data resource:

<table border>
<tr><td>Type</td><td>Web API</td></tr>
<tr><td>Authentication</td><td>API Key</td></tr>
<tr><td>Data Type</td><td>1 minute Crypto Candle Data</td></tr>
<tr><td>Call Interval</td><td>every 5 minutes</td></tr>
<tr><td>Address</td><td>https://finnhub.io</td></tr>
<tr><td>API Documentation</td><td>https://finnhub.io/docs/api</td></tr>
<tr><td>Libraries</td><td>https://finnhub.io/docs/api/library</td></tr>
</table>

Crypto currency symbols simply stores in [symbols.csv](./extract/extract_project/symbols.csv). you can add more currencies in specified format to this file.

After read symbols names from above file, a thread create for each one, so, extract data from Web API executes in parrall.

after extraction, each thread stores extracted data to curresponding .csv file in **files** folder and also stores **last record's timestamp** to [summary.csv](./extract/extract_project/summary.csv) file for the next extraction round (extract records after last stored timestamp)

Finally, all new extracted files are sent to a FTP Server **(DataLake)** inside **fromapi1min** folder and removed from the **files** folder.



## TRANSFORM

**TRANSFORM** part of project reads all new extracted .csv files from **DataLake** 
Then transform Data mostly via ***simpledataengineeringtoolkit*** library that also accessable from [here](https://pypi.org/project/simpledataengineeringtoolkit/) as the main library to help data engineers reshape or transform data.
you can simply use this library by:

```
pip install simpledataengineeringtoolkit
```

Library source code also available in [here](https://github.com/karrabi/simpledataengineeringtoolkit)

And finally store all data in a OLTP database.

## LOAD

In **LOAD** part, first of all, the **Dimention Tables** in OLAP database update with new data, and then all new records in OLTP database loads to OLAP database **Fact Tables**

---
---
# About the codes


## EXTRACT
The **Extract** Code has 2 main part:
1. Check Time Interval
2. extract new Data
3. send Data to DataLake

### Part 1 (Check Time Interval):

1. Read List of symbols

```python
def retriveSymbols():
    symbols = pd.read_csv('symbols.csv')
    return symbols
```
2. Login to FTP Server through `filemanager >> Login`


3. A forever loop continusely check if we are at the begining of a 5 min peroid to start extracting new Data through **run()** function and then move newly extracted data to DataLake (FTP Server in here)

```python
    while True:
        now = int(time.time())
        if now % 300 == 0:
            run( ... )
            ...
            fm.moveFilesToDataLake( ... )
```

inside **run()** function, a for iterator iterate over symbols list; for each symbol first detremined last extracted timestamp through:
```python
def retrive_from(symbol):
    history = pd.read_csv('summary.csv')
    history = history[history['symbol']==symbol]
    if history.shape[0] > 0:
        return max(history['to']) + 1
    else:
        return int(time.time()) - 8053600
```
function and then create an object of CryptoFetcher class and append it to threads list

> In ***retrive_from*** function, if a symbol has history data inside **summary.csv** file then the last timestamp is read from it and the function returns the last timestamp plus one to prevent record duplication in new data request otherwise if the symbol has no data in **summary.csv** file then the function assumes that the symbol is newly added to project and return a timestamp corresponding to about 90 days ago to retrieve historical data requires for further processes

after all objects creates for all symbols, all thread joins the main thread
### Part 2 (extract new Data):
**run** function iterate over ***Symbols*** list and create an object of **CryptoFetcher** for each one.

**CryptoFetcher** is a Thread base Object that connect to the [Finnhub](https://finnhub.io) web API and download specific Symbol Candle Data from it.

Then stores Downloaded Data as ***.csv*** file with Symbol name followed by start timestamp and end timestamp as filename. _(e.g.  BINANCE-1INCHUSDT_1668093311_1668093300.csv)_

file is stored in ***/files*** folder.

### Part 3 
After All Data Extracted from Web API and store as ***.csv*** files then **moveFilesToDataLake** module is sent all new created files to DataLake _(FTP Server in here)_



# TRANSFORM
this is the transform part


# LOAD
this is the transform part


```python
def Log(message:str):
    _t = '001'
    try:
        sql_query = """
        INSERT INTO public.logs(server_id, message)
        VALUES (1,'{}');
        """.format(prepareMessage(message))
        connection = engine.connect()
        connection.execute(sql_query)
    except Exception as e:
        print('Error saving log to database: {} ///////// {}'.format(prepareMessage(sql_query), prepareMessage(e)))
```