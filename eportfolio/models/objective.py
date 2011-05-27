import uuid
from zope.interface import implements

from sqlalchemy import Table
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relation, backref, dynamic_loader

from eportfolio.models import Base, UUID
from eportfolio.models import Competence
from eportfolio.interfaces import IObjective

objectives_competences = Table('objectives_competences', Base.metadata,
    Column('objective_id', UUID, ForeignKey('objectives.id')),
    Column('competence_id', UUID, ForeignKey('competences.id'))
)

class Objective(Base):
    
    implements(IObjective)
    
    __tablename__ = 'objectives'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID, ForeignKey('projects.id'))
    title = Column(Unicode(255))
    description = Column(UnicodeText)
    sort_order = Column(Integer)
    
    project = relation('Project', 
        backref=backref('objectives', lazy='dynamic', cascade='all,delete-orphan', order_by='objectives.c.sort_order'))
    
    competences = dynamic_loader(Competence, secondary=objectives_competences, 
        backref=backref('objectives', lazy='dynamic'))
    
    @property
    def __name__(self):
        return str(self.id)