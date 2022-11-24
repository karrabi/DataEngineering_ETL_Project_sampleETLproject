CREATE DATABASE "Logs"
    WITH 
    OWNER = postgresuser
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
	
	
	
	
\c Logs postgresuser;

CREATE TABLE IF NOT EXISTS public.logs
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    server_id integer DEFAULT 1,
    message character varying(5000) COLLATE pg_catalog."default",
    create_time timestamp with time zone DEFAULT timezone('utc'::text, CURRENT_TIMESTAMP),
    CONSTRAINT logs_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

CREATE INDEX logs_create_time_idx
  ON logs(create_time);

  
ALTER TABLE IF EXISTS public.logs
    OWNER to postgresuser;
	
	