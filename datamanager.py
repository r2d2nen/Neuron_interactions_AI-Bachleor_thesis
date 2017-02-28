from db_config import engine, Measurement, Tag, association_table
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import func, distinct
from datetime import datetime


class Datamanager():
    """
    The datamanager object acts as an interface to the projects database
    It allows you to either save a new measurement as a line in the database,
    or to retrieve previous measurements based on a tag system.
    When adding new lines you must specify a list of tags (for example ['scattering', 'trainingset'])
    Whenever you want to use the data, you provide another list of tags and receive all data entries with that tag
    """

    def __init__(self, echo=False):
        engine.echo = echo
        self.Session = sessionmaker(bind=engine)
        self.s = self.Session()

    def insert(self, tags=['default'], observable=None, energy=None, LECs=[]):
        date = datetime.now()
        #We may still have measurements without LEC information
        if observable is None or energy is None:
            print 'Measurement or energy may not be None, exiting insert'
            return False

        #Create a new measurement row and query for mathching tags
        new_meas = Measurement(date=date, observable=observable, energy=energy, LECs=LECs)
        old_tags = self.s.query(Tag).filter(Tag.tag.in_(tags)).all()
        if not old_tags:
            #If there are no matching tags in database, add all of them
            for tag in tags:
                new_tag = Tag(tag=tag)
                self.s.add(new_tag)
                new_meas.children.append(new_tag)
        else:
            #If one or more tags are new, first connect the old ones then create the new ones
            for tag in old_tags:
                if tag.tag in tags:
                    new_meas.children.append(tag)
                    tags.remove(tag.tag)
            for tag in tags:
                new_tag = Tag(tag=tag)
                self.s.add(new_tag)
                new_meas.children.append(new_tag)

        self.s.add(new_meas)
        self.s.commit()
        return True

    """Returns a Data object for every line matching the specified tag"""
    def read(self, tags):
        data_objects = []
        #The database doesn't like empty lists
        if not tags:
            return []
        #Find all rows in association matching all given tags
        relation_subq = self.s.query(association_table.c.meas_id).\
                join(Tag).filter(Tag.tag.in_(tags)).\
                group_by(association_table.c.meas_id).\
                having(func.count(distinct(association_table.c.tag_id)) >= len (tags)).\
                subquery()
        matches = self.s.query(Measurement).join(relation_subq).all()
        
        #Use data objects as a collection of the data.
        for meas in matches:
            data_objects.append(Data(meas))
        return data_objects

    """Returns a list of all used tags"""
    def list_tags(self):
        tags = []
        for tag in self.s.query(Tag.tag):
            if tag[0] not in tags:
                tags.append(tag[0])
        return tags

    """
    Returns the number of lines in the database matching these tags.
    Useful to know exactly how many datapoints you're using.
    """
    def num_matches(self, tags):
        relation_subq = self.s.query(association_table.c.meas_id).\
                join(Tag).filter(Tag.tag.in_(tags)).\
                group_by(association_table.c.meas_id).\
                having(func.count(distinct(association_table.c.tag_id)) >= len (tags)).\
                subquery()
        count = self.s.query(Measurement).join(relation_subq).count()

        return count

class Data():
    """
    This class defines the "data-chunk" that will be returned from the Datamanager.read function
    The desired data will be available through instance variables
    (self.observable, self.energy, self.LEC)
    """

    def __init__(self, Meas):
        self.observable = Meas.observable
        self.energy = Meas.energy
        self.LECs = Meas.LECs

    def __repr__(self):
        return 'Datachunk: observable=%d, energy=%d'%(self.observable, self.energy)

if __name__ == '__main__':
    dm = Datamanager(echo=True)
    #dm.insert(tags=['sgt', 'training', 'test'], observable=100, energy=50)
    #dm.insert(tags=['sgt', 'training'], observable=20, energy=40)
    #dm.insert(tags=['sgt', 'training'], observable=10, energy=5)
    #dm.insert(tags=['sgt', 'validation'], observable=90, energy=55)

    print dm.read(['validation'])

