from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date, Float

Base = declarative_base()
engine = create_engine('sqlite:////net/data1/ml2017/database/test.db', echo=True)

class Measurement(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    tag = Column(String)
    value = Column(Float)
    energy = Column(Float)


    def __repr__(self):
        return '<Measurement id=%d, date=%s, tag=%s, value=%d, energy=%d>' %(self.id, self.date, self.tag, self.value, self.energy)

if __name__ == '__main__':
    '''If this is run from terminal, reconfigures the database to fit the above declarations'''
    Base.metadata.create_all(engine)
