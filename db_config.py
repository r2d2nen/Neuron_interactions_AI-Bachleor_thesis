from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Table, ForeignKey
from sqlalchemy.orm import relationship

db_path = '/net/data1/ml2017/database/test.db'

Base = declarative_base()
engine = create_engine('sqlite:///' + db_path)

association_table = Table('association', Base.metadata,
        Column('meas_id', Integer, ForeignKey('measurements.id')),
        Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Measurement(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    observable = Column(Float)
    energy = Column(Float)

    children = relationship('Tag', secondary=association_table)

    def __repr__(self):
        return '<Measurement id=%d, date=%s, observable=%d, energy=%d>' %(self.id, self.date, self.observable, self.energy)

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag = Column(String)

    def __repr__(self):
        return '<Tag id=%d, tag=%s>' %(self.id, self.tag)


if __name__ == '__main__':
    '''If this is run from terminal, reconfigures the database to fit the above declarations'''
    Base.metadata.create_all(engine)
