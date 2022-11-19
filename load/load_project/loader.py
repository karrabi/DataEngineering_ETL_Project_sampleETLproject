import pandas as pd
from sqlalchemy import create_engine, select, Table, Column, MetaData, and_, func, Numeric, Integer, VARCHAR, update, insert
from logger import Log


CONNECTION_STRING = "postgresql://postgresuser:postgrespassword@olapserver:5432/dw"

engine = create_engine(
    CONNECTION_STRING
)


def update_dim_symbols():
    try:
        sql_query = """
        INSERT INTO dim_symbols (symbol)
            select distinct(symbol) from oltp_extracted_candles 
            where symbol not in (
                select symbol from dim_symbols
                );
        """
        connection = engine.connect()
        connection.execute(sql_query)
        Log('Dim Symbols Updated successfully')
    except Exception as e:
        Log(e)
        return False
    return True


def update_dim_resolutions():
    try:
        sql_query = """
        INSERT INTO dim_resolutions (resolution)
            select distinct(resolution) from oltp_extracted_candles 
            where resolution not in (
                select resolution from dim_resolutions
                );
        """
        connection = engine.connect()
        connection.execute(sql_query)
        Log('Dim Resolutions Updated successfully')
    except Exception as e:
        Log(e)
        return False
    return True


def load_Transformed_data():
    try:
        sql_query = """
        INSERT INTO public.fact_candles(
            open, high, low, close, volume, symbol_id, resolution_id, "timestamp")
        select 
        oec.open, 
        oec.high, 
        oec.low, 
        oec.close,
        oec.volume,
        ds.id as symbol_id,
        dr.id as resolution_id, 
        oec.timestamp
        from
        oltp_extracted_candles as oec
        left outer join
        dim_symbols as ds
        on
        oec.symbol = ds.symbol
        left outer join 
        dim_resolutions as dr
        on oec.resolution = dr.resolution
        where isloaded=False;

        update 
        oltp_extracted_candles
        set isloaded=True
        where isloaded=False;
        """
        connection = engine.connect()
        connection.execute(sql_query)
        Log('Transformed Data Load successfully')
    except Exception as e:
        Log(e)
        return False
    return True
