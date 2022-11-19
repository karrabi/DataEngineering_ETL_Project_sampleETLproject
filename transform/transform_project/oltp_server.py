import pandas as pd
from sqlalchemy import create_engine, select, Table, Column, MetaData, and_, func, Numeric, Integer, VARCHAR, update, insert
from logger import Log

CONNECTION_STRING = "postgresql://postgresuser:postgrespassword@oltpserver:5432/extracted_data"

engine = create_engine(
    CONNECTION_STRING
)

def save_to_database(data):
    try:
        data.to_sql("extracted_candles", con=engine, index=False, if_exists='append')
        Log('{} Records Save to OLTP Database'.format(data.shape[0]))
    except Exception as e:
        Log(e)

