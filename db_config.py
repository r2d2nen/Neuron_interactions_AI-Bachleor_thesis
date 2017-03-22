from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Table, ForeignKey
from sqlalchemy import orm
from sqlalchemy.orm import relationship

db_path = '/net/data1/ml2017/database/ml2017.db'

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
    n_max = Column(Float)
    h_omega = Column(Float) #NOTE: hbar
    lec0 = Column(Float)
    lec1 = Column(Float)
    lec2 = Column(Float)
    lec3 = Column(Float)
    lec4 = Column(Float)
    lec5 = Column(Float)
    lec6 = Column(Float)
    lec7 = Column(Float)
    lec8 = Column(Float)
    lec9 = Column(Float)
    lec10 = Column(Float)
    lec11 = Column(Float)
    lec12 = Column(Float)
    lec13 = Column(Float)
    lec14 = Column(Float)
    lec15 = Column(Float)

    children = relationship('Tag', secondary=association_table)

    def __init__(self, date=None, observable=None, energy=None, LECs=[], n_max=None, hbar_omega=None):
        self.date = date
        self.observable = observable
        self.energy = energy
        self.LECs = LECs
        self.n_max = n_max
        self.h_omega = hbar_omega
        if len(LECs) == 0:
            LECs = [None for i in range(16)]
        self.lec0 = LECs[0]
        self.lec1 = LECs[1]
        self.lec2 = LECs[2]
        self.lec3 = LECs[3]
        self.lec4 = LECs[4]
        self.lec5 = LECs[5]
        self.lec6 = LECs[6]
        self.lec7 = LECs[7]
        self.lec8 = LECs[8]
        self.lec9 = LECs[9]
        self.lec10 = LECs[10]
        self.lec11 = LECs[11]
        self.lec12 = LECs[12]
        self.lec13 = LECs[13]
        self.lec14 = LECs[14]
        self.lec15 = LECs[15]
    
    @orm.reconstructor
    def init_on_load(self):
        self.LECs = [self.lec0,
                self.lec1, self.lec2, self.lec3,
                self.lec4, self.lec5, self.lec6,
                self.lec7, self.lec8, self.lec9,
                self.lec10, self.lec11, self.lec12,
                self.lec13, self.lec14, self.lec15]


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
