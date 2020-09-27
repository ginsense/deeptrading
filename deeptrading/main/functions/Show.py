
from datetime import datetime
from  Data_manager_SQLalchemy import Session, engine, Base
from Stock import Stock , Real_values


# 2 - extract a session
session = Session()

stocks = session.query(Stock).all()

# 4 - print movies' details
print('\n### All movies:')
for stock in stocks:
    print(stock.name)
    print(stock.last_time)
    #values=session.query(Real_values).filter(Real_values.stock_id == stock.id).all()


    #for val in values:
     #       val.repr()
print('')


#Apple=session.query(Indice.id ).join(Stock, Indice.stocks).filter(Stock.name == 'AAPL').all()

#print(Apple)

#for value in Apple:
#    print(value.name)
