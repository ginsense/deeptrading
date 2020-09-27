from datetime import datetime
import  main.functions.Data_manager_SQLalchemy as db
from sqlalchemy.orm import sessionmaker

import yfinance as yf
import pandas as pd
from main.functions.Stock import Stock,Real_values,Bollinger_Band,Top_3_indicator,MACD_values,StockTwits
from main.functions.Technical_Analysis import BollBnd,MA,EMA,Momentum,MACD
import time
import requests

import json

#Entrega los ultimos n valores de un dataframe
def get_last_n_values(dataframe,n):
    return dataframe.tail(n)

###obtengo valores de un stock  por minuto
def get_yfinance( stock, period):
    features = ['Open', 'High', 'Low', 'Close', 'Volume']
    val = yf.Ticker(stock)
    val_historical = val.history(period=period, interval="1m")
    return val_historical[features]


## Clase para manejar una base de datos
class Manage_Database():

    def __init__(self):
        self.engine = db.engine
        self.Session = sessionmaker(bind=self.engine)
        self.session = db.Session()
        self.Base = db.Base
        # 2 - generate database schema
        self.Base.metadata.create_all(self.engine)

    ## Crea una base de datos de un indice en particular (probado con el Down Jones)
    def create_database(self,list_stocks):
        for ticker in list_stocks:
            new_stock = Stock(ticker)
            prices = get_yfinance(new_stock.name, '5d')
            prices.dropna(inplace=True)
            if prices.empty:
                print('no hay valores en {}'.format(ticker))
                continue
            cont = 0
            # all_real_value=[]
            for time in prices.index:
                # print(time)
                row = prices.iloc[cont]
                Open = row['Open']
                Close = row['Close']
                High = row['High']
                Volume = row['Volume']
                Low = row['Low']
                values = Real_values(new_stock)
                values.add_value(time=time, open=Open, close=Close, high=High, low=Low, volume=Volume)
                self.session.add(values)

                cont += 1
                new_stock.last_time = time
                self.session.add(new_stock)
                self.session.commit()

    ## funcion que actualiza los valores de los precios
    def update_prices(self,stock):
        print(stock.name)
        prices = get_yfinance(stock.name, '5d')
        if prices.empty:
            return
        prices.dropna(inplace=True)
        prices_last=prices.tail(2)
        print(prices_last)
        last_yahoo_time=prices_last.index[1]
        last_yahoo_time_string = last_yahoo_time.strftime("%Y-%m-%d %H:%M:%S")
        last_yahoo_time_datetime = datetime.strptime(last_yahoo_time_string, "%Y-%m-%d %H:%M:%S")

        #cont = 0
        last_time_string = stock.last_time.strftime("%Y-%m-%d %H:%M:%S")
        last_time= datetime.strptime(last_time_string, "%Y-%m-%d %H:%M:%S")

        print(last_yahoo_time_datetime)
        print(last_time)
        self.fill_prices(t1=last_time,t2=last_yahoo_time_datetime,stock=stock,prices=prices)
        last_update_time = prices_last.index[0]
        last_update_time_string = last_update_time.strftime("%Y-%m-%d %H:%M:%S")
        last_update_time_datetime = datetime.strptime(last_update_time_string, "%Y-%m-%d %H:%M:%S")
        print('new last update')
        print(last_update_time_datetime)
        stock.last_time=last_update_time_datetime

#Convierte  una tabla de sql en dataframe (pensada para tener la tabla stock de la base de datos y luego poder iterar en todos los stocks dentro de esa base
#Para nuestro caso table_name puede ser stock o Real_value por ahora

    def sql_to_dataframe(self,table_name='Stock'):
        table_df = pd.read_sql_table(table_name,con=self.engine,index_col='stock_id')
        return table_df


