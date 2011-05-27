import uuid

from zope.interface import implements

from sqlalchemy import Unicode
from sqlalchemy import UnicodeText 
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from sqlalchemy.orm import relation, backref

from eportfolio.interfaces import IIndicatorSet, IIndicators

from eportfolio.models import Base, UUID
from eportfolio.models import Competence
from eportfolio.models.container import Container

class IndicatorSet(Base):
    
    implements(IIndicatorSet)
    
    __tablename__ = 'indicator_sets'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    competence_id = Column(UUID, ForeignKey('competences.id'))
    title = Column(Unicode(255))
    description = Column(UnicodeText)
    sort_order = Column(Integer)
    
    competence = relation(Competence, backref=backref('indicator_sets', lazy='dynamic', 
                        cascade='all,delete-orphan', order_by="indicator_sets.c.sort_order"))
                                                      
    @property
    def __name__(self):
        return str(self.id)
        
    def __getitem__(self, key):
        if key == 'indicators':
            container = Container(self.indicators, IIndicators)
            container.__parent__ = self
            container.__name__ = u'indicators'
            return container
        
        raise KeyError(key)