import  main.functions.Data_manager_SQLalchemy as db
from sqlalchemy import Column, Integer, String, Float,Table,ForeignKey,REAL, DateTime,TEXT
from sqlalchemy.orm import relationship




class Real_values(db.Base):
    __tablename__ = 'Real_values'

    id = Column(Integer, primary_key=True)
    Time = Column('Time',DateTime,nullable=True)
    Open = Column('Open',REAL,nullable=True)
    Close=Column('Close',REAL,nullable=True)
    High = Column('High',REAL,nullable=True)
    Low = Column('Low',REAL,nullable=True)
    Volume = Column('Volume',REAL,nullable=True)
    stock_id = Column(Integer, ForeignKey('Stock.id'))
    stock = relationship("Stock", back_populates="Real_prices")

    def __init__(self,stock):
        self.stock=stock

    def add_value(self,time,open,close,high,low,volume):
        self.Time=time
        self.Open=open
        self.Close=close
        self.High=high
        self.Low=low
        self.Volume=volume

    def repr(self):
        print('Time: {} Open: {} Close: {} High: {} Low : {} Volume :{}'.format(self.Time,self.Open,self.Close,self.High,self.Low,self.Volume))

class Predictions_LSTM_1step(db.Base):
    __tablename__ = 'Predictions_LSTM_1step_values'

    id = Column(Integer, primary_key=True)
    Time = Column('Time',DateTime,nullable=True)
    Open = Column('Open',REAL,nullable=True)
    Close=Column('Close',REAL,nullable=True)
    High = Column('High',REAL,nullable=True)
    Low = Column('Low',REAL,nullable=True)
    Volume = Column('Volume',REAL,nullable=True)
    stock_id = Column(Integer, ForeignKey('Stock.id'))
    stock = relationship("Stock", back_populates="Predictions_LSTM_1step_prices")

    def __init__(self,stock):
        self.stock=stock

    def add_value(self,time,open,close,high,low,volume):
        self.Time=time
        self.Open=open
        self.Close=close
        self.High=high
        self.Low=low
        self.Volume=volume

    def repr(self):
        print('Time: {} Open: {} Close: {} High: {} Low : {} Volume :{}'.format(self.Time,self.Open,self.Close,self.High,self.Low,self.Volume))

class Bollinger_Band(db.Base):
    __tablename__ = 'Bollinger_Band'

    id = Column(Integer, primary_key=True)
    Time = Column('Time', DateTime, nullable=True)
    BB_UP= Column('BB_UP', REAL, nullable=True)
    BB_DOWN = Column('BB_DOWN', REAL, nullable=True)
    BB_WIDTH = Column('BB_WIDTH', REAL, nullable=True)
    stock_id = Column(Integer, ForeignKey('Stock.id'))
    stock = relationship("Stock", back_populates="Bollinger_bands")

    def __init__(self, stock):
        self.stock = stock

    def add_value(self, time, bb_up, bb_down, bb_width):
        self.Time = time
        self.BB_UP = bb_up
        self.BB_DOWN = bb_down
        self.BB_WIDTH = bb_width

    def repr(self):
        print('Time: {} bollinger up: {} bollinger down: {} bollinger width: {} '.format(self.Time, self.BB_UP, self.BB_DOWN,self.BB_WIDTH))
class MACD_values(db.Base):
    __tablename__ = 'MACD_values'

    id = Column(Integer, primary_key=True)
    Time = Column('Time', DateTime, nullable=True)
    MA_FAST= Column('MA_Fast', REAL, nullable=True)
    MA_SLOW= Column('MA_Slow', REAL, nullable=True)
    MACD= Column('MACD', REAL, nullable=True)
    Signal= Column('Signal', REAL, nullable=True)
    stock_id = Column(Integer, ForeignKey('Stock.id'))
    stock = relationship("Stock", back_populates="MACD_value")

    def __init__(self, stock):
        self.stock = stock

    def add_value(self, time, ma_fast, ma_slow, macd,signal):
        self.Time = time
        self.MA_FAST = ma_fast
        self.MA_SLOW = ma_slow
        self.MACD = macd
        self.Signal = signal

    def repr(self):
        print('Time: {} MA FAST: {} MA SLOW: {} MACD: {}  Signal : {}'.format(self.Time, self.MA_FAST, self.MA_SLOW,self.MACD,self.Signal))

class Top_3_indicator(db.Base):
    __tablename__ = 'Top_3_indicator'

    id = Column(Integer, primary_key=True)
    Time = Column('Time', DateTime, nullable=True)
    MA= Column('MA', REAL, nullable=True)
    EMA= Column('EMA', REAL, nullable=True)
    MOMENTUM= Column('MOMENTUM', REAL, nullable=True)
    stock_id = Column(Integer, ForeignKey('Stock.id'))
    stock = relationship("Stock", back_populates="Top_3_indicators")

    def __init__(self, stock):
        self.stock = stock

    def add_value(self, time, ma, ema, momentum):
        self.Time = time
        self.MA = ma
        self.EMA = ema
        self.MOMENTUM = momentum

    def repr(self):
        print('Time: {} MA : {} EMA: {} MOMENTUM: {}'.format(self.Time, self.MA, self.EMA,self.MOMENTUM))



class StockTwits(db.Base):
    __tablename__ = 'StockTwits'

    id = Column(Integer, primary_key=True)
    Time = Column('Time', DateTime, nullable=True)
    Message= Column('Message', TEXT, nullable=True)
    User= Column('User_id',Integer,nullable=True)
    message_id=Column('message_id',Integer,nullable=True)
    stock_id = Column(Integer, ForeignKey('Stock.id'))
    stock = relationship("Stock", back_populates="Messages_Stocktwits")

    def __init__(self, stock):
        self.stock = stock

    def add_value(self, time,message,user,message_id):
        self.Time = time
        self.Message = message
        self.User = user
        self.message_id=message_id

    def repr(self):
        print('Time: {} '.format(self.Time))
        print('Twitter count : {}'.format(self.User))
        print('Message id: {}'.format(self.message_id))
        print('New : {}'.format(self.Message))

class Stock(db.Base):
    __tablename__ = 'Stock'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    last_time = Column(DateTime, nullable=True)
    last_StockTwits_message_id = Column(Integer, default=None)
    Real_prices= relationship("Real_values", uselist=True, back_populates="stock")
    Predictions_LSTM_1step_prices = relationship("Predictions_LSTM_1step", uselist=True, back_populates="stock")
    Bollinger_bands=relationship('Bollinger_Band', uselist=True, back_populates='stock')
    MACD_value=relationship('MACD_values',uselist=True,back_populates='stock')
    Top_3_indicators=relationship('Top_3_indicator',uselist=True,back_populates='stock')
    Messages_Stocktwits = relationship('StockTwits', uselist=True, back_populates='stock')

    def __init__(self,name):
        self.name=name

    def __repr__(self):
        print('El Stock en cuestion es : {}'.format(self.name))
        print('El ultimo valor de actualizacion es : {}'.format(self.last_time))

