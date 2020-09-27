from PostgreSQL.Prueba_inicial.connect import connect
from sqlalchemy import create_engine

class Data_base():

    def __init__(self,file_Name,connect_info):
        self.db_file=file_Name
        self.engine = create_engine(connect_info)
        self.conn = connect(self.db_file)
        self.c = self.conn.cursor()


    def create_table(self,name_table,columns):
        self.c.execute("CREATE TABLE IF NOT EXISTS {}({})".format(name_table,columns))
        self.conn.commit()
    def print_table_data(self,stock):
        self.c.execute('''  
        SELECT * FROM {}'''.format(stock))
        #print(stock)
        for row in self.c.fetchall():
            print (row)

    def data_entry(self,name_table,name_column, entities):
        #print("INSERT INTO {}".format(name_table) + " ({} ) VALUES".format(name_column) + " ({})".format(input_data))
        self.c.execute('''INSERT INTO {}  ( {} ) VALUES( ? )'''.format(name_table,name_column),entities)
        self.conn.commit()


    def add_columns(self,name_table,name_column,type_value):
        self.c.execute("ALTER TABLE {} ADD {} {}".format(name_table,name_column,type_value))
        self.conn.commit()
    def select_from_data(self,name_table):
        self.c.execute('SELECT * FROM {}'.format(name_table))

    def finish_connection(self):
        self.c.close()
        self.conn.close()

