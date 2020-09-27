import psycopg2
from PostgreSQL.Prueba_inicial.config import config


def connect(filename):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config(filename=filename)

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        return conn

        # create a cursor
        #cur = conn.cursor()

        # execute a statement
        #print('PostgreSQL database version:')
        #cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        #db_version = cur.fetchone()
        #print(db_version)

        # close the communication with the PostgreSQL
        #cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            return conn
            #conn.close()
            #print('Database connection closed.')


if __name__ == '__main__':
    connect()