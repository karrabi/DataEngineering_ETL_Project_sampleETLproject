CREATE DATABASE "extracted_data"
    WITH 
    OWNER = postgresuser
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
	
	
	
	
\c extracted_data postgresuser;

CREATE TABLE IF NOT EXISTS public.extracted_candles
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    volume numeric,
    symbol character varying(100) COLLATE pg_catalog."default" NOT NULL,
    resolution character varying(100) COLLATE pg_catalog."default",
    "timestamp" bigint NOT NULL,
    isloaded boolean DEFAULT false,
    create_time timestamp with time zone DEFAULT timezone('utc'::text, CURRENT_TIMESTAMP)
)PARTITION BY RANGE("timestamp");

ALTER TABLE IF EXISTS public.extracted_candles
    OWNER to postgresuser;
	
CREATE TABLE extracted_candles_y2022m11 PARTITION OF extracted_candles
  FOR VALUES FROM (1667260800) TO (1669852800);
	
CREATE TABLE extracted_candles_y2022m12 PARTITION OF extracted_candles
  FOR VALUES FROM (1669852800) TO (1672531200);
	
CREATE TABLE extracted_candles_y2023m01 PARTITION OF extracted_candles
  FOR VALUES FROM (1672531200) TO (1675209600);
	
CREATE TABLE extracted_candles_y2023m02 PARTITION OF extracted_candles
  FOR VALUES FROM (1675209600) TO (1677628800);
	
CREATE TABLE extracted_candles_y2023m03 PARTITION OF extracted_candles
  FOR VALUES FROM (1677628800) TO (1680307200);
	
CREATE TABLE extracted_candles_y2023m04 PARTITION OF extracted_candles
  FOR VALUES FROM (1680307200) TO (1682899200);
	
CREATE TABLE extracted_candles_y2023m05 PARTITION OF extracted_candles
  FOR VALUES FROM (1682899200) TO (1685577600);
	
CREATE TABLE extracted_candles_y2023m06 PARTITION OF extracted_candles
  FOR VALUES FROM (1685577600) TO (1688169600);
	
CREATE TABLE extracted_candles_y2023m07 PARTITION OF extracted_candles
  FOR VALUES FROM (1688169600) TO (1690848000);
	
CREATE TABLE extracted_candles_y2023m08 PARTITION OF extracted_candles
  FOR VALUES FROM (1690848000) TO (1693526400);
	
CREATE TABLE extracted_candles_y2023m09 PARTITION OF extracted_candles
  FOR VALUES FROM (1693526400) TO (1696118400);
	
CREATE TABLE extracted_candles_y2023m10 PARTITION OF extracted_candles
  FOR VALUES FROM (1696118400) TO (1698796800);


CREATE INDEX extracted_candles_timestamp_idx
  ON extracted_candles("timestamp");
