
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def connect_database(param_dic):
    connect = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(param_dic['user'], param_dic['password'], param_dic['host'],param_dic['port'] ,param_dic['database'])
    engine = create_engine(connect)
    return engine




# 2 - generate database schema
#Base.metadata.create_all(engine)


#### Actualizar todas las bases de datos

param_dic = {'host': 'localhost', 'database': 'dow_jones', 'user': 'postgres', 'password': 'pthecrow6908', 'port': 5432}



###Aca trabajo con las bases de datos ya creadas y las actualizo cada una

#diccionarios=[down_jones_param_dic,nasdaq_param_dic,sp500_param_dic]

engine = connect_database(param_dic)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
