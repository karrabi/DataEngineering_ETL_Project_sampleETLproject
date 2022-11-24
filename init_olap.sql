CREATE DATABASE "dw"
    WITH 
    OWNER = postgresuser
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
	
	
	
	
\c dw postgresuser;

CREATE TABLE IF NOT EXISTS public.dim_resolutions
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    resolution character varying(100) COLLATE pg_catalog."default",
    create_time timestamp with time zone DEFAULT timezone('utc'::text, CURRENT_TIMESTAMP),
    CONSTRAINT dim_resolutions_pkey PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.dim_resolutions
    OWNER to postgresuser;
	
	
CREATE TABLE IF NOT EXISTS public.dim_symbols
(
    id BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    symbol character varying(100) COLLATE pg_catalog."default",
    create_time timestamp with time zone DEFAULT timezone('utc'::text, CURRENT_TIMESTAMP),
    CONSTRAINT dim_symbols_pkey PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.dim_symbols
    OWNER to postgresuser;
	

CREATE TABLE public.dim_times
(
  date_dim_id              BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
  "timestamp"              BIGINT NOT NULL,
  date_actual              DATE NOT NULL,
  time_actual			   TIME NOT NULL,
  "datetime"			   TIMESTAMP WITHOUT TIME ZONE NOT NULL,
  hour_actual			   INT NOT NULL,
  minute_actual			   INT NOT NULL,
  minute_of_day			   INT NOT NULL,
  day_suffix               VARCHAR(4) NOT NULL,
  day_name                 VARCHAR(9) NOT NULL,
  day_of_week              INT NOT NULL,
  day_of_month             INT NOT NULL,
  day_of_year              INT NOT NULL,
  week_of_month            INT NOT NULL,
  week_of_year             INT NOT NULL,
  week_of_year_iso         CHAR(10) NOT NULL,
  month_actual             INT NOT NULL,
  month_name               VARCHAR(9) NOT NULL,
  month_name_abbreviated   CHAR(3) NOT NULL,
  quarter_actual           INT NOT NULL,
  quarter_name             VARCHAR(9) NOT NULL,
  year_actual              INT NOT NULL,
  first_day_of_week        DATE NOT NULL,
  last_day_of_week         DATE NOT NULL,
  first_day_of_month       DATE NOT NULL,
  last_day_of_month        DATE NOT NULL,
  first_day_of_quarter     DATE NOT NULL,
  last_day_of_quarter      DATE NOT NULL,
  first_day_of_year        DATE NOT NULL,
  last_day_of_year         DATE NOT NULL,
  mmyyyy                   CHAR(6) NOT NULL,
  mmddyyyy                 CHAR(10) NOT NULL,
  weekend_indr             BOOLEAN NOT NULL
);

ALTER TABLE public.dim_times ADD CONSTRAINT dim_times_id_pk PRIMARY KEY (date_dim_id);

ALTER TABLE IF EXISTS public.dim_times
    OWNER to postgresuser;
	
CREATE INDEX dim_times_actual_idx
  ON dim_times(date_actual);
  
CREATE INDEX dim_times_timestamp_idx
  ON dim_times("timestamp");
  
  
CREATE TABLE IF NOT EXISTS public.fact_candles
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    volume numeric,
    symbol_id bigint,
    resolution_id bigint,
    "timestamp" bigint,
    create_time timestamp with time zone DEFAULT timezone('utc'::text, CURRENT_TIMESTAMP)
)PARTITION BY RANGE ("timestamp");

ALTER TABLE IF EXISTS public.fact_candles
    OWNER to postgresuser;

CREATE TABLE fact_candles_y2022m11 PARTITION OF fact_candles
  FOR VALUES FROM (1667260800) TO (1669852800);
	
CREATE TABLE fact_candles_y2022m12 PARTITION OF fact_candles
  FOR VALUES FROM (1669852800) TO (1672531200);
	
CREATE TABLE fact_candles_y2023m01 PARTITION OF fact_candles
  FOR VALUES FROM (1672531200) TO (1675209600);
	
CREATE TABLE fact_candles_y2023m02 PARTITION OF fact_candles
  FOR VALUES FROM (1675209600) TO (1677628800);
	
CREATE TABLE fact_candles_y2023m03 PARTITION OF fact_candles
  FOR VALUES FROM (1677628800) TO (1680307200);
	
CREATE TABLE fact_candles_y2023m04 PARTITION OF fact_candles
  FOR VALUES FROM (1680307200) TO (1682899200);
	
CREATE TABLE fact_candles_y2023m05 PARTITION OF fact_candles
  FOR VALUES FROM (1682899200) TO (1685577600);
	
CREATE TABLE fact_candles_y2023m06 PARTITION OF fact_candles
  FOR VALUES FROM (1685577600) TO (1688169600);
	
CREATE TABLE fact_candles_y2023m07 PARTITION OF fact_candles
  FOR VALUES FROM (1688169600) TO (1690848000);
	
CREATE TABLE fact_candles_y2023m08 PARTITION OF fact_candles
  FOR VALUES FROM (1690848000) TO (1693526400);
	
CREATE TABLE fact_candles_y2023m09 PARTITION OF fact_candles
  FOR VALUES FROM (1693526400) TO (1696118400);
	
CREATE TABLE fact_candles_y2023m10 PARTITION OF fact_candles
  FOR VALUES FROM (1696118400) TO (1698796800);