#Entrega un dataframe de un stock en particular, solo necesita el nombre del stock y una session de la base de datos
    def get_Stock_to_dataframe(self,stock_name,start,end):
            stock_values=self.session.query(Stock).filter(Stock.name == stock_name)
            for stock in stock_values:
                #print(stock.name)
                stock_pd= pd.read_sql(self.session.query(Real_values).filter(Real_values.stock_id == stock.id).filter(start<=Real_values.Time).filter( Real_values.Time <= end).statement, con=self.engine)
            return stock_pd

    def input_gaphs(self,stock_name,start_time,end_time):
        pd = self.get_Stock_to_dataframe(stock_name=stock_name, start=start_time, end=end_time)
        pd = pd.sort_values('Time')
        cont = 0
        candle_stick = {}
        volume={}
        for val in pd.index:
            row = pd.iloc[cont]
            time = row['Time']
            time_string = time.strftime("%Y-%m-%d %H:%M:%S")
            open = row['Open']
            high = row['High']
            close = row['Close']
            low = row['Low']
            vol = row['Volume']
            dicc = {'o': open, 'h': high, 'l': low, 'c': close}
            candle_stick[time_string] = dicc
            volume['t': time_string] = vol
            ########## FALTA PRINTEAR ESTO
            cont += 1
        return candle_stick,volume

    def finish_connection(self):
        self.session.close()

    def detect_holes(self,dataframe,stock):
        for val in dataframe.index:
            if val < len(dataframe.index) - 1:
                time = dataframe.iloc[val]['Time']
                next_time = dataframe.iloc[val + 1]['Time']
                difference = next_time.minute - time.minute
                if difference > 1:
                    print('Aca hay mas de un minuto de diferencia')
                    print(time)
                    print(next_time)
                    print(difference)
                    prices = get_yfinance(stock.name, '5d')
                    self.fill_prices(t1=time, t2=next_time, stock=stock,prices=prices)
            else:
                print('ultimo valor')

    def fill_prices(self,t1, t2, stock,prices):
        cont1 = 0
        cont_t1 = 0
        cont_t2 = 0
        for date in prices.index:
            time_string = date.strftime("%Y-%m-%d %H:%M:%S")
            date_val = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
            if date_val == t1:
                cont_t1 = cont1
            if date_val == t2:
                cont_t2 = cont1
            cont1 += 1
        hole = prices.iloc[cont_t1:cont_t2]
        print(hole)
        cont=0
        for time in hole.index:
            time_string = time.strftime("%Y-%m-%d %H:%M:%S")
            t_value = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
            lastest = max((t1, t_value))  # Si es t1, significa que no es necesario agregar
            print(lastest)
            if lastest == t_value and lastest!=t1:
                print('hay nuevos valores')
                print('t value :')
                print(t_value)
                print('t1 :')
                print(t1)
                row=hole.iloc[cont]
                Open = row['Open']
                Close = row['Close']
                High = row['High']
                Volume = row['Volume']
                Low = row['Low']
                values = Real_values(stock)
                values.add_value(time=t_value, open=Open, close=Close, high=High, low=Low, volume=Volume)
                self.session.add(values)
                self.session.commit()
            cont+=1

    def create_bollinger_bands(self,dataframe_prices,stock,n=5):
        features=['Time','Open', 'High', 'Low', 'Close', 'Volume']
        selected_data=dataframe_prices[features]
        data=BollBnd(DF=selected_data,n=n)
        #print(data)
        cont=0
        for date in data.index:
            #print(date)
            # print(time)
            row = data.iloc[cont]
            #print(row)
            time = row['Time']
            bb_up = row['BB_up']
            bb_down = row['BB_dn']
            bb_width = row['BB_width']
            bb_band = Bollinger_Band(stock=stock)
            bb_band.add_value(time=time,bb_up=bb_up, bb_down=bb_down, bb_width=bb_width)
            self.session.add(bb_band)
            self.session.commit()
            cont+=1

    def create_Top3_indicators(self,dataframe_prices,stock,n=20):
        print(stock.name)
        features=['Time','Open', 'High', 'Low', 'Close', 'Volume']
        selected_data=dataframe_prices[features]
        ma=MA(dataset=selected_data,window=n)
        ema=EMA(dataset=ma)
        data=Momentum(dataset=ema,n=n)

        print(data)
        cont=0
        for date in data.index:
            #print(date)
            # print(time)
            row = data.iloc[cont]
            print(row)
            time = row['Time']
            ma = row['ma{}'.format(n)]
            ema = row['ema']
            momentum = row['Momentum{}'.format(n)]
            top3_indicators = Top_3_indicator(stock=stock)
            top3_indicators.add_value(time=time,ma=ma, ema=ema, momentum=momentum)
            self.session.add(top3_indicators)
            self.session.commit()
            cont+=1

    def create_MACD(self, dataframe_prices, stock):
            print(stock.name)
            features = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            selected_data = dataframe_prices[features]
            data = MACD(DF=selected_data)

            print(data)
            cont = 0
            for date in data.index:
                # print(date)
                # print(time)
                row = data.iloc[cont]
                print(row)
                time = row['Time']
                ma_fast = row['MA_Fast']
                ma_slow = row['MA_Slow']
                Macd = row['MACD']
                signal= row['Signal']
                macd = MACD_values(stock=stock)
                macd.add_value(time=time, ma_fast=ma_fast, ma_slow=ma_slow, macd=Macd,signal=signal)
                self.session.add(macd)
                self.session.commit()
                cont += 1

    def Stocktiwtts_extractor(self,stock):
        SYMBOL=stock.name
        last_message_id=stock.last_StockTwits_message_id

        # req_proxy = RequestProxy()
        token = 0
        access_token = ['', 'access_token=32a3552d31b92be5d2a3d282ca3a864f96e95818&',
                        'access_token=44ae93a5279092f7804a0ee04753252cbf2ddfee&',
                        'access_token=990183ef04060336a46a80aa287f774a9d604f9c&']

        stocktwit_url = "https://api.stocktwits.com/api/2/streams/symbol/" + SYMBOL + ".json?" + access_token[token]
        if last_message_id is not None:
            stocktwit_url += "max=" + str(last_message_id)

        api_hits = 0
        while True:
            # response = req_proxy.generate_proxied_request(stocktwit_url)
            try:
                response = requests.get(stocktwit_url)
            except Exception:
                response = None

            if response is not None:

                if response.status_code == 429:
                    print("###############")
                    print(response.headers['X-RateLimit-Reset'])
                    time_response=int(response.headers['X-RateLimit-Reset']) - int(time.time())
                    print("REQUEST IP RATE LIMITED FOR {} seconds !!!".format(time_response))

                if not response.status_code == 200:
                    stocktwit_url = "https://api.stocktwits.com/api/2/streams/symbol/" + SYMBOL + ".json?" + \
                                    access_token[token] + "max=" + str(last_message_id)
                    token = (token + 1) % (len(access_token))
                    continue

                api_hits += 1
                response = json.loads(response.text)
                last_message_id = response['cursor']['max']
                # NO MORE MESSAGES
                if not response['messages']:
                    print('There is no message')
                    stock.last_StockTwits_message_id = last_message_id
                    break
                # WRITE DATA TO CSV FILE
                for message in response['messages']:
                    print(message)
                    # PREPARE OBJECT TO WRITE IN CSV FILE
                    text = message['body']
                    time2 = message['created_at']
                    user = message['user']['id']
                    message_id = message['id']
                    twits_message = StockTwits(stock=stock)
                    twits_message.add_value(time=time2, user=user, message=text, message_id=message_id)
                    twits_message.repr()
                    self.session.add(twits_message)
                    last_message_id=message_id
                    self.session.commit()

                print("API HITS TILL NOW = {}".format(api_hits))



            # ADD MAX ARGUMENT TO GET OLDER MESSAGES
            stocktwit_url = "https://api.stocktwits.com/api/2/streams/symbol/" + SYMBOL + ".json?" + access_token[token] + "max=" + str(last_message_id)

            token = (token + 1) % (len(access_token))
            print(token)










#### Actualizar todas las bases de datos
























