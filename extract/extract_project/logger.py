from sqlalchemy import create_engine

# Database connection string
CONNECTION_STRING = "postgresql://postgresuser:postgrespassword@logserver:5432/Logs"

# Create a database engine
engine = create_engine(CONNECTION_STRING)

def prepareMessage(message):
    """
    Prepare the log message by replacing single quotes with double quotes.

    Args:
        message (str): The log message to be prepared.

    Returns:
        str: The prepared log message.
    """
    return str(message).replace("'", '"')

def Log(message: str):
    """
    Log a message to the database.

    Args:
        message (str): The message to be logged.
    """
    try:
        sql_query = """
        INSERT INTO public.logs(server_id, message)
        VALUES (1, '{}');
        """.format(prepareMessage(message))
        connection = engine.connect()
        connection.execute(sql_query)
    except Exception as e:
        # Print an error message if the log couldn't be saved to the database
        print('Error saving log to the database: {} ///////// {}'.format(prepareMessage(sql_query), prepareMessage(e)))
