import uuid
from zope.interface import implements

from sqlalchemy import Unicode
from sqlalchemy import UnicodeText 
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer

from eportfolio.models import Base, DomainObject, UUID
from eportfolio.models.container import Container
from eportfolio.interfaces import IProject
from eportfolio.interfaces import IObjectives

class Project(DomainObject, Base):
    
    implements(IProject)
    
    __tablename__ = 'projects'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(Unicode(255))
    number = Column(Unicode(255))
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(UnicodeText) 
    customer_request = Column(UnicodeText)
    customer_benefit = Column(UnicodeText)
    customer_outcome = Column(UnicodeText)
    budget = Column(Integer)
    risks = Column(UnicodeText)
    preconditions = Column(UnicodeText)
    environment = Column(UnicodeText)
    exclusions = Column(UnicodeText)
    
    @property
    def __name__(self):
        return str(self.id)
    
    def __getitem__(self, key):
        if key == 'entries':
            container = Container(self.journal_entries)
            container.__parent__ = self
            container.__name__ = u'entries'
            return container
        if key == 'objectives':
            container = Container(self.objectives, IObjectives)
            container.__parent__ = self
            container.__name__ = u'objectives'
            return container
        
        raise KeyError(key)
        