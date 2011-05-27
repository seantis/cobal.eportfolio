import uuid

from zope.interface import implements

from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from sqlalchemy.orm import relation, backref

from eportfolio.interfaces import ICompetence, IIndicatorSets

from eportfolio.models import Base, UUID
from eportfolio.models import DomainObject
from eportfolio.models.container import Container

class Competence(DomainObject, Base):
    
    implements(ICompetence)
    
    __tablename__ = 'competences'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    meta_competence_id = Column(UUID, ForeignKey('meta_competences.id'))
    title = Column(Unicode(255))
    description = Column(UnicodeText)
    sort_order = Column(Integer)
    
    meta_competence = relation('MetaCompetence', backref=backref('competences'))
        
    @property
    def __name__(self):
        return str(self.id)
        
    def __getitem__(self, key):
        if key == 'indicator_sets':
            container = Container(self.indicator_sets, IIndicatorSets)
            container.__parent__ = self
            container.__name__ = u'indicator_sets'
            return container
        
        raise KeyError(key)