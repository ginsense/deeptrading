from yahoo_fin.stock_info import *

from deeptrading.main.functions.Manage_Databes import Manage_Database
from deeptrading.main.functions.Stock import Stock,Real_values,Predictions_LSTM_1step

import datetime
#### Actualizar todas las bases de datos




##Asi creo la base de datos inicial
new_database=Manage_Database()
#for ticker in (tickers_dow()):
#new_database.create_database(tickers_dow())
#sp500.create_database(tickers_sp500())
start_time=datetime.datetime(2020,9,21).strftime('%Y-%m-%d')
end_time=datetime.datetime(2020, 9, 23).strftime('%Y-%m-%d')
candle,vol=new_database.input_gaphs(stock_name='AAPL',start_time=start_time,end_time=end_time)

print(candle)
print(vol)

###Aca trabajo con las bases de datos ya creadas y las actualizo cada una

#stocks=new_database.session.query(Stock).all()
#print('\n### All Stocks:')
#contador=0
#for stock in stocks:
    #stock.__repr__()
    #new_database.Stocktiwtts_extractor(stock=stock)
    #dataframe=new_database.get_Stock_to_dataframe(stock.name)
    #dataframe_ordenado=dataframe.sort_values('Time')
    #print(dataframe_ordenado)
    #new_database.create_bollinger_bands(dataframe_ordenado,stock)
    #new_database.create_Top3_indicators(dataframe_prices=dataframe_ordenado,stock=stock)
    #new_database.create_MACD(dataframe_prices=dataframe_ordenado,stock=stock)
    #training_data=Get_data_LSTM1step()
    #training_data.get_data_from_databse(dataframe_ordenado)

    #weight_file='C:/Users/56979/PycharmProjects/Stocks_predictions/GAN/Saved_models/LSTM_1step_weight.h5'

    #lstm = TrainLSTM_1step(training_data=training_data.data,weight_file=weight_file,
    #                       num_feature=training_data.num_features)
    #lstm.train()
    #contador+=1
    #print('el valor del contador es : {}'.format(contador))



    #new_database.detect_holes(dataframe=dataframe_ordenado,stock=stock)
    #new_database.update_prices(stock)

##Se cierra la session del database
new_database.finish_connection()