from db_config import engine, Measurement, Tag, association_table
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import func, distinct
from datetime import datetime


class Datamanager():
    '''
    The datamanager object acts as an interface to the projects database
    It allows you to either save a new measurement as a line in the database,
    or to retrieve previous measurements based on a tag system.
    When adding new lines you must specify a list of tags (for example 'scattering_trainingset')
    Whenever you want to use the data, you provide another list of tags and receive all data entries with that tag
    '''

    def __init__(self):
        self.Session = sessionmaker(bind=engine)
        self.s = self.Session()

    def insert(self, tags=['default'], observable=None, energy=None, LECs=None):
        date = datetime.now()
        #We may still have measurements without LEC information
        if observable is None or energy is None:
            print 'Measurement or energy may not be None, exiting insert'
            return False
        #Handle LECs
        m = Measurement(date=date, observable=observable, energy=energy)
        t = self.s.query(Tag).filter(Tag.tag.in_(tags)).all()
        if not t:
            #If there are no matching tags in database, add all of them
            for tag in tags:
                t = Tag(tag=tag)
                self.s.add(t)
                m.children.append(t)
        else:
            #Add the tags that don't exist
            for tag in t:
                if tag.tag in tags:
                    m.children.append(t)
                    tags.remove(tag)
            for tag in tags:
                t = Tag(tag=tag)
                self.s.add(t)
                m.children.append(t)

        self.s.add(m)
        self.s.commit()
        return True

    '''Returns a Data object for every line matching the specified tag'''
    def read(self, tags=[]):
        data_objects = []
        #The database doesn't like empty lists
        if not tags:
            return []
        #Find all rows in association matching all given tags (and possibly more tags)
        relation_subq = self.s.query(association_table.c.meas_id).\
                join(Tag).filter(Tag.tag.in_(tags)).\
                group_by(association_table.c.meas_id).\
                having(func.count(distinct(association_table.c.tag_id)) >= len (tags)).\
                subquery()
        #Query the matching measurement rows
        matches = self.s.query(Measurement).join(relation_subq).all()
        #print '######'
        #print 'Quering from: ' + str(tags)
        #print matches
        #print '######'
        
        #Translating the objects to allow easier handling
        for meas in matches:
            data_objects.append(Data(meas))
        return data_objects

    '''Returns a list of all used tags'''
    def list_tags(self):
        tags = []
        for tag in self.s.query(Tag.tag):
            if tag[0] not in tags:
                tags.append(tag[0])
        return tags

class Data():
    '''
    This class defines the "data-chunk" that will be returned from the Datamanager.read function
    The desired data will be available through instance variables
    (self.observable, self.energy, self.LEC)
    '''

    def __init__(self, Meas):
        self.observable = Meas.observable
        self.energy = Meas.energy
        #Add LECs

    def __repr__(self):
        return 'Datachunk: observable=%d, energy=%d'%(self.observable, self.energy)

if __name__ == '__main__':
    dm = Datamanager()
    data = dm.read(['test'])
    data = dm.read(['test', 'tested'])
    data = dm.read(['else'])
    #for d in data:
    #    print d
    #print dm.list_tags()