CREATE INDEX fact_candles_timestamp_idx
  ON fact_candles("timestamp");

CREATE INDEX fact_candles_symbol_id_idx
  ON fact_candles("symbol_id");

CREATE INDEX fact_candles_resolution_id_idx
  ON fact_candles("resolution_id");


CREATE EXTENSION postgres_fdw;

create server oltp_server FOREIGN DATA WRAPPER postgres_fdw
options (host 'oltpserver', port '5432', dbname 'extracted_data');

create user mapping for postgresuser
server oltp_server
options (user 'postgresuser', password 'postgrespassword');

create foreign table oltp_extracted_candles(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    volume numeric,
    symbol character varying(100) COLLATE pg_catalog."default",
    resolution character varying(100) COLLATE pg_catalog."default",
    "timestamp" bigint,
    isloaded boolean DEFAULT false,
    create_time timestamp with time zone DEFAULT timezone('utc'::text, CURRENT_TIMESTAMP)
) server oltp_server 
options (schema_name 'public', table_name 'extracted_candles');



INSERT INTO dim_times ("timestamp", date_actual, time_actual,
	"datetime", hour_actual, minute_actual, minute_of_day,
	day_suffix, 
	day_name, day_of_week, day_of_month, 
	day_of_year, week_of_month, week_of_year, 
	week_of_year_iso, month_actual, month_name, 
	month_name_abbreviated, quarter_actual, 
	quarter_name, year_actual, first_day_of_week, 
	last_day_of_week, first_day_of_month, 
	last_day_of_month, first_day_of_quarter, 
	last_day_of_quarter, first_day_of_year, 
	last_day_of_year, mmyyyy, mmddyyyy, weekend_indr)
SELECT 
       EXTRACT(EPOCH FROM datum) AS "timestamp",
       datum::DATE AS date_actual,
	   datum::TIME AS time_actual,
	   datum AS "datetime",
	   EXTRACT('HOUR' FROM datum) AS hour_actual,
	   EXTRACT('MINUTE' FROM datum) AS minute_actual,
	   EXTRACT('HOUR' FROM datum)::INT * 60 + EXTRACT('MINUTE' FROM datum) AS minute_of_day,
       TO_CHAR(datum, 'fmDDth') AS day_suffix,
       TO_CHAR(datum, 'TMDay') AS day_name,
       EXTRACT(ISODOW FROM datum) AS day_of_week,
       EXTRACT(DAY FROM datum) AS day_of_month,
       EXTRACT(DOY FROM datum) AS day_of_year,
       TO_CHAR(datum, 'W')::INT AS week_of_month,
       EXTRACT(WEEK FROM datum) AS week_of_year,
       EXTRACT(ISOYEAR FROM datum) || TO_CHAR(datum, '"-W"IW-') || EXTRACT(ISODOW FROM datum) AS week_of_year_iso,
       EXTRACT(MONTH FROM datum::TIMESTAMP)::INT AS month_actual,
       TO_CHAR(datum, 'TMMonth') AS month_name,
       TO_CHAR(datum, 'Mon') AS month_name_abbreviated,
       EXTRACT(QUARTER FROM datum) AS quarter_actual,
       CASE
           WHEN EXTRACT(QUARTER FROM datum) = 1 THEN 'First'
           WHEN EXTRACT(QUARTER FROM datum) = 2 THEN 'Second'
           WHEN EXTRACT(QUARTER FROM datum) = 3 THEN 'Third'
           WHEN EXTRACT(QUARTER FROM datum) = 4 THEN 'Fourth'
           END AS quarter_name,
       EXTRACT(YEAR FROM datum) AS year_actual,
       datum + ((1 - EXTRACT(ISODOW FROM datum))::text || ' day')::interval AS first_day_of_week,
       datum + ((7 - EXTRACT(ISODOW FROM datum))::text || ' day')::interval AS last_day_of_week,
       datum + ((1 - EXTRACT(DAY FROM datum))::text || ' day')::interval AS first_day_of_month,
       (DATE_TRUNC('MONTH', datum) + INTERVAL '1 MONTH - 1 day')::DATE AS last_day_of_month,
       DATE_TRUNC('quarter', datum)::DATE AS first_day_of_quarter,
       (DATE_TRUNC('quarter', datum) + INTERVAL '3 MONTH - 1 day')::DATE AS last_day_of_quarter,
       TO_DATE(EXTRACT(YEAR FROM datum) || '-01-01', 'YYYY-MM-DD') AS first_day_of_year,
       TO_DATE(EXTRACT(YEAR FROM datum) || '-12-31', 'YYYY-MM-DD') AS last_day_of_year,
       TO_CHAR(datum, 'mmyyyy') AS mmyyyy,
       TO_CHAR(datum, 'mmddyyyy') AS mmddyyyy,
       CASE
           WHEN EXTRACT(ISODOW FROM datum) IN (6, 7) THEN TRUE
           ELSE FALSE
           END AS weekend_indr
FROM (select datum::timestamp from (
		SELECT '2022-11-01 00:00:00'::TIMESTAMP + seconds::interval as datum
		from (
		select tmp.secondss::char(50) || ' min' as seconds from 
			GENERATE_SERIES(1, 60*24*365) as tmp(secondss)) as tmp2) as tmp3) DQ
ORDER BY 1;



