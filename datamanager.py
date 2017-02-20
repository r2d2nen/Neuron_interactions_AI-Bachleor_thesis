from db_config import engine, Measurement
from sqlalchemy.orm import sessionmaker
from datetime import datetime

'''
The datahandler object acts as an interface to the projects database
It allows you to either save a new measurement as a line in the database,
or to retrieve previous measurements based on a tag system.

When adding new lines you must specify a tag (for example 'scattering_trainingset')

Whenever you want to use the data, you provide the tag and will receive all sets of data with that tag
'''


class Datamanager():

    def __init__(self):
        self.Session = sessionmaker(bind=engine)
        self.s = self.Session()

    def insert(self, tag='Default', value=None, energy=None, LECs=None):
        date = datetime.now()
        '''We may still have measurements without LEC information'''
        if value is None or energy is None:
            print 'Measurement or energy may not be None, exiting insert'
            return False
        #Handle LECs
        m = Measurement(tag=tag, date=date, value=value, energy=energy)
        self.s.add(m)
        self.s.commit()
        return True

    '''Returns a Data object for every line matching the specified tag'''
    def read(self, tag):
        data_objects = []
        for meas in self.s.query(Measurement).filter_by(tag=tag):
            data_objects.append(Data(meas))
        return data_objects

    '''Returns a list of all used tags'''
    def list_tags(self):
        tags = []
        for tag in self.s.query(Measurement.tag):
            if tag[0] not in tags:
                tags.append(tag[0])
        return tags

'''
This class defines the "data-chunk" that will be returned from the Datamanager.read function
The desired data will be available through instance variables (self.value, self.energy, self.LEC)
'''
class Data():

    def __init__(self, Meas):
        self.value = Meas.value
        self.energy = Meas.energy
        #Add LECs

    def __repr__(self):
        return 'Datachunk: value=%d, energy=%d'%(self.value, self.energy)

if __name__ == '__main__':
    dm = Datamanager()
    dm.insert(tag='tested', value=15, energy=99)
    #data = dm.read('test')
    #for d in data:
    #    print d
    print dm.list_tags()
