import pandas as pd
from sqlalchemy import create_engine, select, Table, Column, MetaData, and_, func, Numeric, Integer, VARCHAR, update, insert

CONNECTION_STRING = "postgresql://postgresuser:postgrespassword@logserver:5432/Logs"

engine = create_engine(
    CONNECTION_STRING
)

    
def prepareMessage(message):
    return str(message).replace("'", '"')


def Log(message:str):
    _t = '001'
    try:
        sql_query = """
        INSERT INTO public.logs(server_id, message)
        VALUES (2, '{}');
        """.format(prepareMessage(message))
        connection = engine.connect()
        connection.execute(sql_query)
    except Exception as e:
        print('Error saving log to database: {} ///////// {}'.format(prepareMessage(sql_query), prepareMessage(e)))