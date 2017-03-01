from db_config import engine, Measurement, Tag, association_table
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import func, distinct
from datetime import datetime
from collections import Counter

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
        tags = tags[:]
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

    """
    Returns a Data object for every line matching the specified tags
    When unique is True, the query will return only the rows matching the tags exactly
    """
    def read(self, tags, unique=False):
        data_objects = []
        #The database doesn't like empty lists
        if not tags:
            return []
        #Find all rows in association matching all given tags
        if unique:
            print 'Unique not properly implemented yet'
            '''relation_subq = self.s.query(association_table).\
                    join(Tag).filter(Tag.tag.in_(tags)).\
                    subquery()
            print 'matching unique'

            matches = self.s.query(Measurement).join(relation_subq).\
                    group_by(association_table.c.meas_id).\
                    having(func.count(distinct(association_table.c.tag_id)) == len(tags)).\
                    all()
            '''
        else:
            relation_subq = self.s.query(association_table.c.meas_id).\
                    join(Tag).filter(Tag.tag.in_(tags)).\
                    group_by(association_table.c.meas_id).\
                    having(func.count(distinct(association_table.c.tag_id)) >= len(tags)).\
                    subquery()

            matches = self.s.query(Measurement).join(relation_subq).all()
        
        #Use data objects as a collection of the data.
        for meas in matches:
            data_objects.append(Data(meas))
        return data_objects

    """
    Delete all matching measurements, tags are not removed but may not be associated with
    any measurements
    """
    def delete(self, tags):
        if not tags:
            print 'No tags given'
            return False
        #Uses the usual query to find the ids of matches
        relation_subq = self.s.query(association_table.c.meas_id).\
                join(Tag).filter(Tag.tag.in_(tags)).\
                group_by(association_table.c.meas_id).\
                having(func.count(distinct(association_table.c.tag_id)) >= len(tags)).\
                subquery()

        ids = self.s.query(Measurement.id).join(relation_subq).all()
        #ids is a list of 1-element tuples, fixing it below
        for i, id in enumerate(ids):
            ids[i] = ids[i][0]

        self.s.execute(Measurement.__table__.delete().where(Measurement.id.in_(ids)))
        self.s.execute(association_table.delete().where(association_table.c.meas_id.in_(ids)))
        self.s.commit()
        print 'Deleted %d elements' %(len(ids))

    """Returns a list of all used tags"""
    def list_tags(self):
        tags = []
        for tag in self.s.query(Tag.tag):
            if tag[0] not in tags:
                tags.append(tag[0])
        return tags

    """Returns all used combinations of tags, and the number of measurements associated"""
    def list_combinations(self):
        combinations = []
        relations = self.s.query(association_table.c.meas_id, Tag.tag).join(Tag).all()
        index = relations[0][0]
        tags = []
        for row in relations:
            #Keeps adding tags when meas_id is the same
            if row[0] == index:
                tags.append(row[1])
            else:
                new = True
                #Checks to see if tag combination already is in combinations and adds 1 to counter
                for comb in combinations:
                    if Counter(comb[0]) == Counter(tags):
                        comb[1] += 1
                        new = False
                        break
                if new:
                    combinations.append([tags, 1])

                #Startes the next entry
                index = row[0]
                tags = [row[1]]

        print '\nNumber of points\tTags'
        for c in combinations:
            print str(c[1]) + '\t\t\t' + str(c[0])

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
    dm.list_combinations()
    #dm.delete(['valid100'])
    #dm.insert(tags=['sgt', 'training', 'test'], observable=100, energy=50)
    #dm.insert(tags=['sgt', 'training'], observable=20, energy=40)
    #dm.insert(tags=['sgt', 'training'], observable=10, energy=5)
    #dm.insert(tags=['sgt', 'validation'], observable=90, energy=55)
    #dm.list_combinations()
