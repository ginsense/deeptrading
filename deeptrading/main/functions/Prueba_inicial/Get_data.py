

import yfinance as yf
from yahoo_fin.stock_info import *
from pandas import DataFrame
from PostgreSQL.Prueba_inicial.Data_Base_manage import Data_base
import datetime



class Get_data():
    def __init__(self,NAME_database, conection_info):
        self.my_data=Data_base(NAME_database,conection_info)

    ###obtengo valores de un stock  por minuto
    def get_yfinance(self,stock,period):
        features = ['Open', 'High', 'Low', 'Close', 'Volume']
        val = yf.Ticker(stock)
        val_historical = val.history(period=period,interval="1m")
        return val_historical[features]

    # Obtiene los valores de una tabla
    def get_dfstock_from_database(self, name_table):

        df = DataFrame(self.my_data.c.execute('SELECT * FROM {}'.format(name_table)),
                       columns=['time','Open', 'High', 'Low', 'Close', 'Volume'])

        return df

    ## Crea un database de los indices economicos mas utilizados
    def update_database(self,tickers):
        for stock in tickers:
            df=self.get_dfstock_from_database(stock)
            last_time=list(df['time'].tail(1))
            end = datetime.datetime.now()
            t=last_time[0].split(' ')
            val = self.get_yfinance(stock,'id')
            print(val)
            if val.empty:
                print('no hay valores en {}'.format(stock))
                continue
            else:
                input_array=[]
                for index in val.index:
                    columns='Open ,High , Low , Close , Volume '
                    date=index.strftime("%Y-%m-%d %H:%M:%S")
                    print(index)
                    row=val.loc[index]
                    input_array.append(date)
                    input_array.append(row['Open'])
                    input_array.append(row['High'])
                    input_array.append(row['Low'])
                    input_array.append(row['Close'])
                    input_array.append(row['Volume'])
                    self.my_data.data_entry(name_table=stock,name_column=columns,entities=input_array)
        print('Se acabaron los tickers')
        return

    def create_database(self,tickers):
        for stock in tickers:
            #start=datetime.datetime(2020, 9, 11).strftime('%Y-%m-%d')
            #end=datetime.datetime.now()
            val = self.get_yfinance(stock,'5d')
            print(val)
            if val.empty:
                print('no hay valores en {}'.format(stock))
                continue
            else:
                print(stock)
                if stock == 'ELSE' or stock == 'ALL' or stock == 'ON':
                    continue
                self.my_data.create_table(name_table=stock,
                                     columns='Open REAL,High REAL, Low REAL, Close REAL, Volume REAL')
                val.to_sql(stock, self.my_data.engine, if_exists='replace', index=True)
        print('Se acabaron los tickers')










if __name__ == '__main__':
    #value=get_top_crypto()
    #print(value)
    #print(get_analysts_info('nflx'))
    print(get_day_most_active())
    live=get_live_price('nflx')
    print(live)
    #param_dic = {'host': 'localhost', 'database': 'prueba', 'user': 'postgres', 'password': 'sleepy1992', 'port': 5433}

    #connect = "postgresql+psycopg2://%s:%s@%s:5433/%s" % (param_dic['user'], param_dic['password'], param_dic['host'], param_dic['database'])
    #down_jones = tickers_dow()
    #data=Get_data('database.ini',connect)
    #data.create_database(down_jones)
    #tickers=data.my_data.name_table()
    #data.update_database()
    #print(tickers)
    #for stock in down_jones:
        #data.my_data.print_table_data(stock)
        #print(stock)
        ##print(frame)



    #nasdaq=tickers_nasdaq()
    #data.create_database(nasdaq)
    #dataframe=get_dataframe_from_database('Nasdaq.db')
    #dataframe1=get_dfstock_from_database('Nasdaq.db',nasdaq[0])

    #down_jones=tickers_dow()
    #others = tickers_other()
    #print(len(others))
    #sp500=tickers_sp500()
    #create_database('SP500',sp500)


