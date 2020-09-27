import  Data_manager_SQLalchemy as db
from sqlalchemy import Column, Integer, String, Float,Table,ForeignKey
from sqlalchemy.orm import relationship
from Stock import Stock


Indice_stock_association = Table('Indice_stocks',db.Base.metadata,
                                 Column('Indice_id', Integer, ForeignKey('Indice.id')),
                                 Column('Stock_id', Integer, ForeignKey('Stock.id')),
                                 Column('Stock_name', String, ForeignKey('Stock.name'))
                                 )



class Indice(db.Base):
    __tablename__ = 'Indice'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    stocks=relationship('Stock',secondary=Indice_stock_association)

    def __init__(self,name):
        self.name=name





Down_jones = Indice(name="Down Jones")