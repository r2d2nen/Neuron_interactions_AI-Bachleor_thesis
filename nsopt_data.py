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
class Datahandler():

    def __init__(self):
        self.Session = sessionmaker(bind=engine)
        self.s = self.Session()

    def insert(self, tag='Default', value=None, energy=None, LECs=None):
        date = datetime.now()
        '''We may still have measurements without LEC information'''
        if value is None or energy is None:
            print 'Measurement or energy may not be None, exiting insert'
            return False
        '''Handle LECs'''
        m = Measurement(date=date, value=value, energy=energy)
        self.s.add(m)
        self.s.commit()
        return True

    def read(self, tag):
        pass

    def list_tags(self, tag):
        pass



if __name__ == '__main__':
    dh = Datahandler()
    dh.insert(tag='test', value=23, energy=2000)
    
#    
#    '''Create a session'''
#    Session = sessionmaker(bind=engine)
#    s = Session()
#    
#    '''Drop some dummy data'''
#    test_meas = Measurement(tag='test', value=2563., energy=230.)
#    s.add(test_meas)
#    test_meas = Measurement(tag='testing', value=215., energy=100.)
#    s.add(test_meas)
#    s.commit()



